"""Device defaults for a Growatt Inverter."""

from dataclasses import dataclass
from enum import StrEnum
from datetime import time

from .base import (
    GrowattDeviceRegisters,
    custom_function,
    process_export_power_limit_enable,
    process_export_power_limit_rate,
    FIRMWARE_REGISTER,
    DEVICE_TYPE_CODE_REGISTER,
    NUMBER_OF_TRACKERS_AND_PHASES_REGISTER,
    ATTR_INVERTER_ENABLED,
    ATTR_OUTPUT_POWER_LIMIT,
    ATTR_EXPORT_POWER_LIMIT_ENABLE,
    ATTR_EXPORT_POWER_LIMIT_RATE,
    ATTR_DISCHARGE_POWER_LIMIT_RATE,
    ATTR_CHARGE_POWER_LIMIT_RATE,
    ATTR_DISCHARGE_STOP_SOC_PERCENT_OFFGRID,
    ATTR_DISCHARGE_STOP_SOC_PERCENT_ONGRID,
    ATTR_CHARGE_STOP_SOC_PERCENT,
    ATTR_AC_CHARGE_ENABLED,
    ATTR_CHARGE_DISCHARGE_PERIOD_1,
    ATTR_CHARGE_DISCHARGE_PERIOD_2,
    ATTR_CHARGE_DISCHARGE_PERIOD_3,
    ATTR_CHARGE_DISCHARGE_PERIOD_4,
    ATTR_CHARGE_DISCHARGE_PERIOD_5,
    ATTR_CHARGE_DISCHARGE_PERIOD_6,
    ATTR_CHARGE_DISCHARGE_PERIOD_7,
    ATTR_CHARGE_DISCHARGE_PERIOD_8,
    ATTR_CHARGE_DISCHARGE_PERIOD_9,
    ATTR_INVERTER_MODEL,
    ATTR_MODBUS_VERSION,
    ATTR_SOC_PERCENTAGE,
    ATTR_DISCHARGE_POWER,
    ATTR_CHARGE_POWER,
    ATTR_POWER_TO_USER,
    ATTR_POWER_TO_GRID,
    ATTR_POWER_USER_LOAD,
    ATTR_ENERGY_TO_USER_TODAY,
    ATTR_ENERGY_TO_USER_TOTAL,
    ATTR_ENERGY_TO_GRID_TODAY,
    ATTR_ENERGY_TO_GRID_TOTAL,
    ATTR_DISCHARGE_ENERGY_TODAY,
    ATTR_DISCHARGE_ENERGY_TOTAL,
    ATTR_CHARGE_ENERGY_TODAY,
    ATTR_CHARGE_ENERGY_TOTAL,
    ATTR_SERIAL_NUMBER,
    ATTR_PAC_TO_GRID_TOTAL,
    ATTR_PAC_TO_USER_TOTAL,
    ATTR_PRIORITY_MODE,
)

MAXIMUM_DATA_LENGTH = 100

STORAGE_PRIORITY_MODE_CODES = {
    0: "Load First",
    1: "Battery First",
    2: "Grid First",
}

class ChargeDischargeMode(StrEnum):
    AUTO = "Auto"
    CHARGE = "Charge"
    DISCHARGE = "Discharge"

@dataclass
class ChargeDischargePeriodValue:
    enable: bool = False
    mode: ChargeDischargeMode = ChargeDischargeMode.AUTO
    start_time: time = time()
    end_time: time = time()

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

def process_priority_mode(value) -> str:
    return STORAGE_PRIORITY_MODE_CODES.get(value, "Invalid")

def process_charge_discharge_period(values: list[int]) -> ChargeDischargePeriodValue:
    enable = ((values[0] & 0x8000) >> 15) == 1
    mode_val = ((values[0] & 0x6000) >> 13)
    if mode_val == 2:
        mode = ChargeDischargeMode.DISCHARGE
    elif mode_val == 1:
        mode = ChargeDischargeMode.CHARGE
    else:
        mode = ChargeDischargeMode.AUTO
    start_time = time(((values[0] & 0x1F00) >> 8), (values[0] & 0x00FF))
    end_time = time(((values[1] & 0x1F00) >> 8), (values[1] & 0x00FF))
    return ChargeDischargePeriodValue(enable, mode, start_time, end_time)

