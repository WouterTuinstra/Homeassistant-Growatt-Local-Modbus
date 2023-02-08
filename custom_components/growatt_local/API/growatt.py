"""
Python wrapper for getting data asynchronously from Growatt inverters
via serial usb RS232 connection and modbus RTU protocol.
"""
from abc import abstractmethod
import logging
import os
import sys
import asyncio


from datetime import datetime, timedelta
from typing import Any
from collections.abc import Sequence, Set


from pymodbus.client import ModbusBaseClient
from pymodbus.client.serial import AsyncModbusSerialClient
from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.client.udp import AsyncModbusUdpClient

from pymodbus.constants import Defaults
from pymodbus.framer.rtu_framer import ModbusRtuFramer

from .device_type.base import (
    ATTR_STATUS,
    ATTR_DERATING_MODE,
    ATTR_FAULT_CODE,
    ATTR_STATUS_CODE,
)
from .device_type.inverter import INVERTER_REGISTERS_TYPES, inverter_status

from .exception import ModbusException, ModbusPortException
from .const import DeviceTypes


def rchr(rr, index, end=None):
    """Read and convert to ASCII."""
    string = ""
    if end is None:
        end = index
    for i in range(index, end + 1):
        string += chr(rr.registers[i] >> 8)
        string += chr(rr.registers[i] & 0x000000FF)

    return string


_LOGGER = logging.getLogger(__name__)


class GrowattModbusBase:
    client: ModbusBaseClient
    device_info: tuple[str, str, str] = None

    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Needs to be override by sub class")

    async def connect(self):
        """Connecting the modbus device."""
        await self.client.connect()

    def connected(self):
        return self.client.connected

    async def close(self):
        """Closing the modbus device connection."""
        await self.client.close()

    async def get_device_info(self, unit: int) -> tuple[str, str, str]:
        """
        Read Growatt device information.
        """

        if self.device_info is not None:
            return self.device_info

        # Assuming the serial number doesn't change, it is read only once
        rhr = await self.client.read_holding_registers(0, 30, slave=unit)
        if rhr.isError():
            self.client.close()
            _LOGGER.debug("Modbus read failed for rhr")
            raise ModbusException("Modbus read failed for rhr.")

        firmware = rchr(rhr, 9, 14)

        serial_number = rchr(rhr, 23, 27)

        mo = (rhr.registers[28] << 16) + rhr.registers[29]
        model_number = (
            "T"
            + str((mo & 0xF00000) >> 20)
            + " Q"
            + str((mo & 0x0F0000) >> 16)
            + " P"
            + str((mo & 0x00F000) >> 12)
            + " U"
            + str((mo & 0x000F00) >> 8)
            + " M"
            + str((mo & 0x0000F0) >> 4)
            + " S"
            + str((mo & 0x00000F))
        )

        self.device_info = (serial_number, model_number, firmware)

        _LOGGER.debug(
            "GrowattRS232 with serial number %s is model %s and has firmware %s",
            *self.device_info,
        )

        return self.device_info

    async def read_device_time(self, unit: int):
        """
        Read Growatt device time.
        """

        # Assuming the serial number doesn't change, it is read only once
        rhr = await self.client.read_holding_registers(45, 6, slave=unit)
        if rhr.isError():
            _LOGGER.debug("Modbus read failed for rhr")
            raise ModbusException("Modbus read failed for rhr.")

        return datetime(
            rhr.register[0] + 2000,
            rhr.register[1],
            rhr.register[2],
            rhr.register[3],
            rhr.register[4],
            rhr.register[5],
        )

    async def write_device_time(
        self, year: int, month: int, day: int, hour: int, minute: int, second: int
    ):
        """Writing current date/time to device."""
        # doesn't work with asyc libary
        await self.client.write_register(45, year - 2000)
        await self.client.write_register(46, month)
        await self.client.write_register(47, day)
        await self.client.write_register(48, hour)
        await self.client.write_register(49, minute)
        await self.client.write_register(50, second)

    async def read_holding_registers(self, start_index, length, unit) -> dict[int, int]:
        data = await self.client.read_input_registers(start_index, length, unit)
        registers = {c: v for c, v in enumerate(data.registers, start_index)}
        return registers

    async def read_input_registers(self, start_index, length, unit) -> dict[int, int]:
        data = await self.client.read_input_registers(start_index, length, unit)
        registers = {c: v for c, v in enumerate(data.registers, start_index)}
        return registers


