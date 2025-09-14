"""Test Modbus simulator register reads."""

import asyncio
import json
from pathlib import Path

import pytest
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer import FramerType

pytestmark = pytest.mark.enable_socket

DATASET_PATH = (
    Path(__file__).parent.parent / "testing" / "datasets" / "min_6000xh_tl.json"
)
UNIT_ID = 1


@pytest.mark.asyncio
async def test_simulator_register_reads():
    from testing.modbus_simulator import start_simulator
    import socket

    # Find free port
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()

    # Load expected values from dataset
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    expected = {int(k): int(v) for k, v in dataset["holding"].items()}

    address, value = next(iter(expected.items()))

    async with start_simulator(port=port, debug_wire=True) as (host, real_port):
        client = AsyncModbusTcpClient(
            host,
            port=real_port,
            framer=FramerType.SOCKET,
            reconnect_delay=0,
        )
        await client.connect()
        await asyncio.sleep(0.05)
        try:
            rr = await client.read_holding_registers(address - 1, count=1, device_id=1)
        finally:
            client.close()
    assert not rr.isError(), f"Read error at address {address}"
    read_val = rr.registers[0]
    assert read_val == value, (
        f"Mismatch at address {address}: got {read_val}, expected {value}"
    )
