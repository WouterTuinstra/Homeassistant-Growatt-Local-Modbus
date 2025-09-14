"""
Test that the simulator responds correctly to pymodbus read requests for holding registers using GrowattNetwork.
Validates that values read match those in the min_6000xh_tl dataset.
"""

import asyncio
import pytest
from pymodbus.client import AsyncModbusTcpClient
import json
from pathlib import Path

DATASET_PATH = (
    Path(__file__).parent.parent / "testing" / "datasets" / "min_6000xh_tl.json"
)
SIM_HOST = "127.0.0.1"
SIM_PORT = 5020
UNIT_ID = 1


@pytest.mark.asyncio
async def test_simulator_register_reads():
    # Load expected values from dataset
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    expected = {int(k): int(v) for k, v in dataset["holding"].items()}

    # Connect to simulator
    client = AsyncModbusTcpClient(SIM_HOST, port=SIM_PORT)
    await client.connect()
    assert client.connected

    # Read and validate each register in dataset
    for address, value in expected.items():
        # Read one register at a time (unit ID assumed default 1)
        rr = await client.read_holding_registers(address, 1)
        assert not rr.isError(), f"Read error at address {address}"
        read_val = rr.registers[0]
        assert read_val == value, (
            f"Mismatch at address {address}: got {read_val}, expected {value}"
        )

    await client.close()