class GrowattNetwork(GrowattModbusBase):
    def __init__(
        self,
        network_type: str,
        host: str,
        port: int = None,
        timeout: int = Defaults.Timeout,
        retries: int = Defaults.Retries,
    ) -> None:
        """Initialize Network Growatt."""

        if network_type.lower() == "tcp":
            self.client = AsyncModbusTcpClient(
                host,
                port if port else Defaults.TcpPort,
                framer=ModbusRtuFramer,
                timeout=timeout,
                retries=retries,
            )

        elif network_type.lower() == "udp":
            self.client = AsyncModbusUdpClient(
                host,
                port if port else Defaults.UdpPort,
                framer=ModbusRtuFramer,
                timeout=timeout,
                retries=retries,
            )
        else:
            raise ModbusPortException("Unsuported network type defined")


class GrowattSerial(GrowattModbusBase):
    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        stopbits: int = 1,
        parity: str = "N",
        bytesize: int = 8,
        timeout: int = 3,
    ) -> None:
        """Initialize Serial Growatt."""

        if sys.platform.startswith("win"):
            if not port.startswith("COM"):
                _LOGGER.debug(
                    "Port %s is not available on windows platfrom should always start with 'COM'",
                    port,
                )
                raise ModbusPortException(
                    f"Port {port} is not available on windows platfrom should always start with 'COM'"
                )
        else:
            if not os.path.exists(port):
                _LOGGER.debug("Port %s is not available", port)
                raise ModbusPortException(f"USB port {port} is not available")

        self.client = AsyncModbusSerialClient(
            port=port,
            framer=ModbusRtuFramer,
            baudrate=baudrate,
            stopbits=stopbits,
            parity=parity[:1],
            bytesize=bytesize,
            timeout=timeout,
        )


class GrowattDevice:
    def __init__(
        self,
        GrowattModbusClient: GrowattModbusBase,
        GrowattDeviceType: DeviceTypes,
        unit: int,
    ) -> None:
        self.modbus = GrowattModbusClient
        self.device = GrowattDeviceType
        if GrowattDeviceType == DeviceTypes.INVERTER:
            self.register_lookup = {
                obj.register: obj for obj in INVERTER_REGISTERS_TYPES
            }
        self.unit = unit

    async def connect(self):
        await self.modbus.connect()

    def connected(self):
        return self.modbus.connected()

    async def close(self):
        await self.modbus.close()

    async def get_device_into(self) -> tuple[str, str, str]:
        return await self.modbus.get_device_info()

    async def sync_time(self) -> timedelta:
        device_time = await self.modbus.read_device_time()
        time = datetime.now()
        await self.modbus.write_device_time(
            time.year, time.month, time.day, time.hour, time.minute, time.second
        )

        return time - device_time

    async def update(self, keys: Sequence[int]) -> dict[str, Any]:
        if len(keys) == 0:
            return

        key = min(keys)
        maximum_key = max(keys)
        key_seperation = []
        while key < maximum_key:
            end_of_sequence = max([k for k in keys if k <= key + 43])

            double_value = self.register_lookup[end_of_sequence].double_value

            key_seperation.append((key, end_of_sequence + double_value + 1 - key))

            if end_of_sequence == maximum_key:
                break

            key = min([k for k in keys if k > end_of_sequence])

        register_values = {}
        result: dict[str, Any] = {}

        for item in key_seperation:
            register_values.update(
                await self.modbus.read_input_registers(*item, self.unit)
            )

        for key in keys:
            value = register_values.get(key, None)

            if value is None:
                continue

            register = self.register_lookup.get(key)

            if register.value_type == int:
                result[register.name] = value

            elif register.value_type == float and register.double_value:
                second_value = register_values.get(key + 1, None)

                if second_value is None:
                    continue

                result[register.name] = round(
                    float((value << 16) + second_value) / register.scale, 3
                )

            elif register.value_type == float:
                result[register.name] = round(float(value) / register.scale, 3)

        return result

    def get_keys_by_name(self, names: Sequence[str]) -> Set[int]:
        if ATTR_STATUS in names:
            names = {*names, ATTR_STATUS_CODE, ATTR_FAULT_CODE, ATTR_DERATING_MODE}

        return {
            key
            for key, register in self.register_lookup.items()
            if register.name in names
        }

    def status(self, value):
        if self.device is DeviceTypes.INVERTER:
            return inverter_status(value)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    server = GrowattSerial("COM10", timeout=10)
    # server = GrowattNetwork('TCP', 'localhost')

    test = GrowattDevice(server, INVERTER_REGISTERS_TYPES, 1)

    loop.run_until_complete(test.connect())

    loop.run_until_complete(test.update([0, 1]))

    loop.run_until_complete(test.close())
