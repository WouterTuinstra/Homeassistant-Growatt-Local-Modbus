from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

# Attribute names for values in the holding register

ATTR_FIRMWARE = "firmware"
ATTR_SERIAL_NUMBER = "serial number"
ATTR_INVERTER_MODEL = "Inverter model"

ATTR_DEVICE_TYPE_CODE = "device type code"
ATTR_NUMBER_OF_TRACKERS_AND_PHASES = "number of trackers and phases"

ATTR_MODBUS_VERSION = "modbus version"

# Attribute names for values in the input register

ATTR_STATUS = "status"
ATTR_STATUS_CODE = "status_code"
ATTR_DERATING_MODE = "derating_mode"
ATTR_FAULT_CODE = "fault_code"
ATTR_WARNING_CODE = "warning_code"
ATTR_WARNING_VALUE = "warning_value"

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

ATTR_INPUT_3_VOLTAGE = "input_3_voltage"  # V
ATTR_INPUT_3_AMPERAGE = "input_3_amperage"  # A
ATTR_INPUT_3_POWER = "input_3_power"  # W
ATTR_INPUT_3_ENERGY_TODAY = "input_3_energy_today"  # kWh
ATTR_INPUT_3_ENERGY_TOTAL = "input_3_energy_total"  # kWh

ATTR_INPUT_4_VOLTAGE = "input_4_voltage"  # V
ATTR_INPUT_4_AMPERAGE = "input_4_amperage"  # A
ATTR_INPUT_4_POWER = "input_4_power"  # W
ATTR_INPUT_4_ENERGY_TODAY = "input_4_energy_today"  # kWh
ATTR_INPUT_4_ENERGY_TOTAL = "input_4_energy_total"  # kWh

ATTR_INPUT_5_VOLTAGE = "input_5_voltage"  # V
ATTR_INPUT_5_AMPERAGE = "input_5_amperage"  # A
ATTR_INPUT_5_POWER = "input_5_power"  # W
ATTR_INPUT_5_ENERGY_TODAY = "input_5_energy_today"  # kWh
ATTR_INPUT_5_ENERGY_TOTAL = "input_5_energy_total"  # kWh

ATTR_INPUT_6_VOLTAGE = "input_6_voltage"  # V
ATTR_INPUT_6_AMPERAGE = "input_6_amperage"  # A
ATTR_INPUT_6_POWER = "input_6_power"  # W
ATTR_INPUT_6_ENERGY_TODAY = "input_6_energy_today"  # kWh
ATTR_INPUT_6_ENERGY_TOTAL = "input_6_energy_total"  # kWh

ATTR_INPUT_7_VOLTAGE = "input_7_voltage"  # V
ATTR_INPUT_7_AMPERAGE = "input_7_amperage"  # A
ATTR_INPUT_7_POWER = "input_7_power"  # W
ATTR_INPUT_7_ENERGY_TODAY = "input_7_energy_today"  # kWh
ATTR_INPUT_7_ENERGY_TOTAL = "input_7_energy_total"  # kWh

ATTR_INPUT_8_VOLTAGE = "input_8_voltage"  # V
ATTR_INPUT_8_AMPERAGE = "input_8_amperage"  # A
ATTR_INPUT_8_POWER = "input_8_power"  # W
ATTR_INPUT_8_ENERGY_TODAY = "input_8_energy_today"  # kWh
ATTR_INPUT_8_ENERGY_TOTAL = "input_8_energy_total"  # kWh

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

ATTR_TEMPERATURE = "inverter_temperature"  # C
ATTR_IPM_TEMPERATURE = "ipm_temperature"  # C
ATTR_BOOST_TEMPERATURE = "boost_temperature"  # C

ATTR_P_BUS_VOLTAGE = "p_bus_voltage"  # V
ATTR_N_BUS_VOLTAGE = "n_bus_voltage"  # V

ATTR_OUTPUT_PERCENTAGE = "real_output_power_percent"  # %


