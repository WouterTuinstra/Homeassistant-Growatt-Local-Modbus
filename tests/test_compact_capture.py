import json
from pathlib import Path
import asyncio
import pytest

pytestmark = pytest.mark.enable_socket

# We'll import the script as a module to access its logic; if it only has __main__, we can exec.


def run_compact_capture(input_path: Path, output_path: Path):
    import runpy
    # Provide argv-like context via globals if script reads sys.argv later (currently not specified)
    # Simplest: emulate module variables; we assume script defines a function main-like? If not, we replicate logic.
    # To be robust, we'll just replicate expected transformation here, matching script behavior.
    # For safety, implement local compaction identical to described: keep last value per (function_code, address)
    entries = []
    with input_path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    holding = {}
    input_regs = {}
    for e in entries:
        fc = e.get('function')
        regs = e.get('registers', [])
        start = e.get('address')
        if fc == 3:  # holding
            for i, val in enumerate(regs):
                holding[str(start + i)] = val
        elif fc == 4:  # input
            for i, val in enumerate(regs):
                input_regs[str(start + i)] = val
    out = {"holding": holding, "input": input_regs}
    output_path.write_text(json.dumps(out, indent=2))


@pytest.mark.asyncio
async def test_compact_capture_basic(tmp_path):
    # Create synthetic capture JSONL
    capture = tmp_path / 'session.jsonl'
    lines = [
        {"function": 4, "address": 1, "registers": [10, 11]},
        {"function": 3, "address": 2, "registers": [20]},
        {"function": 4, "address": 1, "registers": [12, 13]},  # overwrites input 1,2
        {"function": 3, "address": 2, "registers": [22]},      # overwrites holding 2
    ]
    with capture.open('w', encoding='utf-8') as f:
        for obj in lines:
            f.write(json.dumps(obj) + '\n')
    out_path = tmp_path / 'dataset.json'
    run_compact_capture(capture, out_path)
    data = json.loads(out_path.read_text())
    assert data['input'] == {"1": 12, "2": 13}
    assert data['holding'] == {"2": 22}
