"""Small probe utility to read a few registers from the simulator.

Usage:
  python testing/probe_simulator.py --port 5034 --host 127.0.0.1
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from pymodbus.client import AsyncModbusTcpClient

# Ensure repository root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from testing.modbus_simulator import start_simulator  # type: ignore


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=5034)
    p.add_argument('--host', default='127.0.0.1')
    return p.parse_args()


async def run():
    args = parse_args()
    async with start_simulator(host=args.host, port=args.port):
        client = AsyncModbusTcpClient(args.host, port=args.port)
        await client.connect()
        for base, count, label in [(30, 10, 'holding'), (331, 2, 'holding'), (92, 6, 'input')]:
            fn = client.read_input_registers if label == 'input' else client.read_holding_registers
            resp = await fn(base, count=count, device_id=1)
            print(f"{label} {base}-{base+count-1}:", getattr(resp, 'registers', resp))
        client.close()


if __name__ == '__main__':  # pragma: no cover
    asyncio.run(run())