def create_charge_discharge_period(charge_discharge_period: ChargeDischargePeriodValue) -> tuple[int, int]:
    reg_1 = charge_discharge_period.start_time.minute & 0x00FF
    reg_1 += (charge_discharge_period.start_time.hour << 8) & 0x1F00
    if charge_discharge_period.mode == ChargeDischargeMode.DISCHARGE:
        reg_1 += 2 << 13
    elif charge_discharge_period.mode == ChargeDischargeMode.CHARGE:
        reg_1 += 1 << 13
    if charge_discharge_period.enable:
        reg_1 += 1 << 15
    reg_2 = charge_discharge_period.end_time.minute & 0x00FF 
    reg_2 += (charge_discharge_period.end_time.hour << 8) & 0x1F00
    return reg_1, reg_2

SERIAL_NUMBER_REGISTER = GrowattDeviceRegisters(
    name=ATTR_SERIAL_NUMBER, register=3001, value_type=str, length=15
)

STORAGE_HOLDING_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_INVERTER_ENABLED,
        register=0,
        value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_POWER_LIMIT,
        register=3,
        value_type=int
    ),
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
    ),
    GrowattDeviceRegisters(
        name=ATTR_EXPORT_POWER_LIMIT_ENABLE,
        register=122,
        value_type=custom_function,
        function=process_export_power_limit_enable
    ),
    GrowattDeviceRegisters(
        name=ATTR_EXPORT_POWER_LIMIT_RATE,
        register=123,
        value_type=custom_function,
        function=process_export_power_limit_rate
    ),
)

STORAGE_HOLDING_REGISTERS_120_TL_XH: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_INVERTER_ENABLED,
        register=0,
        value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_POWER_LIMIT,
        register=3,
        value_type=int
    ),
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
    ),
    GrowattDeviceRegisters(
        name=ATTR_EXPORT_POWER_LIMIT_ENABLE,
        register=122,
        value_type=custom_function,
        function=process_export_power_limit_enable
    ),
    GrowattDeviceRegisters(
        name=ATTR_EXPORT_POWER_LIMIT_RATE,
        register=123,
        value_type=custom_function,
        function=process_export_power_limit_rate
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_POWER_LIMIT_RATE, register=3036, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_POWER_LIMIT_RATE, register=3047, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_STOP_SOC_PERCENT_OFFGRID, register=3037, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_STOP_SOC_PERCENT_ONGRID, register=3067, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_STOP_SOC_PERCENT, register=3048, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_AC_CHARGE_ENABLED, register=3049, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_1,
        register=3038,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_2,
        register=3040,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_3,
        register=3042,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_4,
        register=3044,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_5,
        register=3050,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_6,
        register=3052,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_7,
        register=3054,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_8,
        register=3056,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_DISCHARGE_PERIOD_9,
        register=3058,
        value_type=custom_function,
        length=2,
        function=process_charge_discharge_period
    ),
)

STORAGE_INPUT_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_PRIORITY_MODE, register=118, value_type=custom_function, function=process_priority_mode
    ),
    GrowattDeviceRegisters(
        name=ATTR_SOC_PERCENTAGE, register=1014, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_POWER, register=1009, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_POWER, register=1011, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_USER_TODAY, register=1044, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_USER_TOTAL, register=1046, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_GRID_TODAY, register=1048, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_GRID_TOTAL, register=1050, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TODAY, register=1052, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TOTAL, register=1054, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_ENERGY_TODAY, register=1056, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_ENERGY_TOTAL, register=1058, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_PAC_TO_USER_TOTAL, register=1021, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_PAC_TO_GRID_TOTAL, register=1029, value_type=float, length=2,
    ),
)

STORAGE_INPUT_REGISTERS_120_TL_XH: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_PRIORITY_MODE, register=3144, value_type=custom_function, function=process_priority_mode
    ),
    GrowattDeviceRegisters(
        name=ATTR_SOC_PERCENTAGE, register=3171, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_POWER, register=3178, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_POWER, register=3180, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_POWER_TO_USER, register=3041, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_POWER_TO_GRID, register=3043, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_POWER_USER_LOAD, register=3045, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_USER_TODAY, register=3067, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_USER_TOTAL, register=3069, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_GRID_TODAY, register=3071, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_ENERGY_TO_GRID_TOTAL, register=3073, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TODAY, register=3125, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TOTAL, register=3127, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_ENERGY_TODAY, register=3129, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_ENERGY_TOTAL, register=3131, value_type=float, length=2
    ),
)
