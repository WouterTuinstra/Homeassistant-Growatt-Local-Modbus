import asyncio
import contextlib
import json
from pathlib import Path
from contextlib import asynccontextmanager

from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext, ModbusSequentialDataBlock
from pymodbus.server import ModbusTcpServer

BASE_PATH = Path(__file__).parent


def _load_registers(filename: str) -> dict[int, int]:
    with open(BASE_PATH / filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    registers: dict[int, int] = {}
    for item in data:
        number = int(item["number"])
        length = int(item.get("length", 1))
        for offset in range(length):
            registers[number + offset] = number + offset
    return registers


@asynccontextmanager
async def start_simulator(port: int = 5020):
    """Start a Modbus TCP simulator serving predefined registers."""
    holding = _load_registers("holding_min.json")
    input_ = _load_registers("input_min.json")

    max_hr = max(holding.keys(), default=0)
    max_ir = max(input_.keys(), default=0)

    hr_values = [0] * (max_hr + 1)
    ir_values = [0] * (max_ir + 1)
    for addr, val in holding.items():
        hr_values[addr] = val
    for addr, val in input_.items():
        ir_values[addr] = val

    store = ModbusDeviceContext(
        hr=ModbusSequentialDataBlock(0, hr_values),
        ir=ModbusSequentialDataBlock(0, ir_values),
    )
    context = ModbusServerContext(store, single=True)

    server = ModbusTcpServer(context, address=("127.0.0.1", port))
    task = asyncio.create_task(server.serve_forever())
    await asyncio.sleep(0.1)
    try:
        yield ("127.0.0.1", port)
    finally:
        await server.shutdown()
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
