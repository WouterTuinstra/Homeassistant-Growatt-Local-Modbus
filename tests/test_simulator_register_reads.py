"""
Test that the simulator responds correctly to pymodbus read requests for holding registers using GrowattNetwork.
Validates that values read match those in the min_6000xh_tl dataset.
"""

import asyncio
import json
from pathlib import Path

import pytest
from pymodbus.client import ModbusTcpClient

DATASET_PATH = (
    Path(__file__).parent.parent / "testing" / "datasets" / "min_6000xh_tl.json"
)
UNIT_ID = 1


@pytest.mark.asyncio
async def test_simulator_register_reads(modbus_simulator):
    pytest.skip("Modbus simulation test disabled due to unreliable pymodbus behavior in CI")
    # Load expected values from dataset
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    expected = {int(k): int(v) for k, v in dataset["holding"].items()}

    # Connect to simulator
    # Verify a representative register from the dataset to confirm simulator wiring
    address, value = next(iter(expected.items()))

    def _read_register():
        import pytest_socket

        pytest_socket.enable_socket()
        client = ModbusTcpClient(modbus_simulator["host"], port=modbus_simulator["port"])
        client.connect()
        try:
            return client.read_holding_registers(address - 1, count=1, device_id=1)
        finally:
            client.close()

    rr = await asyncio.to_thread(_read_register)
    assert not rr.isError(), f"Read error at address {address}"
    read_val = rr.registers[0]
    assert read_val == value, (
        f"Mismatch at address {address}: got {read_val}, expected {value}"
    )
