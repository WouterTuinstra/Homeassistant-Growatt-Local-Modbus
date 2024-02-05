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

from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.framer.socket_framer import ModbusSocketFramer

from .device_type.base import (
    GrowattDeviceRegisters,
    GrowattDeviceInfo,
    ATTR_DEVICE_TYPE_CODE,
    ATTR_FIRMWARE,
    ATTR_INVERTER_MODEL,
    ATTR_MODBUS_VERSION,
    ATTR_NUMBER_OF_TRACKERS_AND_PHASES,
    ATTR_SERIAL_NUMBER,
    ATTR_STATUS,
    ATTR_DERATING_MODE,
    ATTR_FAULT_CODE,
    ATTR_STATUS_CODE,
    inverter_status,
)
from .device_type.inverter_120 import MAXIMUM_DATA_LENGTH_120, HOLDING_REGISTERS_120, INPUT_REGISTERS_120
from .device_type.inverter_315 import MAXIMUM_DATA_LENGTH_315, HOLDING_REGISTERS_315, INPUT_REGISTERS_315

from .exception import ModbusException, ModbusPortException
from .const import DeviceTypes
from .utils import (
    get_keys_from_register,
    get_all_keys_from_register,
    keys_sequences,
    process_registers,
    LRUCache
)


_LOGGER = logging.getLogger(__name__)


