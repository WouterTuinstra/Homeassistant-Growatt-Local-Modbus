"""
Python wrapper for getting data asynchronously from Growatt inverters
via serial usb RS232 connection and modbus RTU protocol.
"""
import json
import logging
import os
import sys
from abc import abstractmethod
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Any, Optional

from pymodbus.client import ModbusBaseClient
from pymodbus.client.serial import AsyncModbusSerialClient
from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.client.udp import AsyncModbusUdpClient
from pymodbus.framer import FramerType
from pymodbus.pdu import ModbusPDU

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
from .device_type.inverter_120 import MAXIMUM_DATA_LENGTH_120, HOLDING_REGISTERS_120, INPUT_REGISTERS_120, INPUT_REGISTERS_120_TL_XH
from .device_type.storage_120 import (
    STORAGE_HOLDING_REGISTERS_120,
    STORAGE_HOLDING_REGISTERS_120_TL_XH,
    STORAGE_INPUT_REGISTERS_120,
    STORAGE_INPUT_REGISTERS_120_TL_XH,
)
from .device_type.inverter_315 import MAXIMUM_DATA_LENGTH_315, HOLDING_REGISTERS_315, INPUT_REGISTERS_315
from .device_type.offgrid import INPUT_REGISTERS_OFFGRID, offgrid_status

