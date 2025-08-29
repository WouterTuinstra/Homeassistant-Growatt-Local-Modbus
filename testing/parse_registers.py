#!/usr/bin/env python3
"""Parse growatt_registers.md into JSON register maps.

Outputs separate JSON files for holding and input registers and
splits entries into MIN (<3000) and TL-XH (>=3000) groups.
Each record contains register number, Modbus function code, length,
scale (if detectable), unit, and description.
"""

from __future__ import annotations

import json
import pathlib
import re


def parse_registers(md_path: pathlib.Path):
    data = {
        "holding_min": [],
        "holding_tl_xh": [],
        "input_min": [],
        "input_tl_xh": [],
    }

    current_fc = None  # '03' or '04'
    in_table = False

    lines = md_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        line = line.rstrip()

        # Section switches determine function code
        if line.startswith("# "):
            if "Holding Registers" in line:
                current_fc = "03"
            elif "Input Registers" in line:
                current_fc = "04"
            else:
                current_fc = None
            in_table = False
            continue

        # Table header / separator handling
        if line.startswith("|"):
            cols = [c.strip() for c in line.strip().split("|")[1:-1]]
            if cols and cols[0].lower() == "register":
                in_table = True
                continue
            if not in_table or set(cols[0]) <= {"", "-"}:
                continue

            reg_text = cols[0]
            m = re.match(r"(\d+)\s*[–-]\s*(\d+)", reg_text)
            if m:
                start = int(m.group(1))
                end = int(m.group(2))
            else:
                m = re.match(r"(\d+)", reg_text)
                if not m:
                    continue
                start = end = int(m.group(1))
            length = end - start + 1

            desc = cols[1] if len(cols) > 1 else ""
            unit = cols[2] if len(cols) > 2 else ""
            notes = cols[4] if len(cols) > 4 else (cols[3] if len(cols) > 3 else "")

            scale = 1
            m_scale = re.search(r"×\s?(\d+)", desc) or re.search(r"×\s?(\d+)", notes)
            if m_scale:
                try:
                    scale = int(m_scale.group(1))
                except ValueError:
                    pass

            entry = {
                "number": start,
                "function_code": current_fc,
                "length": length,
                "scale": scale,
                "unit": unit,
                "description": desc,
            }

            group = "tl_xh" if start >= 3000 else "min"
            key = f"{'holding' if current_fc == '03' else 'input'}_{group}"
            data[key].append(entry)
        else:
            in_table = False

    return data


def main():
    base = pathlib.Path(__file__).resolve().parent
    md_path = base / "growatt_registers.md"
    registers = parse_registers(md_path)

    for name, entries in registers.items():
        out_path = base / f"{name}.json"
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(entries, fh, indent=2, ensure_ascii=False)
        print(f"Wrote {out_path} ({len(entries)} records)")


if __name__ == "__main__":
    main()
