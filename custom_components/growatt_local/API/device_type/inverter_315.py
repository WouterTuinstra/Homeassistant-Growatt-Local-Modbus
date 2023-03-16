"""Device defaults for a Growatt Inverter."""

from .base import (
    GrowattDeviceRegisters,
    custom_function,
    FIRMWARE_REGISTER,
    SERIAL_NUMBER_REGISTER,
    DEVICE_TYPE_CODE_REGISTER,
    NUMBER_OF_TRACKERS_AND_PHASES_REGISTER,
    ATTR_INVERTER_MODEL,
    ATTR_MODBUS_VERSION,
    ATTR_STATUS_CODE,
    ATTR_DERATING_MODE,
    ATTR_FAULT_CODE,
    ATTR_WARNING_CODE,
    ATTR_WARNING_VALUE,
    ATTR_INPUT_POWER,
    ATTR_INPUT_ENERGY_TOTAL,
    ATTR_INPUT_1_VOLTAGE,
    ATTR_INPUT_1_AMPERAGE,
    ATTR_INPUT_1_POWER,
    ATTR_INPUT_1_ENERGY_TODAY,
    ATTR_INPUT_1_ENERGY_TOTAL,
    ATTR_INPUT_2_VOLTAGE,
    ATTR_INPUT_2_AMPERAGE,
    ATTR_INPUT_2_POWER,
    ATTR_INPUT_2_ENERGY_TODAY,
    ATTR_INPUT_2_ENERGY_TOTAL,
    ATTR_OUTPUT_POWER,
    ATTR_OUTPUT_ENERGY_TODAY,
    ATTR_OUTPUT_ENERGY_TOTAL,
    ATTR_OUTPUT_REACTIVE_POWER,
    ATTR_OUTPUT_REACTIVE_ENERGY_TODAY,
    ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL,
    ATTR_OUTPUT_1_VOLTAGE,
    ATTR_OUTPUT_1_AMPERAGE,
    ATTR_OUTPUT_1_POWER,
    ATTR_OUTPUT_2_VOLTAGE,
    ATTR_OUTPUT_2_AMPERAGE,
    ATTR_OUTPUT_2_POWER,
    ATTR_OUTPUT_3_VOLTAGE,
    ATTR_OUTPUT_3_AMPERAGE,
    ATTR_OUTPUT_3_POWER,
    ATTR_OPERATION_HOURS,
    ATTR_FREQUENCY,
    ATTR_TEMPERATURE,
    ATTR_IPM_TEMPERATURE,
    ATTR_P_BUS_VOLTAGE,
    ATTR_N_BUS_VOLTAGE,
    ATTR_OUTPUT_PERCENTAGE,
)


MAXIMUM_DATA_LENGTH_315 = 45


def model(registers) -> str:
    mo = (registers[0] << 16) + registers[1]
    return "T{:X} Q{:X} P{:X} U{:X} M{:X} S{:X}".format(
        (mo & 0xF00000) >> 20,
        (mo & 0x0F0000) >> 16,
        (mo & 0x00F000) >> 12,
        (mo & 0x000F00) >> 8,
        (mo & 0x0000F0) >> 4,
        (mo & 0x00000F)
    )


HOLDING_REGISTERS_315: tuple[GrowattDeviceRegisters, ...] = (
    FIRMWARE_REGISTER,
    SERIAL_NUMBER_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_INVERTER_MODEL,
        register=28,
        value_type=custom_function,
        length=2,
        function=model
    ),
    DEVICE_TYPE_CODE_REGISTER,
    NUMBER_OF_TRACKERS_AND_PHASES_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_MODBUS_VERSION,
        register=73,
        value_type=float,
        scale=100
    )
)

INPUT_REGISTERS_315: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_STATUS_CODE, register=0, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_POWER, register=1, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_VOLTAGE, register=3, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_AMPERAGE, register=4, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_POWER, register=5, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_VOLTAGE, register=7, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_AMPERAGE, register=8, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_POWER, register=9, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_POWER, register=11, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_FREQUENCY, register=13, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_VOLTAGE, register=14, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_AMPERAGE, register=15, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_POWER, register=16, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_VOLTAGE, register=18, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_AMPERAGE, register=19, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_POWER, register=20, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_VOLTAGE, register=22, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_AMPERAGE, register=23, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_POWER, register=24, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TODAY, register=26, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TOTAL, register=28, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OPERATION_HOURS, register=30, value_type=float, length=2, scale=7200,
    ),
    GrowattDeviceRegisters(name=ATTR_TEMPERATURE, register=32, value_type=float),
    GrowattDeviceRegisters(name=ATTR_FAULT_CODE, register=40, value_type=int),
    GrowattDeviceRegisters(name=ATTR_IPM_TEMPERATURE, register=41, value_type=float),
    GrowattDeviceRegisters(name=ATTR_P_BUS_VOLTAGE, register=42, value_type=float),
    GrowattDeviceRegisters(name=ATTR_N_BUS_VOLTAGE, register=43, value_type=float),
    GrowattDeviceRegisters(name=ATTR_DERATING_MODE, register=47, value_type=int),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TODAY, register=48, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TOTAL, register=50, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TODAY, register=52, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TOTAL, register=54, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_ENERGY_TOTAL, register=56, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_POWER, register=58, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_ENERGY_TODAY, register=60, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL, register=62, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_WARNING_CODE, register=64, value_type=int
    ),
    GrowattDeviceRegisters(name=ATTR_WARNING_VALUE, register=65, value_type=int),
    GrowattDeviceRegisters(name=ATTR_OUTPUT_PERCENTAGE, register=66, value_type=int),
)
