"""Device defaults for a Growatt Inverter."""

from typing import Any
from enum import Enum
from .base import (
    GrowattDeviceRegisters,
    ATTR_STATUS_CODE,
    ATTR_DERATING_MODE,
    ATTR_FAULT_CODE,
    ATTR_WARNING_CODE,
    ATTR_WARNING_VALUE,
)

ATTR_SERIAL_NUMBER = "serial_number"
ATTR_MODEL_NUMBER = "model_number"
ATTR_FIRMWARE = "firmware"

ATTR_INPUT_POWER = "input_power"  # W
ATTR_INPUT_ENERGY_TOTAL = "input_energy_total"  # kWh

ATTR_INPUT_1_VOLTAGE = "input_1_voltage"  # V
ATTR_INPUT_1_AMPERAGE = "input_1_amperage"  # A
ATTR_INPUT_1_POWER = "input_1_power"  # W
ATTR_INPUT_1_ENERGY_TODAY = "input_1_energy_today"  # kWh
ATTR_INPUT_1_ENERGY_TOTAL = "input_1_energy_total"  # kWh

ATTR_INPUT_2_VOLTAGE = "input_2_voltage"  # V
ATTR_INPUT_2_AMPERAGE = "input_2_amperage"  # A
ATTR_INPUT_2_POWER = "input_2_power"  # W
ATTR_INPUT_2_ENERGY_TODAY = "input_2_energy_today"  # kWh
ATTR_INPUT_2_ENERGY_TOTAL = "input_2_energy_total"  # kWh

ATTR_OUTPUT_POWER = "output_power"  # W
ATTR_OUTPUT_ENERGY_TODAY = "output_energy_today"  # kWh
ATTR_OUTPUT_ENERGY_TOTAL = "output_energy_total"  # kWh

ATTR_OUTPUT_REACTIVE_POWER = "output_reactive_power"  # Var
ATTR_OUTPUT_REACTIVE_ENERGY_TODAY = "output_reactive_energy_today"  # kVarh
ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL = "output_reactive_energy_total"  # kVarh

ATTR_OUTPUT_1_VOLTAGE = "output_1_voltage"  # V
ATTR_OUTPUT_1_AMPERAGE = "output_1_amperage"  # A
ATTR_OUTPUT_1_POWER = "output_1_power"  # W

ATTR_OUTPUT_2_VOLTAGE = "output_2_voltage"  # V
ATTR_OUTPUT_2_AMPERAGE = "output_2_amperage"  # A
ATTR_OUTPUT_2_POWER = "output_2_power"  # W

ATTR_OUTPUT_3_VOLTAGE = "output_3_voltage"  # V
ATTR_OUTPUT_3_AMPERAGE = "output_3_amperage"  # A
ATTR_OUTPUT_3_POWER = "output_3_power"  # W

ATTR_OPERATION_HOURS = "operation_hours"  # s

ATTR_FREQUENCY = "frequency"  # Hz

ATTR_TEMPERATURE = "temperature"  # C
ATTR_IPM_TEMPERATURE = "ipm_temperature"  # C

ATTR_P_BUS_VOLTAGE = "p_bus_voltage"  # V
ATTR_N_BUS_VOLTAGE = "n_bus_voltage"  # V


class InverterStatus(Enum):
    "Enum of possible Inverter Status."
    Waiting = 0
    Normal = 1
    Fault = 3


INVERTER_FAULTCODES = {
    0: "None",
    24: "Auto Test Failed",
    25: "No AC Connection",
    26: "PV Isolation Low",
    27: "Residual I High",
    28: "Output High DCI",
    29: "PV Voltage High",
    30: "AC V Outrange",
    31: "AC F Outrange",
    32: "Module Hot",
}
for i in range(1, 24):
    INVERTER_FAULTCODES[i] = "Generic Error Code: %s" % str(99 + i)