from .exception import ModbusException, ModbusPortException
from .const import DeviceTypes
from .utils import (
    RegisterKeys,
    DeviceRegisters,
    get_keys_from_register,
    register_sequences,
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
            device_id: int
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
                await self.read_holding_registers(item[0], count=item[1], device_id=device_id)
            )

        results = process_registers(register, register_values)

        device_info = GrowattDeviceInfo(
            serial_number=results[ATTR_SERIAL_NUMBER].replace("\x00", ""),
            model=results[ATTR_INVERTER_MODEL],
            firmware=results[ATTR_FIRMWARE].replace("\x00", ""),
            mppt_trackers=results[ATTR_NUMBER_OF_TRACKERS_AND_PHASES][0],
            grid_phases=results[ATTR_NUMBER_OF_TRACKERS_AND_PHASES][1],
            modbus_version=results[ATTR_MODBUS_VERSION],
            device_type=results[ATTR_DEVICE_TYPE_CODE],
            device_type_code=register_values[43],
        )

        return device_info

    async def read_device_time(self, device_id: int):
        """
        Read Growatt device time.
        """
        # TODO: update with dynamic register values
        rhr = await self.client.read_holding_registers(45, count=6, device_id=device_id)
        if rhr.isError():
            _LOGGER.debug("Modbus read failed for rhr")
            raise ModbusException("Modbus read failed for rhr.")

        return datetime(
            rhr.registers[0] + 2000,
            rhr.registers[1],
            rhr.registers[2],
            rhr.registers[3],
            rhr.registers[4],
            rhr.registers[5],
        )

    async def write_device_time(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        device_id: int,
    ):
        """Writing current date/time to device."""
        # TODO: test if it works with current asyc libary
        # TODO: update with dynamic register values
        await self.client.write_register(45, year - 2000, device_id=device_id)
        await self.client.write_register(46, month, device_id=device_id)
        await self.client.write_register(47, day, device_id=device_id)
        await self.client.write_register(48, hour, device_id=device_id)
        await self.client.write_register(49, minute, device_id=device_id)
        await self.client.write_register(50, second, device_id=device_id)

    async def write_register(
        self, register: int, value: int | Sequence[int], device_id: int
    ) -> ModbusPDU:
        payload = ModbusBaseClient.convert_to_registers(
            value, ModbusBaseClient.DATATYPE.INT16
        )
        return await self.client.write_register(
            register, payload[0], device_id=device_id
        )

    async def read_holding_registers(self, start_address, count, device_id) -> dict[int, int]:
        data = await self.client.read_holding_registers(start_address, count=count, device_id=device_id)
        registers = {c: v for c, v in enumerate(data.registers, start_address)}
        return registers

    async def read_input_registers(self, start_address, count, device_id) -> dict[int, int]:
        data = await self.client.read_input_registers(start_address, count=count, device_id=device_id)
        registers = {c: v for c, v in enumerate(data.registers, start_address)}
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
                    framer=FramerType.RTU,
                    port=port,
                    timeout=timeout,
                    retries=retries,
                )
            else:
                self.client = AsyncModbusTcpClient(
                    host,
                    framer=FramerType.SOCKET,
                    port=port,
                    timeout=timeout,
                    retries=retries,
                )

        elif network_type.lower() == "udp":
            if frame.lower() == 'rtu':
                self.client = AsyncModbusUdpClient(
                    host,
                    framer=FramerType.RTU,
                    port=port,
                    timeout=timeout,
                    retries=retries,
                )
            else:
                self.client = AsyncModbusUdpClient(
                    host,
                    framer=FramerType.SOCKET,
                    port=port,
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
            framer=FramerType.RTU,
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

        self.device_registers = get_register_information(GrowattDeviceType)
        self.max_length = self.device_registers.max_length
        self.holding_register = self.device_registers.holding
        self.input_register = self.device_registers.input

        self.device_id = unit

    async def connect(self):
        await self.modbus.connect()

    def connected(self):
        return self.modbus.connected()

    def close(self):
        self.modbus.close()

    async def get_device_info(self) -> GrowattDeviceInfo:
        return await self.modbus.get_device_info(self.holding_register, self.max_length, self.device_id)

    async def sync_time(self) -> timedelta:
        device_time = await self.modbus.read_device_time(self.device_id)
        time = datetime.now()
        await self.modbus.write_device_time(
            time.year,
            time.month,
            time.day,
            time.hour,
            time.minute,
            time.second,
            self.device_id,
        )

        return time - device_time

    async def update(self, keys: RegisterKeys) -> dict[str, Any]:
        """
        Based on the given keys it will generate one or multiple requests to get the corrisponding results
        from both holding and input registers from the device.

        returns a dictionary of register name and value
        """
        if len(keys) == 0:
            return {}

        if (key_hash := hash(keys)) not in self._input_cache:
            key_sequences = register_sequences(keys, self.device_registers)
            self._input_cache[key_hash] = key_sequences
        else:
            key_sequences = self._input_cache[key_hash]

        results = {}

        if key_sequences.holding:
            register_values = {}
            for item in key_sequences.holding:
                register_values.update(
                    await self.modbus.read_holding_registers(item[0], item[1], self.device_id)
                )

            results.update(process_registers(self.device_registers.holding, register_values))

        if key_sequences.input:
            register_values = {}
            for item in key_sequences.input:
                register_values.update(
                    await self.modbus.read_input_registers(item[0], item[1], self.device_id)
                )

            results.update(process_registers(self.device_registers.input, register_values))

        return results

    async def write_register(
        self, register: int, payload: int | Sequence[int]
    ) -> ModbusPDU:
        _LOGGER.info(
            "Write register %s with payload %s and unit %s",
            register,
            payload,
            self.device_id,
        )
        data = await self.modbus.write_register(register, payload, self.device_id)
        _LOGGER.info("Write response done")
        return data

    async def read_holding_register(self, registers: tuple[GrowattDeviceRegisters, ...]) -> dict[str, Any]:
        _LOGGER.info("Read holding registers")
        register = {item.register: item for item in registers}
        key_sequences = keys_sequences(get_keys_from_register(register), self.max_length)
        register_values = {}

        for item in key_sequences:
            register_values.update(
                await self.modbus.read_holding_registers(item[0], item[1], self.device_id)
            )

        results = process_registers(register, register_values)
        _LOGGER.info("Read holding register response %s", json.dumps(results))
        return results

    def get_keys_by_name(self, names: Sequence[str]) -> RegisterKeys:
        if ATTR_STATUS in names:
            names = (*names, ATTR_STATUS_CODE, ATTR_FAULT_CODE, ATTR_DERATING_MODE)

        return RegisterKeys(
            holding={
                key
                for key, register in self.device_registers.holding.items()
                if register.name in names
            },
            input={
                key
                for key, register in self.device_registers.input.items()
                if register.name in names
            }
        )

    def get_input_register_by_name(self, name: str) -> Optional[GrowattDeviceRegisters]:
        for register in self.input_register.values():
            if register.name == name:
                return register

    def get_holding_register_by_name(self, name: str) -> Optional[GrowattDeviceRegisters]:
        for register in self.holding_register.values():
            if register.name == name:
                return register

    def get_register_names(self) -> set[str]:
        names = {register.name for register in self.input_register.values()}
        names.update({register.name for register in self.holding_register.values()})

        names.add(ATTR_STATUS)

        return names

    def status(self, value: dict[str, Any]):
        """
        Based on the various register values the status of the device can be determined.
        """
        if self.device == DeviceTypes.OFFGRID_SPF:
            return offgrid_status(value)

        return inverter_status(value)


def get_register_information(GrowattDeviceType: DeviceTypes) -> DeviceRegisters:
    if GrowattDeviceType in (DeviceTypes.INVERTER, DeviceTypes.INVERTER_315):
        max_length = MAXIMUM_DATA_LENGTH_315
        holding_register = {
            obj.register: obj for obj in HOLDING_REGISTERS_315
        }
        input_register = {
            obj.register: obj for obj in INPUT_REGISTERS_315
        }
    elif GrowattDeviceType == DeviceTypes.OFFGRID_SPF:
        max_length = MAXIMUM_DATA_LENGTH_315
        holding_register = {
            obj.register: obj for obj in HOLDING_REGISTERS_315
        }
        input_register = {
            obj.register: obj for obj in INPUT_REGISTERS_OFFGRID
        }
    elif GrowattDeviceType == DeviceTypes.INVERTER_120:
        max_length = MAXIMUM_DATA_LENGTH_120
        holding_register = {
            obj.register: obj for obj in HOLDING_REGISTERS_120
        }
        input_register = {
            obj.register: obj for obj in INPUT_REGISTERS_120
        }
    elif GrowattDeviceType == DeviceTypes.HYBRID_120:
        max_length = MAXIMUM_DATA_LENGTH_120
        holding_register = {
            obj.register: obj for obj in STORAGE_HOLDING_REGISTERS_120
        }
        input_register = {
            obj.register: obj for obj in INPUT_REGISTERS_120
        }
        input_register.update({
            obj.register: obj for obj in STORAGE_INPUT_REGISTERS_120
        })
    elif GrowattDeviceType == DeviceTypes.HYBRID_120_TL_XH:
        max_length = MAXIMUM_DATA_LENGTH_120
        holding_register = {
            obj.register: obj for obj in STORAGE_HOLDING_REGISTERS_120_TL_XH
        }
        input_register = {
            obj.register: obj for obj in INPUT_REGISTERS_120_TL_XH
        }
        input_register.update({
            obj.register: obj for obj in STORAGE_INPUT_REGISTERS_120_TL_XH
        })
    elif GrowattDeviceType == DeviceTypes.STORAGE_120:
        max_length = MAXIMUM_DATA_LENGTH_120
        holding_register = {
            obj.register: obj for obj in STORAGE_HOLDING_REGISTERS_120
        }
        input_register = {
            obj.register: obj for obj in STORAGE_INPUT_REGISTERS_120
        }
    else:
        raise TypeError("Unsupported Growatt device type")

    return DeviceRegisters(holding_register, input_register, max_length)


_PROTOCOL_120_DEVICE_TYPE_FAMILIES = {
    0x0100,
    0x0200,
    0x0300,
    0x0400,
    0x0500,
    0x0600,
    0x0700,
    0x0800,
    0x0900,
    0x0A00,
    0x0C00,
    0x1300,
    0x1500,
}


def _device_family_for_code(device_type_code: int) -> DeviceTypes | None:
    """Map known device-code families to the corresponding register layout."""

    family_code = device_type_code & 0xFF00
    if family_code == 0x1300:
        return DeviceTypes.HYBRID_120_TL_XH
    if family_code in {0x0C00, 0x1500}:
        return DeviceTypes.HYBRID_120
    if family_code == 0x0D00:
        return DeviceTypes.OFFGRID_SPF
    if family_code in _PROTOCOL_120_DEVICE_TYPE_FAMILIES:
        return DeviceTypes.INVERTER_120
    return None


def select_device_info(
    inverter_v120: GrowattDeviceInfo,
    inverter_v315: GrowattDeviceInfo,
) -> GrowattDeviceInfo | None:
    """Select a register-layout family using the device type code."""

    if inverter_v120.device_type_code is not None and (
        device_family := _device_family_for_code(inverter_v120.device_type_code)
    ) not in (None, DeviceTypes.OFFGRID_SPF):
        inverter_v120.device_family = device_family
        return inverter_v120

    if inverter_v315.device_type_code is not None and (
        device_family := _device_family_for_code(inverter_v315.device_type_code)
    ) == DeviceTypes.OFFGRID_SPF:
        inverter_v315.device_family = device_family
        return inverter_v315

    return None


async def get_device_info(device: GrowattModbusBase, unit: int, fixed_device_types: DeviceTypes | None = None) -> GrowattDeviceInfo | None:
    # Needs to determine minimal maximum length as all devices need to be able to support this
    minimal_length = min((MAXIMUM_DATA_LENGTH_120, MAXIMUM_DATA_LENGTH_315))

    if fixed_device_types is not None:
        if fixed_device_types in (DeviceTypes.INVERTER_120, DeviceTypes.HYBRID_120, 
                                  DeviceTypes.HYBRID_120_TL_XH, DeviceTypes.STORAGE_120):
            return await device.get_device_info(HOLDING_REGISTERS_120, minimal_length, unit)
        elif fixed_device_types in (DeviceTypes.INVERTER_315, DeviceTypes.OFFGRID_SPF):
            return await device.get_device_info(HOLDING_REGISTERS_315, minimal_length, unit)
        else:
            return None

    _LOGGER.info(f"Detected the following device info")
    inverter_v120 = await device.get_device_info(HOLDING_REGISTERS_120, minimal_length, unit)
    _LOGGER.info(f"Inverter Protocol v1.20: {inverter_v120}")

    inverter_v315 = await device.get_device_info(HOLDING_REGISTERS_315, minimal_length, unit)
    _LOGGER.info(f"Inverter Protocol v3.15: {inverter_v315}")

    if (device_info := select_device_info(inverter_v120, inverter_v315)):
        return device_info

    _LOGGER.warning(
        "Could not identify a supported register-layout family from device type "
        "code; select the protocol family explicitly."
    )
    return None
