#!/usr/bin/env python3
"""Convert growatt_registers_best_guess.json into the canonical register data schema."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

DOC_DIR = Path(__file__).resolve().parent
SPEC_PATH = DOC_DIR / "growatt_registers_best_guess.json"
OUTPUT_PATH = DOC_DIR / "growatt_registers_best_guess.v2.json"
CATALOG_PATH = DOC_DIR / "register_catalog.json"
DATATYPES_PATH = DOC_DIR / "growatt_register_data_types.json"
VENDOR_TABLES_PATH = DOC_DIR / "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json"


@dataclass
class SpecEntry:
    table: str
    section: str
    register: int
    register_end: int
    payload: Dict[str, Any]

def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_range(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    text = value.strip()
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)", text)
    if not match:
        return None
    def convert(token: str) -> Any:
        return float(token) if "." in token else int(token)
    return {"min": convert(match.group(1)), "max": convert(match.group(2))}


def detect_encoding(description: Optional[str], unit: Optional[str]) -> str:
    text = (description or "").lower()
    if any(token in text for token in ("ascii", "string", "serial")):
        return "ascii"
    if "bitfield" in text or "bit field" in text or "bit mask" in text:
        return "bitfield"
    if unit and unit.lower() in {"text", "string"}:
        return "ascii"
    return "numeric"


def build_register_id(table: str, start: int, end: int) -> str:
    if start == end:
        return f"{table}:{start}"
    return f"{table}:{start}-{end}"


def load_datatypes() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    if not DATATYPES_PATH.exists():
        return {}, {}
    payload = json.loads(DATATYPES_PATH.read_text(encoding="utf-8"))
    type_defs = payload.get("types", {})
    register_entries = payload.get("register_types", [])
    mapping: Dict[str, Dict[str, Any]] = {}
    for entry in register_entries:
        table = entry.get("table")
        start = entry.get("register")
        end = entry.get("register_end", start)
        if table not in {"holding", "input"} or start is None:
            continue
        reg_id = build_register_id(table, int(start), int(end))
        mapping[reg_id] = entry
    return mapping, type_defs


def expected_encoding(kind: Optional[str]) -> Optional[str]:
    mapping = {
        "enum": "enum",
        "bitfield": "bitfield",
        "ascii": "ascii",
        "raw": "raw",
        "scaled": "numeric",
        "scaled_signed": "numeric",
        "scaled_unsigned": "numeric",
        "struct": "raw",
    }
    return mapping.get(kind)


def to_enum_list(values: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for raw_value, meta in values.items():
        try:
            value = int(raw_value)
        except ValueError:
            value = raw_value
        entry = {"value": value}
        label = sanitize_string(meta.get("label"))
        if label:
            entry["label"] = label
        desc = sanitize_string(meta.get("description"))
        if desc:
            entry["description"] = desc
        entries.append(entry)
    return entries


def to_bitfield_list(flags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for flag in flags:
        entry = {"bit": flag.get("bit")}
        label = sanitize_string(flag.get("name"))
        if label:
            entry["label"] = label
        desc = sanitize_string(flag.get("description"))
        if desc:
            entry["description"] = desc
        result.append(entry)
    return result


def sort_registers(registers: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    def sort_key(item: Tuple[str, Dict[str, Any]]) -> Tuple[int, int, int]:
        reg_id, payload = item
        reg_type, _, number_part = reg_id.partition(":")
        start = payload.get("register", 0)
        reg_type_rank = 0 if reg_type == "holding" else 1
        return (reg_type_rank, start, payload.get("length", 1))

    return [value for _, value in sorted(registers.items(), key=sort_key)]


def sanitize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = str(value)
    replacements = {
        "°C": "degC",
        "°F": "degF",
        "°": "deg",
        "µ": "u",
        "Ω": "Ohm",
        "–": "-",
        "—": "-",
        "\u202f": " ",
        "\u3001": ",",
        "\uff08": "(",
        "\uff09": ")",
        "\uff1b": ";",
        "\uff1a": ":",
        "\uff0c": ",",
        "\uff0d": "-",
        "\uff0e": ".",
        "\uff1f": "?",
    }
    for src, dest in replacements.items():
        text = text.replace(src, dest)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text if text else None


def parse_register_field(field: str) -> Optional[Tuple[int, int]]:
    if not field:
        return None
    numbers = re.findall(r"\d+", field)
    if not numbers:
        return None
    start = int(numbers[0])
    end = int(numbers[1]) if len(numbers) > 1 else start
    return start, end


def load_vendor_tables() -> Tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
    if not VENDOR_TABLES_PATH.exists():
        return {}, []
    data = json.loads(VENDOR_TABLES_PATH.read_text(encoding="utf-8"))
    mapping: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    warnings: List[str] = []

    for table_name, entries in data.items():
        table = table_name.lower()
        if table not in {"holding", "input"}:
            continue
        for entry in entries:
            reg_field = sanitize_string(entry.get("register")) or ""
            parsed = parse_register_field(reg_field)
            if not parsed:
                warnings.append(
                    f"[WARN] {table}:{reg_field}: unable to parse vendor register field"
                )
                continue
            start, end = parsed
            reg_id = build_register_id(table, start, end)
            cleaned = {
                "table": table,
                "start": start,
                "end": end,
                "variable": sanitize_string(entry.get("variable")),
                "description": sanitize_string(entry.get("description")),
                "value": sanitize_string(entry.get("value")),
                "note": sanitize_string(entry.get("note")),
                "initial": sanitize_string(entry.get("initial")),
                "unit": sanitize_string(entry.get("unit")),
                "write_or_not": sanitize_string(entry.get("write_or_not")),
                "page": sanitize_string(entry.get("page")) or None,
            }
            mapping[reg_id].append(cleaned)

    return mapping, warnings


def interpret_vendor_writable(flag: Optional[str]) -> Optional[bool]:
    if not flag:
        return None
    flag_upper = flag.upper()
    if "W" in flag_upper:
        return True
    if "R" in flag_upper:
        return False
    return None


def merge_vendor_tables(
    register_values: Dict[str, Dict[str, Any]],
    vendor_map: Dict[str, List[Dict[str, Any]]],
) -> List[str]:
    warnings: List[str] = []

    for reg_id, entries in vendor_map.items():
        reg = register_values.get(reg_id)
        if not reg:
            warnings.append(f"[WARN] {reg_id}: vendor table entry missing from best guess")
            continue

        strings = reg.setdefault("source_strings", {})
        vendor_bucket = strings.setdefault("vendor_tables", {})

        vendor_units = set()
        vendor_writable_flags: List[Optional[bool]] = []

        for entry in entries:
            for src_key, dest_key in (
                ("variable", "variable"),
                ("description", "description"),
                ("value", "value"),
                ("note", "note"),
                ("initial", "initial"),
                ("unit", "unit"),
                ("write_or_not", "access"),
                ("page", "page"),
            ):
                val = entry.get(src_key)
                if val and dest_key not in vendor_bucket:
                    vendor_bucket[dest_key] = val

            if entry.get("unit"):
                vendor_units.add(entry["unit"])
            vendor_writable_flags.append(interpret_vendor_writable(entry.get("write_or_not")))

        vendor_unit = next(iter(vendor_units)) if vendor_units else None
        if vendor_unit and reg.get("unit") and vendor_unit.lower() != str(reg.get("unit")).lower():
            warnings.append(
                f"[WARN] {reg_id}: unit mismatch (vendor '{vendor_unit}' vs best guess '{reg.get('unit')}')"
            )

        vendor_writable = next((flag for flag in vendor_writable_flags if flag is not None), None)
        if vendor_writable is not None and bool(reg.get("writable")) != vendor_writable:
            warnings.append(
                f"[WARN] {reg_id}: writable mismatch (vendor {vendor_writable} vs best guess {reg.get('writable')})"
            )

    return warnings


def collect_entries(raw: Dict[str, Any]) -> Dict[str, List[SpecEntry]]:
    tables: Dict[str, List[SpecEntry]] = {}
    for table in ("holding", "input"):
        entries: List[SpecEntry] = []
        current_sections: Dict[str, Dict[str, Any]] = {}
        for item in raw.get(table, []):
            if item.get("type") == "section":
                title = item.get("title") or "Unnamed section"
                current_sections[title] = item
                continue
            if item.get("type") != "entry":
                continue
            section = item.get("section") or "Unnamed section"
            entry = SpecEntry(
                table=table,
                section=section,
                register=int(item.get("register_start", item.get("register", 0))),
                register_end=int(item.get("register_end", item.get("register", 0))),
                payload=item,
            )
            entries.append(entry)
        entries.sort(key=lambda e: (e.register, e.register_end))
        tables[table] = entries
    return tables


def build_register_value(entry: SpecEntry, block_id: str) -> Tuple[str, Dict[str, Any]]:
    payload = entry.payload
    start = entry.register
    end = entry.register_end
    length = end - start + 1
    record_id = build_register_id(entry.table, start, end)

    description = sanitize_string(payload.get("description"))
    unit = sanitize_string(payload.get("unit"))
    encoding = detect_encoding(description, unit)
    value_range = parse_range(payload.get("range"))

    register_value: Dict[str, Any] = {
        "id": record_id,
        "label": sanitize_string(payload.get("name")) or record_id,
        "description": description,
        "register": start,
        "length": length,
        "reg_type": entry.table,
        "unit": unit,
        "writable": bool(payload.get("access") and "W" in str(payload["access"]).upper()),
        "scale": None,
        "value_encoding": encoding,
        "enum_values": [],
        "bitfields": [],
        "decoder": None,
        "value_range": value_range,
        "aliases": [],
        "source_strings": {},
    }

    source_strings: Dict[str, Dict[str, str]] = {}

    def add_string(kind: str, value: Optional[str]) -> None:
        value = sanitize_string(value)
        if not value:
            return
        entries = source_strings.setdefault("best_guess", {})
        entries.setdefault(kind, value)

    add_string("label", payload.get("name"))
    add_string("note", payload.get("note"))
    add_string("description", description)
    attributes = payload.get("attributes")
    if isinstance(attributes, list):
        for attr in attributes:
            attr_text = sanitize_string(str(attr))
            if attr_text:
                add_string(f"attribute_{attr_text}", attr_text)

    if source_strings:
        register_value["source_strings"] = source_strings

    return record_id, register_value


def find_block_for_entry(entry: SpecEntry, catalog_blocks: Dict[str, Dict[str, Any]]) -> Optional[str]:
    for block_id, block in catalog_blocks.items():
        if block.get("reg_type") != entry.table:
            continue
        start = block["register"]
        end = start + block["length"] - 1
        if start <= entry.register and entry.register_end <= end:
            return block_id
    return None


def normalize_label(label: Optional[str]) -> str:
    text = (label or "").strip().lower()
    text = re.sub(r"\s*\(.*?\)\s*$", "", text)
    return text


def compare_sections(
    block_id: str,
    catalog_block: Dict[str, Any],
    discovered_sections: Dict[str, Dict[str, int]],
) -> None:
    catalog_sections = catalog_block.get("sections", [])

    catalog_by_label: Dict[str, List[Tuple[str, int, int]]] = {}
    for sec in catalog_sections:
        label = sec.get("label")
        start = sec.get("register")
        length = sec.get("length")
        if start is None or length is None:
            continue
        catalog_by_label.setdefault(normalize_label(label), []).append((label, start, start + length - 1))

    discovered_by_label: Dict[str, List[Tuple[str, int, int]]] = {}
    for label, info in discovered_sections.items():
        start = info["start"]
        end = info["end"]
        discovered_by_label.setdefault(normalize_label(label), []).append((label, start, end))

    matched_catalog: Dict[Tuple[str, int, int], bool] = {}

    for norm_label, entries in discovered_by_label.items():
        catalog_entries = catalog_by_label.get(norm_label)
        if not catalog_entries:
            for label, start, end in entries:
                print(
                    f"[WARN] Block {block_id}: section not in catalog -> {label} ({start}-{end})"
                )
            continue

        # attempt to match each discovered entry to a catalog entry
        remaining_catalog = [item for item in catalog_entries if not matched_catalog.get(item)]
        for label, start, end in entries:
            match = None
            for candidate in remaining_catalog:
                cat_label, cat_start, cat_end = candidate
                if cat_start <= start <= cat_end:
                    match = candidate
                    break
            if match is None:
                print(
                    f"[WARN] Block {block_id}: no catalog match for {label} ({start}-{end})"
                )
                continue

            remaining_catalog.remove(match)
            matched_catalog[match] = True
            cat_label, cat_start, cat_end = match
            if start < cat_start or end > cat_end:
                print(
                    f"[WARN] Block {block_id}: discovered range {label} ({start}-{end}) extends beyond catalog {cat_label} ({cat_start}-{cat_end})"
                )
            elif start > cat_start or end < cat_end:
                print(
                    f"[INFO] Block {block_id}: partial coverage for {cat_label} -> best guess {start}-{end} within {cat_start}-{cat_end}"
                )

    for norm_label, catalog_entries in catalog_by_label.items():
        for entry in catalog_entries:
            if not matched_catalog.get(entry):
                label, start, end = entry
                print(
                    f"[WARN] Block {block_id}: catalog section without best-guess coverage -> {label} ({start}-{end})"
                )


def build_document(raw: Dict[str, Any], catalog: Dict[str, Any]) -> Dict[str, Any]:
    catalog_blocks: Dict[str, Dict[str, Any]] = catalog.get("blocks", {})
    datatype_map, type_defs = load_datatypes()
    vendor_map, vendor_parse_warnings = load_vendor_tables()

    tables = collect_entries(raw)

    register_values: Dict[str, Dict[str, Any]] = {}
    block_usage: Dict[str, Dict[str, Any]] = {}

    unmatched_entries: List[SpecEntry] = []

    for table, entries in tables.items():
        for entry in entries:
            block_id = find_block_for_entry(entry, catalog_blocks)
            if not block_id:
                unmatched_entries.append(entry)
                continue

            usage = block_usage.setdefault(block_id, {"sections": {}, "entries": []})
            usage["entries"].append(entry)
            section_label = entry.section.strip() if entry.section else "Unnamed section"
            section_info = usage["sections"].setdefault(
                section_label, {"start": entry.register, "end": entry.register_end}
            )
            section_info["start"] = min(section_info["start"], entry.register)
            section_info["end"] = max(section_info["end"], entry.register_end)

            cid, value = build_register_value(entry, block_id)
            if cid not in register_values:
                register_values[cid] = value

    if unmatched_entries:
        print("[WARN] Entries without matching catalog block:")
        for entry in unmatched_entries[:20]:
            print(
                f"  - {entry.table} register {entry.register}-{entry.register_end} section '{entry.section}'"
            )
        if len(unmatched_entries) > 20:
            print(f"  ... and {len(unmatched_entries) - 20} more")

    if vendor_parse_warnings:
        for line in vendor_parse_warnings:
            print(line)

    datatype_warnings: List[str] = []
    for reg_id, dt_entry in datatype_map.items():
        reg = register_values.get(reg_id)
        if not reg:
            datatype_warnings.append(f"[WARN] {reg_id}: datatype entry missing from best guess")
            continue

        type_key = dt_entry.get("type")
        type_info = type_defs.get(type_key, {})

        start = dt_entry.get("register")
        end = dt_entry.get("register_end", start)
        if start is not None and end is not None:
            expected_length = int(end) - int(start) + 1
            if reg.get("length") != expected_length:
                datatype_warnings.append(
                    f"[WARN] {reg_id}: length mismatch (datatype {expected_length} vs best guess {reg.get('length')})"
                )

        if "read_write" in type_info:
            reg["writable"] = bool(type_info["read_write"])

        kind = type_info.get("kind")
        expected_enc = expected_encoding(kind)
        if expected_enc:
            reg["value_encoding"] = expected_enc

        if type_info.get("scale") is not None:
            reg["scale"] = type_info["scale"]

        if kind == "enum" and type_info.get("values"):
            reg["enum_values"] = to_enum_list(type_info["values"])

        if kind == "bitfield" and type_info.get("flags"):
            reg["bitfields"] = to_bitfield_list(type_info["flags"])

        strings = reg.setdefault("source_strings", {})
        bucket = strings.setdefault("growatt_data_types", {})
        reg_desc = sanitize_string(dt_entry.get("description"))
        if reg_desc:
            bucket.setdefault("register_description", reg_desc)
        type_desc = sanitize_string(type_info.get("description"))
        if type_desc:
            bucket.setdefault("type_description", type_desc)
        notes = sanitize_string(type_info.get("notes"))
        if notes:
            bucket.setdefault("notes", notes)
        if dt_entry.get("attributes"):
            attrs = ", ".join(filter(None, (sanitize_string(str(a)) for a in dt_entry["attributes"])))
            if attrs:
                bucket.setdefault("attributes", attrs)

    if datatype_warnings:
        for line in datatype_warnings:
            print(line)

    vendor_warnings = merge_vendor_tables(register_values, vendor_map)
    if vendor_warnings:
        for line in vendor_warnings:
            print(line)

    blocks: Dict[str, Dict[str, Any]] = {}
    for block_id in sorted(block_usage.keys()):
        catalog_block = catalog_blocks.get(block_id)
        if not catalog_block:
            print(f"[WARN] Block id {block_id} referenced by best guess but missing in catalog")
            continue

        compare_sections(block_id, catalog_block, block_usage[block_id]["sections"])

        block_entry = {
            "label": catalog_block.get("label"),
            "reg_type": catalog_block.get("reg_type"),
            "register": catalog_block.get("register"),
            "length": catalog_block.get("length"),
            "description": catalog_block.get("description"),
            "sections": catalog_block.get("sections", []),
        }
        blocks[block_id] = block_entry

    holding_blocks = [bid for bid, block in blocks.items() if block.get("reg_type") == "holding"]
    input_blocks = [bid for bid, block in blocks.items() if block.get("reg_type") == "input"]

    catalog_meta = catalog.get("meta", {})

    document: Dict[str, Any] = {
        "meta": {
            "version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": Path(__file__).name,
            "source_files": {
                "growatt_registers_best_guess": {
                    "path": str(SPEC_PATH.relative_to(DOC_DIR)),
                    "sha256": sha256sum(SPEC_PATH),
                },
                "register_catalog": {
                    "path": str(CATALOG_PATH.relative_to(DOC_DIR)),
                    "sha256": sha256sum(CATALOG_PATH),
                },
            },
        },
        "catalog": {
            "version": catalog_meta.get("version"),
            "path": str(CATALOG_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(CATALOG_PATH),
        },
        "inverter_families": {
            "vendor_best_guess": {
                "label": "Vendor best guess",
                "description": "Curated interpretation derived from growatt_registers_best_guess.json",
                "aliases": ["vendor"],
                "holding_blocks": sorted(holding_blocks),
                "input_blocks": sorted(input_blocks),
                "notes": "Sections and ranges aligned with register_catalog.json",
            }
        },
        "blocks": blocks,
        "register_values": sort_registers(register_values),
    }

    return document


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"Destination file (default: {OUTPUT_PATH.name})",
    )
    args = parser.parse_args()

    raw = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    document = build_document(raw, catalog)

    output_path = args.output
    if not output_path.is_absolute():
        output_path = DOC_DIR / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
