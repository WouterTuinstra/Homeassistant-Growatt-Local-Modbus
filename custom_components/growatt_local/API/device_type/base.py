from dataclasses import dataclass

ATTR_STATUS = "status"
ATTR_STATUS_CODE = "status_code"
ATTR_DERATING_MODE = "derating_mode"
ATTR_FAULT_CODE = "fault_code"
ATTR_WARNING_CODE = "warning_code"
ATTR_WARNING_VALUE = "warning_value"



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