INVERTER_WARNINGCODES = {
    0x0000: "None",
    0x0001: "Fan warning",
    0x0002: "String communication abnormal",
    0x0004: "StrPID config Warning",
    0x0008: "Fail to read EEPROM",
    0x0010: "DSP and COM firmware unmatch",
    0x0020: "Fail to write EEPROM",
    0x0040: "SPD abnormal",
    0x0080: "GND and N connect abnormal",
    0x0100: "PV1 or PV2 circuit short",
    0x0200: "PV1 or PV2 boost driver broken",
    0x0400: "",
    0x0800: "",
    0x1000: "",
    0x2000: "",
    0x4000: "",
    0x8000: "",
}

INVERTER_DERATINGMODES = {
    0: "No Deratring",
    1: "PV",
    3: "Vac",
    4: "Fac",
    5: "Tboost",
    6: "Tinv",
    7: "Control",
    8: "*LoadSpeed",
    9: "*OverBackByTime",
}

STATUS_REGISTER = GrowattDeviceRegisters(
    name=ATTR_STATUS_CODE, register=0, value_type=int
)
FAULT_REGISTER = GrowattDeviceRegisters(
    name=ATTR_FAULT_CODE, register=40, value_type=int
)
DERATING_REGISTER = GrowattDeviceRegisters(
    name=ATTR_DERATING_MODE, register=47, value_type=int
)


def inverter_status(value: dict[str, Any]) -> str:
    """Returns status based on multiple registery values."""
    if STATUS_REGISTER.name not in value.keys():
        return None

    status_value = InverterStatus(value[STATUS_REGISTER.name])

    if status_value is InverterStatus.Waiting:
        return status_value.name

    elif status_value == InverterStatus.Normal:
        derating = value.get(DERATING_REGISTER.name, None)
        if (
            derating is not None
            and derating in INVERTER_DERATINGMODES.keys()
            and derating != 0
        ):
            return f"{status_value.name} - {INVERTER_DERATINGMODES[derating]}"

        return status_value.name

    elif status_value is InverterStatus.Fault:
        fault = value.get(FAULT_REGISTER.name, None)
        if fault is not None and fault != 0:
            return f"{status_value.name} - {INVERTER_FAULTCODES[fault]}"


INVERTER_REGISTERS_TYPES: tuple[GrowattDeviceRegisters, ...] = (
    STATUS_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_INPUT_POWER, register=1, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_VOLTAGE,
        register=3,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_AMPERAGE,
        register=4,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_POWER,
        register=5,
        value_type=float,
        double_value=True,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_VOLTAGE,
        register=7,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_AMPERAGE,
        register=8,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_POWER, register=9, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_POWER, register=11, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_FREQUENCY, register=13, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_VOLTAGE,
        register=14,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_AMPERAGE,
        register=15,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_1_POWER, register=16, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_VOLTAGE,
        register=18,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_AMPERAGE,
        register=19,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_2_POWER, register=20, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_VOLTAGE,
        register=22,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_AMPERAGE,
        register=23,
        value_type=float,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_3_POWER, register=24, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TODAY, register=26, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_ENERGY_TOTAL, register=28, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OPERATION_HOURS,
        register=30,
        value_type=float,
        double_value=True,
        scale=7200,
    ),
    GrowattDeviceRegisters(name=ATTR_TEMPERATURE, register=32, value_type=float),
    FAULT_REGISTER,
    GrowattDeviceRegisters(name=ATTR_IPM_TEMPERATURE, register=41, value_type=float),
    GrowattDeviceRegisters(name=ATTR_P_BUS_VOLTAGE, register=42, value_type=float),
    GrowattDeviceRegisters(name=ATTR_N_BUS_VOLTAGE, register=43, value_type=float),
    DERATING_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TODAY, register=48, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_1_ENERGY_TOTAL, register=50, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TODAY, register=52, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_2_ENERGY_TOTAL, register=54, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_INPUT_ENERGY_TOTAL, register=56, value_type=float, double_value=True
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_POWER,
        register=58,
        value_type=float,
        double_value=True,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_ENERGY_TODAY,
        register=60,
        value_type=float,
        double_value=True,
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_ENERGY_TOTAL,
        register=62,
        value_type=float,
        double_value=True,
    ),
    GrowattDeviceRegisters(
        name=ATTR_WARNING_CODE, register=64, value_type=int, double_value=True
    ),
    GrowattDeviceRegisters(name=ATTR_WARNING_VALUE, register=65, value_type=int),
)