class GrowattModbusBase:
    client: ModbusBaseClient

    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Needs to be override by sub class")

    async def connect(self):
        """Connecting the modbus device."""
        await self.client.connect()

    def connected(self):
        return self.client.connected

    def close(self):
        """Closing the modbus device connection."""
        self.client.close()

    async def get_device_info(
            self,
            register: dict[int, GrowattDeviceRegisters] | tuple[GrowattDeviceRegisters, ...],
            max_length: int,
            unit: int
    ) -> GrowattDeviceInfo:
        """
        Read Growatt device information.
        """

        if isinstance(register, tuple):
            register = {item.register: item for item in register}

        key_sequences = keys_sequences(get_keys_from_register(register), max_length)

        register_values = {}

        for item in key_sequences:
            register_values.update(
                await self.read_holding_registers(start_index=item[0], length=item[1], unit=unit)
            )

        results = process_registers(register, register_values)

        device_info = GrowattDeviceInfo(
            serial_number=results[ATTR_SERIAL_NUMBER],
            model=results[ATTR_INVERTER_MODEL],
            firmware=results[ATTR_FIRMWARE],
            mppt_trackers=results[ATTR_NUMBER_OF_TRACKERS_AND_PHASES][0],
            grid_phases=results[ATTR_NUMBER_OF_TRACKERS_AND_PHASES][1],
            modbus_version=results[ATTR_MODBUS_VERSION],
            device_type=results[ATTR_DEVICE_TYPE_CODE]
        )

        return device_info

    async def read_device_time(self, unit: int):
        """
        Read Growatt device time.
        """
        # TODO: update with dynamic register values
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
        # TODO: test if it works with current asyc libary
        # TODO: update with dynamic register values
        await self.client.write_register(45, year - 2000)
        await self.client.write_register(46, month)
        await self.client.write_register(47, day)
        await self.client.write_register(48, hour)
        await self.client.write_register(49, minute)
        await self.client.write_register(50, second)

    async def read_holding_registers(self, start_index, length, unit) -> dict[int, int]:
        data = await self.client.read_holding_registers(start_index, length, unit)
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
        port: int = 502,
        frame: str = '',
        timeout: int = 3,
        retries: int = 3,
    ) -> None:
        """Initialize Network Growatt."""

        if network_type.lower() == "tcp":
            if frame.lower() == 'rtu':
                self.client = AsyncModbusTcpClient(
                    host,
                    port ,
                    framer=ModbusRtuFramer,
                    timeout=timeout,
                    retries=retries,
                )
            else:
                self.client = AsyncModbusTcpClient(
                    host,
                    port,
                    framer=ModbusSocketFramer,
                    timeout=timeout,
                    retries=retries,
                )

        elif network_type.lower() == "udp":
            if frame.lower() == 'rtu':
                self.client = AsyncModbusUdpClient(
                    host,
                    port,
                    framer=ModbusRtuFramer,
                    timeout=timeout,
                    retries=retries,
                )
            else:
                self.client = AsyncModbusUdpClient(
                    host,
                    port,
                    framer=ModbusSocketFramer,
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
    holding_register: dict[int, GrowattDeviceRegisters] = {}
    input_register: dict[int, GrowattDeviceRegisters] = {}
    max_length: int = 20

    def __init__(
        self,
        GrowattModbusClient: GrowattModbusBase,
        GrowattDeviceType: DeviceTypes,
        unit: int,
    ) -> None:
        self.modbus = GrowattModbusClient
        self.device = GrowattDeviceType
        self._input_cache = LRUCache(10)
        if GrowattDeviceType in (DeviceTypes.INVERTER, DeviceTypes.INVERTER_315):
            self.max_length = MAXIMUM_DATA_LENGTH_315
            self.holding_register = {
                obj.register: obj for obj in HOLDING_REGISTERS_315
            }
            self.input_register = {
                obj.register: obj for obj in INPUT_REGISTERS_315
            }
        elif GrowattDeviceType == DeviceTypes.INVERTER_120:
            self.max_length = MAXIMUM_DATA_LENGTH_120
            self.holding_register = {
                obj.register: obj for obj in HOLDING_REGISTERS_120
            }
            self.input_register = {
                obj.register: obj for obj in INPUT_REGISTERS_120
            }

        self.unit = unit

    async def connect(self):
        await self.modbus.connect()

    def connected(self):
        return self.modbus.connected()

    def close(self):
        self.modbus.close()

    async def get_device_info(self) -> GrowattDeviceInfo:
        return await self.modbus.get_device_info(self.holding_register, self.max_length, self.unit)

    async def sync_time(self) -> timedelta:
        device_time = await self.modbus.read_device_time(self.unit)
        time = datetime.now()
        await self.modbus.write_device_time(
            time.year, time.month, time.day, time.hour, time.minute, time.second
        )

        return time - device_time

    async def update(self, keys: set[int]) -> dict[str, Any]:
        """
        Based on the given keys it will generate one or multiple requests to get the corrisponding results
        from the input registers from the device.

        returns a dictionary of register name and value
        """
        if len(keys) == 0:
            return {}

        if (key_hash := hash(frozenset(keys))) not in self._input_cache:
            key_sequences = keys_sequences(get_all_keys_from_register(self.input_register, keys), self.max_length)
            self._input_cache[key_hash] = key_sequences
        else:
            key_sequences = self._input_cache[key_hash]

        register_values = {}

        for item in key_sequences:
            register_values.update(
                await self.modbus.read_input_registers(start_index=item[0], length=item[1], unit=self.unit)
            )

        return process_registers(self.input_register, register_values)

    def get_keys_by_name(self, names: Sequence[str]) -> set[int]:
        if ATTR_STATUS in names:
            names = (*names, ATTR_STATUS_CODE, ATTR_FAULT_CODE, ATTR_DERATING_MODE)

        return {
            key
            for key, register in self.input_register.items()
            if register.name in names
        }

    def get_register_names(self) -> set[str]:
        names = {register.name for register in self.input_register.values()}
        names.add(ATTR_STATUS)
        return names

    def status(self, value: dict[str, Any]):
        """
        Based on the various register values the status of the device can be determined.
        """
        if self.device in (DeviceTypes.INVERTER, DeviceTypes.INVERTER_315, DeviceTypes.INVERTER_120):
            return inverter_status(value)


async def get_device_info(device: GrowattModbusBase, unit: int, fixed_device_types: DeviceTypes | None = None) -> GrowattDeviceInfo | None:
    # Needs to determine minimal maximum length as all devices need to be able to support this
    minimal_length = min((MAXIMUM_DATA_LENGTH_120, MAXIMUM_DATA_LENGTH_315))

    if fixed_device_types is not None:
        if fixed_device_types == DeviceTypes.INVERTER_120:
            return await device.get_device_info(HOLDING_REGISTERS_120, minimal_length, unit)
        elif fixed_device_types == DeviceTypes.INVERTER_315:
            return await device.get_device_info(HOLDING_REGISTERS_315, minimal_length, unit)
        else:
            return None

    _LOGGER.info(f"Detected the following device info")
    inverter_v120 = await device.get_device_info(HOLDING_REGISTERS_120, minimal_length, unit)
    _LOGGER.info(f"Inverter Protocol v1.20: {inverter_v120}")

    inverter_v315 = await device.get_device_info(HOLDING_REGISTERS_315, minimal_length, unit)
    _LOGGER.info(f"Inverter Protocol v3.15: {inverter_v315}")

    if 1.0 < inverter_v120.modbus_version < 1.20:
        return inverter_v120
    elif 3.0 < inverter_v315.modbus_version < 3.15:
        return inverter_v315
    else:
        _LOGGER.warning(f"Inverter Modbus version not default supported.\nCheck full logs to get device information using the supported protocols.")
        return None
