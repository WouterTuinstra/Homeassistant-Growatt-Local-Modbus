#!/usr/bin/env python3
"""Create an overlay from the vendor Growatt tables JSON.

The overlay captures descriptive strings from
`Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json` and checks
for conflicts with the current best-guess dataset.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DOC_DIR = Path(__file__).resolve().parent
TABLES_PATH = DOC_DIR / "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json"
BEST_GUESS_PATH = DOC_DIR / "growatt_registers_best_guess.v2.json"
CATALOG_PATH = DOC_DIR / "register_catalog.json"
DEFAULT_OUTPUT = DOC_DIR / "overlays" / "growatt_vendor_tables_overlay.json"


REPLACEMENTS = {
    "°C": "degC",
    "°F": "degF",
    "°": "deg",
    "µ": "u",
    "Ω": "Ohm",
    "–": "-",
    "—": "-",
    "\u202f": " ",
    "\u3000": " ",
    "\uff08": "(",  # fullwidth (
    "\uff09": ")",  # fullwidth )
    "\uff1b": ";",  # fullwidth semicolon
    "\uff1a": ":",  # fullwidth colon
    "\uff0c": ",",  # fullwidth comma
    "\uff0d": "-",
    "\uff0e": ".",
    "\uff1f": "?",
    "\u3001": ",",
}


def sanitize(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = str(value)
    for src, dest in REPLACEMENTS.items():
        text = text.replace(src, dest)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text if text else None


def parse_register_field(field: str) -> Optional[Tuple[int, int]]:
    numbers = re.findall(r"\d+", field)
    if not numbers:
        return None
    start = int(numbers[0])
    end = int(numbers[1]) if len(numbers) > 1 else start
    return start, end


def build_register_id(table: str, start: int, end: int) -> str:
    return f"{table}:{start}" if start == end else f"{table}:{start}-{end}"


def load_best_guess() -> Dict[str, Dict[str, Any]]:
    data = json.loads(BEST_GUESS_PATH.read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in data.get("register_values", [])}


def load_catalog_blocks() -> Dict[str, Dict[str, Any]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return catalog.get("blocks", {})


def build_overlay() -> Dict[str, Any]:
    tables = json.loads(TABLES_PATH.read_text(encoding="utf-8"))
    best_guess = load_best_guess()
    catalog_blocks = load_catalog_blocks()

    overlay: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "source_strings": {},
        }
    )

    warnings: list[str] = []

    for table_name, entries in tables.items():
        table = table_name.lower()
        if table not in {"holding", "input"}:
            continue

        for entry in entries:
            reg_field = sanitize(entry.get("register")) or ""
            parsed = parse_register_field(reg_field)
            if not parsed:
                warnings.append(f"[WARN] {table}:{reg_field}: unable to parse register field")
                continue
            start, end = parsed
            reg_id = build_register_id(table, start, end)

            overlay_entry = overlay[reg_id]
            strings = overlay_entry.setdefault("source_strings", {}).setdefault("vendor_tables", {})

            for key in ("variable", "description", "value", "note", "initial"):
                val = sanitize(entry.get(key))
                if val and key not in strings:
                    strings[key] = val

            unit = sanitize(entry.get("unit"))
            if unit:
                strings.setdefault("unit", unit)

            vendor_writable = None
            write_flag = (entry.get("write_or_not") or "").upper()
            if "W" in write_flag:
                vendor_writable = True
            elif "R" in write_flag:
                vendor_writable = False

            best = best_guess.get(reg_id)
            if not best:
                warnings.append(f"[WARN] {reg_id}: vendor table entry missing from best guess")
                continue

            # Validate length
            expected_length = end - start + 1
            if best.get("length") != expected_length:
                warnings.append(
                    f"[WARN] {reg_id}: length mismatch (vendor {expected_length} vs best guess {best.get('length')})"
                )

            # Validate unit
            if unit and best.get("unit") and unit.lower() != str(best["unit"]).lower():
                warnings.append(
                    f"[WARN] {reg_id}: unit mismatch (vendor '{unit}' vs best guess '{best['unit']}')"
                )

            if vendor_writable is not None and bool(best.get("writable")) != vendor_writable:
                warnings.append(
                    f"[WARN] {reg_id}: writable mismatch (vendor {vendor_writable} vs best guess {best.get('writable')})"
                )

            # Basic catalog length check for ranges
            block = None
            for block_id, block_info in catalog_blocks.items():
                if block_info.get("reg_type") != table:
                    continue
                start_reg = block_info.get("register")
                if start_reg is None:
                    continue
                end_reg = start_reg + block_info.get("length", 0) - 1
                if start_reg <= start <= end_reg:
                    block = block_info
                    break
            if block and end > block.get("register", 0) + block.get("length", 0) - 1:
                warnings.append(
                    f"[WARN] {reg_id}: vendor range exceeds catalog block {block.get('label')}"
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
                "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json": str(TABLES_PATH.relative_to(DOC_DIR)),
                "growatt_registers_best_guess.v2.json": str(BEST_GUESS_PATH.relative_to(DOC_DIR)),
                "register_catalog.json": str(CATALOG_PATH.relative_to(DOC_DIR)),
            },
        },
        "overlays": dict(sorted(overlay.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Destination overlay path")
    args = parser.parse_args()

    overlay = build_overlay()
    document = build_document(overlay)

    output_path = args.output if args.output.is_absolute() else DOC_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
