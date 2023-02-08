from dataclasses import dataclass

ATTR_STATUS = "status"
ATTR_STATUS_CODE = "status_code"
ATTR_DERATING_MODE = "derating_mode"
ATTR_FAULT_CODE = "fault_code"
ATTR_WARNING_CODE = "warning_code"
ATTR_WARNING_VALUE = "warning_value"


@dataclass
class GrowattDeviceRegisters:
    """Dataclass object to define register value for Growatt devices using modbus."""

    name: str
    register: int
    value_type: type
    double_value: bool = False
    ascii_length: int = 1
    scale: int = 10
