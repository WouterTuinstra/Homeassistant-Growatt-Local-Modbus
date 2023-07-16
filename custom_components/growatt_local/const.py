"""Define constants for the Growatt Server component."""
from homeassistant.backports.enum import StrEnum
from homeassistant.const import Platform

CONF_LAYER = "communication_layer"
CONF_SERIAL = "serial"
CONF_TCP = "tcp"
CONF_UDP = "udp"

CONF_FRAME = "modbus_frame"

CONF_SERIAL_PORT = "port"
CONF_BAUDRATE = "baudrate"
CONF_STOPBITS = "stopbits"
CONF_PARITY = "parity"
CONF_BYTESIZE = "bytesize"

CONF_DC_STRING = "dc_string"
CONF_AC_PHASES = "ac_phases"

CONF_POWER_SCAN_INTERVAL = "power_scan_interval"
CONF_POWER_SCAN_ENABLED = "power_scan_enabled"

CONF_SERIAL_NUMBER = "serial_number"
CONF_FIRMWARE = "firmware"


class ParityOptions(StrEnum):
    NONE = "None"
    EVEN = "Even"
    ODD = "Odd"
    MARK = "Mark"
    SPACE = "Space"


DEFAULT_PLANT_ID = "0"

DEFAULT_NAME = "Growatt Modbus"

DOMAIN = "growatt_local"

PLATFORMS = [Platform.SENSOR]
