"""Test Modbus simulator register reads."""

import asyncio
import json
from pathlib import Path

import pytest
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.framer import FramerType

from .serial_helpers import virtual_serial_pair

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
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()

    # Load expected values from dataset
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    expected = {int(k): int(v) & 0xFFFF for k, v in dataset["holding"].items()}

    ranges = [
        (0, 124),  # core input block
        (3000, 3124),  # mirror of low range
        (3125, 3199),  # battery energy counters
        (3200, 3231),  # BMS diagnostics
        (3232, 3374),  # remaining TL-XH block / reserved
    ]

    async with start_simulator(
        port=port, debug_wire=True, force_deterministic=True
    ) as (host, real_port):
        client = AsyncModbusTcpClient(
            host,
            port=real_port,
            framer=FramerType.SOCKET,
            reconnect_delay=0,
        )
        await client.connect()
        await asyncio.sleep(0.05)
        try:
            # First: test every register individually
            for start, end in ranges:
                for addr in range(start, end + 1):
                    # rr = await client.read_holding_registers(addr, 1, device_id=1)
                    rr = await client.read_holding_registers(addr, count=1, device_id=1)
                    assert not rr.isError(), f"Read error at address {addr}"
                    reg_val = rr.registers[0]
                    expected_val = expected.get(addr, 0)

                    # @agent (DEBUG_REPORT.md) : when commenting out the next line,
                    # communication gets lost after a certain amount of reads.
                    # with line as is, a mismatch is reported, which is another problem
                    # alltogether that has to be investigated separately.
                    # First problem is to make sure we can read all registers without
                    # communication loss.
                    assert reg_val == expected_val, (
                        f"Mismatch at address {addr}: got {reg_val}, expected {expected_val}"
                    )
            # Second: test block reads for each range
            for start, end in ranges:
                total = end - start + 1
                offset = start
                while total > 0:
                    chunk = min(total, 125)
                    rr = await client.read_holding_registers(
                        offset, count=chunk, device_id=1
                    )
                    assert not rr.isError(), (
                        f"Read error at range {offset}-{offset + chunk - 1}"
                    )
                    for i, reg_val in enumerate(rr.registers):
                        addr = offset + i
                        expected_val = expected.get(addr, 0)
                        assert reg_val == expected_val, (
                            f"Mismatch at address {addr}: got {reg_val}, expected {expected_val}"
                        )
                    offset += chunk
                    total -= chunk
        finally:
            client.close()


@pytest.mark.asyncio
async def test_simulator_register_reads_serial():
    from testing.modbus_simulator import start_simulator

    # Load expected values from dataset
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    expected = {int(k): int(v) & 0xFFFF for k, v in dataset["holding"].items()}

    ranges = [
        (0, 124),
        (3000, 3124),
        (3125, 3199),
        (3200, 3231),
        (3232, 3374),
    ]

    async with virtual_serial_pair() as (sim_port, client_port):
        async with start_simulator(
            mode="serial",
            serial_port=sim_port,
            debug_wire=True,
            force_deterministic=True,
        ):
            client = AsyncModbusSerialClient(
                client_port,
                framer=FramerType.RTU,
                baudrate=9600,
                stopbits=1,
                bytesize=8,
                parity="N",
                timeout=1,
                reconnect_delay=0,
            )
            await client.connect()
            await asyncio.sleep(0.1)
            try:
                for start, end in ranges:
                    for addr in range(start, end + 1):
                        rr = await client.read_holding_registers(
                            addr, count=1, device_id=UNIT_ID
                        )
                        assert not rr.isError(), f"Read error at address {addr}"
                        reg_val = rr.registers[0]
                        expected_val = expected.get(addr, 0)
                        assert reg_val == expected_val, (
                            f"Mismatch at address {addr}: got {reg_val}, expected {expected_val}"
                        )
                for start, end in ranges:
                    total = end - start + 1
                    offset = start
                    while total > 0:
                        chunk = min(total, 125)
                        rr = await client.read_holding_registers(
                            offset, count=chunk, device_id=UNIT_ID
                        )
                        assert not rr.isError(), (
                            f"Read error at range {offset}-{offset + chunk - 1}"
                        )
                        for i, reg_val in enumerate(rr.registers):
                            addr = offset + i
                            expected_val = expected.get(addr, 0)
                            assert reg_val == expected_val, (
                                f"Mismatch at address {addr}: got {reg_val}, expected {expected_val}"
                            )
                        offset += chunk
                        total -= chunk
            finally:
                client.close()