class custom_function(type):
    """
    Object to be used as value_type in a `GrowattDeviceRegisters` that require custom function to translate the register value.
    """
    pass


@dataclass
class GrowattDeviceRegisters:
    """Dataclass object to define register value for Growatt devices using modbus."""

    name: str
    register: int
    value_type: type
    length: int = 1
    scale: int = 10
    function: Callable | None = None


@dataclass
class GrowattDeviceInfo:
    serial_number: str
    model: str
    firmware: str
    mppt_trackers: int
    grid_phases: int
    modbus_version: float
    device_type: str = ""


DEVICE_TYPE_CODES = {
    0x100: "1 tracker and 1phase Grid connect PV inverter TL",
    0x200: "2 tracker and 1phase Grid connect PV inverter TL",
    0x300: "1 tracker and 1phase Grid connect PV inverter HF",
    0x400: "2 tracker and 1phase Grid connect PV inverter HF",
    0x500: "1 tracker and 1phase Grid connect PV inverter LF",
    0x600: "2 tracker and 1phase Grid connect PV inverter LF",
    0x700: "1 tracker and 3phase Grid connect PV inverter TL",
    0x800: "2 tracker and 3phase Grid connect PV inverter TL",
    0x900: "1 tracker and 3phase Grid connect PV inverter LF",
    0xA00: "2 tracker and 3phase Grid connect PV inverter LF",
    3100: "Front 1 tracker PV Storage",
    3400: "OffGrid SPF 3-5K",
    10001: "RF-ShineVersion",
    10002: "Web-ShinePano",
    10003: "Web-ShineWebBox",
    10004: "WL-WIFI Module",
}


def device_type(register) -> str:
    not_defined = f"Device type {register} not defined in protocol"

    if 10000 < register <= 10004:
        return DEVICE_TYPE_CODES.get(register, not_defined)

    return DEVICE_TYPE_CODES.get(register & 0xFF00, not_defined)
    

def trackers_and_phases(register) -> tuple[int, int]:
    # number of mppt trackers high byte, grid phases low byte 
    return (register >> 8, register & 0xFF)


FIRMWARE_REGISTER = GrowattDeviceRegisters(
    name=ATTR_FIRMWARE, register=9, value_type=str, length=6
)
SERIAL_NUMBER_REGISTER = GrowattDeviceRegisters(
    name=ATTR_SERIAL_NUMBER, register=23, value_type=str, length=5
)
DEVICE_TYPE_CODE_REGISTER = GrowattDeviceRegisters(
    name=ATTR_DEVICE_TYPE_CODE,
    register=43,
    value_type=custom_function,
    function=device_type
)
NUMBER_OF_TRACKERS_AND_PHASES_REGISTER = GrowattDeviceRegisters(
    name=ATTR_NUMBER_OF_TRACKERS_AND_PHASES,
    register=44,
    value_type=custom_function,
    function=trackers_and_phases
)


class InverterStatus(Enum):
    "Enum of possible Inverter Status."
    Waiting = 0
    Normal = 1
    Fault = 3


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


def inverter_status(value: dict[str, Any]) -> str | None:
    """Returns status based on multiple registery values."""
    if ATTR_STATUS_CODE not in value.keys():
        return None

    status_value = InverterStatus(value[ATTR_STATUS_CODE])

    if status_value is InverterStatus.Waiting:
        return status_value.name

    elif status_value == InverterStatus.Normal:
        derating = value.get(ATTR_DERATING_MODE, None)
        if (derating is not None and derating in INVERTER_DERATINGMODES.keys() and derating != 0):
            return f"{status_value.name} - {INVERTER_DERATINGMODES[derating]}"

        return status_value.name

    elif status_value is InverterStatus.Fault:
        fault = value.get(ATTR_FAULT_CODE, None)
        if fault is not None and fault != 0:
            return f"{status_value.name} - {INVERTER_FAULTCODES[fault]}"
