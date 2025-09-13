"""Compact a Growatt broker capture JSONL into a dataset JSON file.

Usage:
  python testing/compact_capture.py --in session.jsonl --device min_6000xh_tl \
      --out testing/datasets/min_6000xh_tl_new.json

If --out is omitted it writes to testing/datasets/<device>.json
Keeps the *last* observed value for each register per function.
Accepts events produced by CaptureBackend (ops: read_input, read_holding).
"""
from __future__ import annotations
import argparse, json, pathlib, sys
from typing import Dict, List

OP_MAP = {"read_input": "input", "read_holding": "holding"}

def load_events(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

def compact(lines) -> dict:
    holding: Dict[int, int] = {}
    input_: Dict[int, int] = {}
    for ev in lines:
        op = ev.get("op")
        regs: List[int] = ev.get("regs", [])
        addr = ev.get("addr")
        if op not in OP_MAP or addr is None:
            continue
        table = input_ if op == "read_input" else holding
        for i, val in enumerate(regs):
            table[addr + i] = int(val) & 0xFFFF
    return {
        "holding": {str(k): v for k, v in sorted(holding.items())},
        "input": {str(k): v for k, v in sorted(input_.items())},
    }

def main(argv=None):
    ap = argparse.ArgumentParser(description="Compact capture JSONL to dataset JSON")
    ap.add_argument("--in", required=True, dest="inp", help="Input capture JSONL file")
    ap.add_argument("--device", required=True, help="Device key used for default output name")
    ap.add_argument("--out", help="Output dataset JSON file (default: testing/datasets/<device>.json)")
    ap.add_argument("--source-tag", help="Optional provenance tag (_source field)")
    args = ap.parse_args(argv)

    in_path = pathlib.Path(args.inp)
    if not in_path.exists():
        print(f"[ERROR] input file not found: {in_path}", file=sys.stderr)
        return 2

    out_path = pathlib.Path(args.out) if args.out else pathlib.Path("testing/datasets") / f"{args.device}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    data = compact(load_events(in_path))
    if args.source_tag:
        data["_source"] = args.source_tag

    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(out_path)
    print(f"[OK] wrote dataset: {out_path} (holding={len(data['holding'])} input={len(data['input'])})")
    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
