"""Device defaults for a Growatt Offgrid Inverter SPF."""

from enum import Enum
from typing import Any
from .base import (
    GrowattDeviceRegisters,
    custom_function,
    ATTR_STATUS_CODE,
    ATTR_FAULT_CODE,
    ATTR_WARNING_CODE,
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
    ATTR_OPERATION_HOURS,
    ATTR_GRID_VOLTAGE,
    ATTR_GRID_FREQUENCY,
    ATTR_TEMPERATURE,
    ATTR_SOC_PERCENTAGE,
    ATTR_DISCHARGE_POWER,
    ATTR_CHARGE_POWER,
    ATTR_ACTIVE_POWER,
    ATTR_BATTERY_VOLTAGE,
    ATTR_BUS_VOLTAGE,
    ATTR_OUTPUT_1_VOLTAGE,
    ATTR_OUTPUT_1_AMPERAGE,
    ATTR_OUTPUT_FREQUENCY,
    ATTR_OUTPUT_DC_VOLTAGE,
    ATTR_DC_TEMPERATURE,
    ATTR_LOAD_PERCENTAGE,
    ATTR_CONSTANT_POWER,
    ATTR_BATTERY_P_VOLTAGE,
    ATTR_BATTERY_B_VOLTAGE,
    ATTR_BATTERY_DISCHARGE_AMPERAGE,
    ATTR_BATTERY_POWER,
    ATTR_CHARGE_ENERGY_TODAY,
    ATTR_CHARGE_ENERGY_TOTAL,
    ATTR_DISCHARGE_ENERGY_TODAY,
    ATTR_DISCHARGE_ENERGY_TOTAL,
    ATTR_AC_CHARGE_AMPERAGE,
    ATTR_AC_DISCHARGE_TODAY,
    ATTR_AC_DISCHARGE_TOTAL,
)


class OffgridStatus(Enum):
    "Enum of possible Offgrid Status."
    Stendby = 0
    Not_used = 1
    Discharge = 2
    Fault = 3
    PV_charge = 5
    AC_charge = 6
    Combined_charge = 7
    Combined_charge_bypass = 8
    PV_charge_bypass = 9
    AC_charge_bypass = 10
    Bypass = 11
    PV_charge_discharge = 12


OFFGRID_WARNINGCODES = {
    0x0001: "Battery voltage low warning",
    0x0002: "Over temprature warning",
    0x0004: "Over load warning",
    0x0008: "Fail to read EEPROM",
    0x0010: "Firmware version unmatch",
    0x0020: "Fail to write EEPROM",
    0x0040: "BMS warning",
    0x0080: "Li‐Battery over load warning",
    0x0100: "Li‐Battery aging warning",
    0x0200: "Fan lock warning",
    0x0400: "",
    0x0800: "",
    0x1000: "",
    0x2000: "",
    0x4000: "",
    0x8000: "",
}
OFFGRID_FAULTCODES = {
    0x00000001: "",
    0x00000002: "CPU A to B Communication error",
    0x00000004: "Battery sample inconsistent",
    0x00000008: "BUCK over current",
    0x00000010: "BMS communication fault",
    0x00000020: "Battery unnormal",
    0x00000040: "",
    0x00000080: "Battery voltage high",
    0x00000100: "Over temprature",
    0x00000200: "Over load",
    0x00000400: "",
    0x00000800: "",
    0x00001000: "",
    0x00002000: "",
    0x00004000: "",
    0x00008000: "",
    0x00010000: "Battery reverse connection",
    0x00020000: "BUS soft start fail",
    0x00040000: "DC‐DC unnormal",
    0x00080000: "DC voltage high",
    0x00100000: "CT detect failed",
    0x00200000: "CPU B to A Communication error",
    0x00400000: "BUS voltage high ",
    0x00800000: "",
    0x01000000: "MOV break",
    0x02000000: "Output short circuit",
    0x04000000: "Li‐Battery over load",
    0x08000000: "Output voltage high",
    0x10000000: "",
    0x20000000: "",
    0x40000000: "",
    0x80000000: "",
}


def offgrid_status(value: dict[str, Any]) -> str | None:
    """Returns status based on multiple registery values."""
    if ATTR_STATUS_CODE not in value.keys():
        return None

    status_value = OffgridStatus(value[ATTR_STATUS_CODE])

    if status_value is OffgridStatus.Fault:
        fault = value.get(ATTR_FAULT_CODE, None)
        if fault is not None and fault != 0:
            return f"{status_value.name} - {OFFGRID_FAULTCODES[fault]}"

    warning = value.get(ATTR_WARNING_CODE, None)
    if (warning is not None and warning in OFFGRID_WARNINGCODES.keys() and warning != 0):
        return f"{status_value.name} - {OFFGRID_WARNINGCODES[warning]}"

    return status_value.name


def batt_watt(registers) -> float:
   value = (registers[0] << 16) + registers[1]
   if (value & 0x80000000) == 0x80000000 :
      neg = ~0xFFFFFFFF
   else:
      neg = 0
   return round(float(-1 * int(neg + value)) / 10, 3)


INPUT_REGISTERS_OFFGRID: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_STATUS_CODE, register=0, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_VOLTAGE, register=1, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_VOLTAGE, register=2, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_POWER, register=3, value_type=float, length=2,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_POWER, register=5, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_AMPERAGE, register=7, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_AMPERAGE, register=8, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_ACTIVE_POWER, register=9, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_POWER, register=13, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_VOLTAGE, register=17, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_SOC_PERCENTAGE, register=18, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BUS_VOLTAGE, register=19, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_GRID_VOLTAGE, register=20, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_GRID_FREQUENCY, register=21, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_VOLTAGE, register=22, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_FREQUENCY, register=23, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_DC_VOLTAGE, register=24, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_TEMPERATURE, register=25, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_DC_TEMPERATURE, register=26, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_LOAD_PERCENTAGE, register=27, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_P_VOLTAGE, register=28, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_B_VOLTAGE, register=29, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OPERATION_HOURS, register=30, value_type=float, length=2, scale=7200,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_AMPERAGE, register=34, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_FAULT_CODE, register=42, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_WARNING_CODE, register=43, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_CONSTANT_POWER, register=47, value_type=int
    ),

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
        name=ATTR_CHARGE_ENERGY_TODAY, register=56, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_ENERGY_TOTAL, register=58, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TODAY, register=60, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_ENERGY_TOTAL, register=62, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_AC_DISCHARGE_TODAY, register=64, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_AC_DISCHARGE_TOTAL, register=66, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_AC_CHARGE_AMPERAGE, register=68, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_POWER, register=69, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_DISCHARGE_AMPERAGE, register=73, value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_POWER,
        register=77,
        value_type=custom_function,
        length=2,
        function=batt_watt
    )
)
