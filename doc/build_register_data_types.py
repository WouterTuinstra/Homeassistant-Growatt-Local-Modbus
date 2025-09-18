#!/usr/bin/env python3
"""Generate growatt_register_data_types.json from the integration mapping."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent
MAPPING_PATH = DOC_DIR / "growatt_local_registers.json"
OUTPUT_PATH = DOC_DIR / "growatt_register_data_types.json"


def load_mapping() -> dict:
    with MAPPING_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def type_id(length: int, scale: float | int, read_write: bool) -> str:
    bits = length * 16
    if scale == 1 or scale == 1.0:
        scale_part = "scale1"
    elif isinstance(scale, float) and scale != int(scale):
        scale_part = f"scale{scale}".replace(".", "p")
    else:
        scale_part = f"scale{int(scale)}"
    suffix = "_rw" if read_write else ""
    return f"u{bits}_{scale_part}{suffix}"


def main() -> None:
    mapping = load_mapping()
    types: dict[str, dict] = {}
    reg_map: dict[int, dict] = {}

    for family, groups in mapping.items():
        for group_name, entries in groups.items():
            for entry in entries:
                length = entry.get("length", 1)
                scale = entry.get("scale", 10)
                read_write = entry.get("read_write", False)
                tid = type_id(length, scale, read_write)

                if tid not in types:
                    types[tid] = {
                        "registers": length,
                        "bits": length * 16,
                        "scale": scale,
                        "read_write": bool(read_write),
                    }

                register = entry["register"]
                reg_info = reg_map.setdefault(register, {
                    "register": register,
                    "type": tid,
                    "attributes": set(),
                    "families": set(),
                })
                reg_info["attributes"].add(entry["name"])
                reg_info["families"].add(family)

    # serialise sets
    register_types = []
    for reg in sorted(reg_map):
        info = reg_map[reg]
        register_types.append({
            "register": info["register"],
            "type": info["type"],
            "attributes": sorted(info["attributes"]),
            "families": sorted(info["families"]),
        })

    data = {
        "types": dict(sorted(types.items())),
        "register_types": register_types,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    print(f"Wrote {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
