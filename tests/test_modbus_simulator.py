import asyncio
import socket
import importlib
import types
import sys
import json
from pathlib import Path

import pytest
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer import FramerType

from testing.modbus_simulator import start_simulator

pytestmark = pytest.mark.enable_socket


@pytest.mark.asyncio
async def test_positional_port_and_custom_host():
    # Find a free port first
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    async with start_simulator(port, host="127.0.0.1") as (host, real_port):
        assert real_port == port
        assert host == "127.0.0.1"
        client = AsyncModbusTcpClient(host, port=real_port, framer=FramerType.SOCKET, reconnect_delay=0)
        await client.connect()
        # Brief sleep to ensure server task fully entered serve loop
        await asyncio.sleep(0.05)
        rr = await client.read_input_registers(0, count=2)
        assert not rr.isError()
        assert rr.registers == [1, 2]
    client.close()


@pytest.mark.asyncio
async def test_default_dataset_values():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    async with start_simulator(port) as (host, real_port):
        client = AsyncModbusTcpClient(host, port=real_port, framer=FramerType.SOCKET, reconnect_delay=0)
        await client.connect()
        await asyncio.sleep(0.05)
        rr = await client.read_input_registers(0, count=2)
        assert not rr.isError()
        assert rr.registers == [1, 2]
    client.close()


@pytest.mark.asyncio
async def test_mutation_plugin_application(tmp_path, monkeypatch):
    # Create a temporary module acting as a mutator
    mod_path = tmp_path / "temp_mutator.py"
    mod_path.write_text(
        "tick_values = []\n"
        "def mutate(registers, tick):\n"
        "    # Increment register 1 each tick starting from existing value\n"
        "    registers['input'][1] = registers['input'].get(1, 0) + 10\n"
        "    tick_values.append(registers['input'][1])\n"
    )
    sys.path.insert(0, str(tmp_path))
    try:
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        async with start_simulator(port, mutators=["temp_mutator"]) as (host, real_port):
            client = AsyncModbusTcpClient(host, port=real_port, framer=FramerType.SOCKET, reconnect_delay=0)
            await client.connect()
            # Read initial value after first tick sleep (~0.05s in ctx + <1s before first loop)
            await asyncio.sleep(1.2)
            # Address 0 maps to our seeded register 1 which the mutator increments
            rr1 = await client.read_input_registers(0, count=1)
            first = rr1.registers[0]
            await asyncio.sleep(1.1)
            rr2 = await client.read_input_registers(0, count=1)
            second = rr2.registers[0]
            assert second > first >= 10  # mutated at least once
            client.close()
        temp_mod = importlib.import_module("temp_mutator")
        assert len(temp_mod.tick_values) >= 2
    finally:
        if str(tmp_path) in sys.path:
            sys.path.remove(str(tmp_path))


@pytest.mark.asyncio
async def test_strict_defs_ignores_extra_dataset(tmp_path):
    # Create a minimal dataset with an extra register not in defs
    dataset = {"input": {"9999": 123}, "holding": {}}
    dataset_path = tmp_path / "ds.json"
    dataset_path.write_text(json.dumps(dataset))
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    async with start_simulator(port, dataset=str(dataset_path), strict_defs=True) as (host, real_port):
        client = AsyncModbusTcpClient(host, port=real_port, framer=FramerType.SOCKET, reconnect_delay=0)
        await client.connect()
        # 9999 should not exist (not in definition); reading should give 0 or error
        rr = await client.read_input_registers(9999, count=1)
        if not rr.isError():
            assert rr.registers[0] == 0
    client.close()
