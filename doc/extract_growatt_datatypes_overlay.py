#!/usr/bin/env python3
"""Generate an overlay from growatt_register_data_types.json.

The data-types catalogue contains per-register hints (enums, bitfields, scaling
notes, attributes, etc.). This script reshapes that information into an overlay
so we can review conflicts before merging human-friendly strings and type
details into the canonical dataset.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DOC_DIR = Path(__file__).resolve().parent
TYPES_PATH = DOC_DIR / "growatt_register_data_types.json"
CATALOG_PATH = DOC_DIR / "register_catalog.json"
BEST_GUESS_V2_PATH = DOC_DIR / "growatt_registers_best_guess.v2.json"
DEFAULT_OUTPUT = DOC_DIR / "overlays" / "growatt_datatypes_overlay.json"


def register_id(table: str, start: int, end: int) -> str:
    return f"{table}:{start}" if start == end else f"{table}:{start}-{end}"


def merge_strings(dest: Dict[str, Dict[str, str]], source: str, key: str, value: Optional[str]) -> None:
    if not value:
        return
    text = str(value).strip()
    if not text:
        return
    bucket = dest.setdefault(source, {})
    bucket.setdefault(key, text)


def to_enum_list(values: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for raw_value, meta in values.items():
        try:
            value = int(raw_value)
        except ValueError:
            value = raw_value
        entry = {"value": value, "label": meta.get("label")}
        if meta.get("description"):
            entry["description"] = meta["description"]
        items.append(entry)
    return items


def to_bitfield_list(flags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for flag in flags:
        entry = {"bit": flag.get("bit"), "label": flag.get("name")}
        if flag.get("description"):
            entry["description"] = flag["description"]
        result.append(entry)
    return result


def expected_encoding(kind: Optional[str]) -> Optional[str]:
    mapping = {
        "enum": "enum",
        "bitfield": "bitfield",
        "ascii": "ascii",
        "raw": "raw",
        "scaled": "numeric",
        "scaled_signed": "numeric",
        "scaled_unsigned": "numeric",
    }
    return mapping.get(kind)


def build_overlay() -> Dict[str, Any]:
    data_types = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
    type_definitions: Dict[str, Dict[str, Any]] = data_types.get("types", {})
    register_types: List[Dict[str, Any]] = data_types.get("register_types", [])

    # Build quick lookup for catalog blocks to check lengths
    catalog_blocks = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_blocks = catalog_blocks.get("blocks", {})

    overlay: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "enum_values": [],
            "bitfields": [],
            "source_strings": {},
        }
    )

    warnings: List[str] = []

    best_guess = json.loads(BEST_GUESS_V2_PATH.read_text(encoding="utf-8"))
    register_lookup = {
        item["id"]: item for item in best_guess.get("register_values", [])
    }

    for entry in register_types:
        table = entry.get("table")
        start = entry.get("register")
        end = entry.get("register_end", start)
        type_key = entry.get("type")
        if table not in {"holding", "input"} or start is None:
            continue

        reg_id = register_id(table, start, end)
        overlay_entry = overlay[reg_id]

        type_info = type_definitions.get(type_key, {})
        if not type_info:
            warnings.append(f"[WARN] Missing type definition '{type_key}' for {reg_id}")

        # Type hints for validation/comparison
        # Candidate enums / bitfields
        if type_info.get("kind") == "enum" and type_info.get("values"):
            enums = to_enum_list(type_info["values"])
            if not overlay_entry["enum_values"]:
                overlay_entry["enum_values"] = enums
        if type_info.get("kind") == "bitfield" and type_info.get("flags"):
            bits = to_bitfield_list(type_info["flags"])
            if not overlay_entry["bitfields"]:
                overlay_entry["bitfields"] = bits

        # Gather descriptive strings
        strings = overlay_entry["source_strings"]
        merge_strings(strings, "growatt_data_types", "type_description", type_info.get("description"))
        merge_strings(strings, "growatt_data_types", "notes", type_info.get("notes"))
        merge_strings(strings, "growatt_data_types", "register_description", entry.get("description"))
        if entry.get("attributes"):
            merge_strings(
                strings,
                "growatt_data_types",
                "attributes",
                ", ".join(map(str, entry["attributes"]))
            )

        # Basic structural validation versus catalog
        block = catalog_blocks.get(entry.get("block_id", ""))
        if not block:
            block = catalog_blocks.get(register_id(table, start, end))
        if block:
            expected_len = end - start + 1
            cat_len = block.get("length")
            if cat_len and expected_len > cat_len:
                warnings.append(
                    f"[WARN] {reg_id}: datatype length {expected_len} exceeds catalog block length {cat_len}"
                )

        # Compare against best guess entry for conflicts
        best = register_lookup.get(reg_id)
        if not best:
            warnings.append(f"[WARN] {reg_id}: not present in best guess export")
        else:
            expected_len = end - start + 1
            if best.get("length") != expected_len:
                warnings.append(
                    f"[WARN] {reg_id}: length mismatch (best guess {best.get('length')} vs datatype {expected_len})"
                )

            if type_info.get("read_write") is not None:
                if bool(type_info["read_write"]) != bool(best.get("writable")):
                    warnings.append(
                        f"[WARN] {reg_id}: writable mismatch (datatype {type_info['read_write']} vs best guess {best.get('writable')})"
                    )

            kind = type_info.get("kind")
            expected_enc = expected_encoding(kind)
            if expected_enc and best.get("value_encoding") and best.get("value_encoding") != expected_enc:
                warnings.append(
                    f"[WARN] {reg_id}: encoding mismatch (datatype kind {kind} -> {expected_enc} vs best guess {best.get('value_encoding')})"
                )

            if kind in {"scaled", "scaled_signed", "scaled_unsigned"}:
                dt_scale = type_info.get("scale")
                if dt_scale is not None and best.get("scale") not in (dt_scale, str(dt_scale)):
                    warnings.append(
                        f"[WARN] {reg_id}: scale mismatch (datatype {dt_scale} vs best guess {best.get('scale')})"
                    )

    if warnings:
        for line in warnings:
            print(line)

    return overlay


def build_document(overlay: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "generator": Path(__file__).name,
        "source_files": {
            "growatt_register_data_types.json": str(TYPES_PATH.relative_to(DOC_DIR)),
            "register_catalog.json": str(CATALOG_PATH.relative_to(DOC_DIR)),
            "growatt_registers_best_guess.v2.json": str(BEST_GUESS_V2_PATH.relative_to(DOC_DIR)),
        },
        },
        "overlays": overlay,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Destination overlay path")
    args = parser.parse_args()

    overlay = build_overlay()
    document = build_document(dict(sorted(overlay.items())))

    output_path = args.output if args.output.is_absolute() else DOC_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
