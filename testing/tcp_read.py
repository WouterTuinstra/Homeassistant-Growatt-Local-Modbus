import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

HOST = "192.168.2.48"
PORT = 5021  # use 5020 if you mapped the primary port
UNIT = 1  # Modbus slave address on the inverter
START = 0  # first register to read
COUNT = 16  # how many registers to fetch


async def main():
    client = AsyncModbusTcpClient(host=HOST, port=PORT, timeout=3, retries=1)
    try:
        connected = await client.connect()
        if not connected or not client.connected:
            raise RuntimeError(f"Unable to connect to {HOST}:{PORT}")
        response = await client.read_holding_registers(
            START, count=COUNT, device_id=UNIT
        )
        if response.isError():
            raise ModbusException(response)
        print(f"Read {COUNT} registers starting at {START}:")
        for offset, value in enumerate(response.registers, START):
            print(f"  {offset:04d}: {value}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
