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
    ATTR_INPUT_3_VOLTAGE,
    ATTR_INPUT_3_AMPERAGE,
    ATTR_INPUT_3_POWER,
    ATTR_INPUT_3_ENERGY_TODAY,
    ATTR_INPUT_3_ENERGY_TOTAL,
    ATTR_INPUT_4_VOLTAGE,
    ATTR_INPUT_4_AMPERAGE,
    ATTR_INPUT_4_POWER,
    ATTR_INPUT_4_ENERGY_TODAY,
    ATTR_INPUT_4_ENERGY_TOTAL,
    ATTR_INPUT_5_VOLTAGE,
    ATTR_INPUT_5_AMPERAGE,
    ATTR_INPUT_5_POWER,
    ATTR_INPUT_5_ENERGY_TODAY,
    ATTR_INPUT_5_ENERGY_TOTAL,
    ATTR_INPUT_6_VOLTAGE,
    ATTR_INPUT_6_AMPERAGE,
    ATTR_INPUT_6_POWER,
    ATTR_INPUT_6_ENERGY_TODAY,
    ATTR_INPUT_6_ENERGY_TOTAL,
    ATTR_INPUT_7_VOLTAGE,
    ATTR_INPUT_7_AMPERAGE,
    ATTR_INPUT_7_POWER,
    ATTR_INPUT_7_ENERGY_TODAY,
    ATTR_INPUT_7_ENERGY_TOTAL,
    ATTR_INPUT_8_VOLTAGE,
    ATTR_INPUT_8_AMPERAGE,
    ATTR_INPUT_8_POWER,
    ATTR_INPUT_8_ENERGY_TODAY,
    ATTR_INPUT_8_ENERGY_TOTAL,
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
    ATTR_BOOST_TEMPERATURE,
    ATTR_P_BUS_VOLTAGE,
    ATTR_N_BUS_VOLTAGE,
    ATTR_OUTPUT_PERCENTAGE,
)




MAXIMUM_DATA_LENGTH_120 = 100


def model(registers) -> str:
    mo = (registers[0] << 16) + registers[1]
    return "A{:X} B{:X} D{:X} T{:X} P{:X} U{:X} M{:X} S{:X}".format(
        (mo & 0xF0000000) >> 28,
        (mo & 0x0F000000) >> 24,
        (mo & 0x00F00000) >> 20,
        (mo & 0x000F0000) >> 16,
        (mo & 0x0000F000) >> 12,
        (mo & 0x00000F00) >> 8,
        (mo & 0x000000F0) >> 4,
        (mo & 0x0000000F)
    )


HOLDING_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
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
        register=88,
        value_type=float,
        scale=100
    )
)

INPUT_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
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
        name=ATTR_INPUT_3_VOLTAGE, register=11, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_3_AMPERAGE, register=12, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_3_POWER, register=13, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_4_VOLTAGE, register=15, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_4_AMPERAGE, register=16, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_4_POWER, register=17, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_5_VOLTAGE, register=19, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_5_AMPERAGE, register=20, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_5_POWER, register=21, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_6_VOLTAGE, register=23, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_6_AMPERAGE, register=24, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_6_POWER, register=25, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_7_VOLTAGE, register=27, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_7_AMPERAGE, register=28, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_7_POWER, register=29, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_8_VOLTAGE, register=31, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_8_AMPERAGE, register=32, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_8_POWER, register=33, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_POWER, register=35, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_FREQUENCY, register=37, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_VOLTAGE, register=38, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_AMPERAGE, register=39, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_POWER, register=40, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_VOLTAGE, register=42, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_AMPERAGE, register=43, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_POWER, register=44, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_VOLTAGE, register=46, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_AMPERAGE, register=47, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_POWER, register=48, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TODAY, register=53, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TOTAL, register=55, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OPERATION_HOURS, register=57, value_type=float, length=2, scale=7200,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TODAY, register=59, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TOTAL, register=61, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TODAY, register=63, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TOTAL, register=65, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_3_ENERGY_TODAY, register=67, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_3_ENERGY_TOTAL, register=69, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_4_ENERGY_TODAY, register=71, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_4_ENERGY_TOTAL, register=73, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_5_ENERGY_TODAY, register=75, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_5_ENERGY_TOTAL, register=77, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_6_ENERGY_TODAY, register=79, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_6_ENERGY_TOTAL, register=81, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_7_ENERGY_TODAY, register=83, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_7_ENERGY_TOTAL, register=85, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_8_ENERGY_TODAY, register=87, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_8_ENERGY_TOTAL, register=89, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_ENERGY_TOTAL, register=91, value_type=float, length=2
    ),
    GrowattDeviceRegisters(name=ATTR_TEMPERATURE, register=93, value_type=float),
    GrowattDeviceRegisters(name=ATTR_IPM_TEMPERATURE, register=94, value_type=float),
    GrowattDeviceRegisters(name=ATTR_BOOST_TEMPERATURE, register=95, value_type=float),
    GrowattDeviceRegisters(name=ATTR_P_BUS_VOLTAGE, register=98, value_type=float),
    GrowattDeviceRegisters(name=ATTR_N_BUS_VOLTAGE, register=99, value_type=float),
    GrowattDeviceRegisters(name=ATTR_OUTPUT_PERCENTAGE, register=101, value_type=int),
    GrowattDeviceRegisters(name=ATTR_DERATING_MODE, register=104, value_type=int),
    GrowattDeviceRegisters(name=ATTR_FAULT_CODE, register=105, value_type=int),
    GrowattDeviceRegisters(
        name=ATTR_WARNING_CODE, register=110, value_type=int, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_POWER, register=234, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL, register=236, value_type=float, length=2,
    ),
)
