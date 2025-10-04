"""Utility to build a dataset JSON from a python-modbus-scanner scan file.

Parses lines like:
  found holding register 331, value=4900
  found input   register 2, value=14

Outputs JSON structure consumable by `growatt_broker.simulator.modbus_simulator` datasets:
{
  "holding": {"331": 4900, ...},
  "input": {"2": 14, ...}
}

Usage:
  python build_dataset_from_scan.py --scan-file python-modbus-scanner/scan3.txt \
    --out ../external/growatt-rtu-broker/growatt_broker/simulator/datasets/min_6000xh_tl_from_scan3.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HOLDING_RE = re.compile(r"found holding register (\d+), value=([-\d]+)")
INPUT_RE = re.compile(r"found input\s+register (\d+), value=([-\d]+)")


def parse_scan(path: Path):
    holding: dict[int, int] = {}
    input_: dict[int, int] = {}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if (m := HOLDING_RE.search(line)):
                holding[int(m.group(1))] = int(m.group(2))
            elif (m := INPUT_RE.search(line)):
                input_[int(m.group(1))] = int(m.group(2))
    return holding, input_


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scan-file", required=True, help="Path to scan*.txt")
    p.add_argument("--out", required=True, help="Output dataset JSON path")
    args = p.parse_args()

    scan_path = Path(args.scan_file)
    out_path = Path(args.out)
    holding, input_ = parse_scan(scan_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "holding": {str(k): v for k, v in sorted(holding.items())},
                "input": {str(k): v for k, v in sorted(input_.items())},
            },
            f,
            indent=2,
        )
    print(
        f"Wrote dataset with {len(holding)} holding and {len(input_)} input registers to {out_path}"
    )


if __name__ == "__main__":  # pragma: no cover
    main()
