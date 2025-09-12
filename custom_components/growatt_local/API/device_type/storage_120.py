"""Device defaults for a Growatt Inverter."""

from .base import (
    GrowattDeviceRegisters,
    custom_function,
    FIRMWARE_REGISTER,
    DEVICE_TYPE_CODE_REGISTER,
    NUMBER_OF_TRACKERS_AND_PHASES_REGISTER,
    ATTR_INVERTER_MODEL,
    ATTR_INVERTER_ENABLED,
    ATTR_MODBUS_VERSION,
    ATTR_SOC_PERCENTAGE,
    ATTR_DISCHARGE_POWER,
    ATTR_CHARGE_POWER,
    ATTR_OUTPUT_REACTIVE_POWER,
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
    ATTR_AC_CHARGE_ENABLED,
    ATTR_SERIAL_NUMBER,
    ATTR_PAC_TO_GRID_TOTAL,
    ATTR_PAC_TO_USER_TOTAL,
    ATTR_BDC_NEW_FLAG,
    ATTR_BATTERY_TEMPERATURE_A,
    ATTR_BATTERY_TEMPERATURE_B,
    ATTR_COMM_BOARD_TEMPERATURE,
    ATTR_PRESENT_FFT_A,
    ATTR_INV_START_DELAY,
    ATTR_BATTERY_VOLTAGE,
    ATTR_BATTERY_CURRENT,
    ATTR_VBUS1_VOLTAGE,
    ATTR_VBUS2_VOLTAGE,
    ATTR_BUCK_BOOST_CURRENT,
    ATTR_LLC_CURRENT,
    ATTR_BMS_MAX_VOLT_CELL_NO,
    ATTR_BMS_MIN_VOLT_CELL_NO,
    ATTR_BMS_AVG_TEMP_A,
    ATTR_BMS_MAX_CELL_TEMP_A,
    ATTR_BMS_AVG_TEMP_B,
    ATTR_BMS_MAX_CELL_TEMP_B,
    ATTR_BMS_AVG_TEMP_C,
    ATTR_BMS_MAX_SOC,
    ATTR_BMS_MIN_SOC,
    ATTR_PARALLEL_BATTERY_NUM,
    ATTR_BMS_DERATE_REASON,
    ATTR_BMS_GAUGE_FCC_AH,
    ATTR_BMS_GAUGE_RM_AH,
    ATTR_BMS_PROTECT1,
    ATTR_BMS_WARN1,
    ATTR_BMS_FAULT1,
    ATTR_BMS_FAULT2,
    ATTR_BAT_ISO_STATUS,
    ATTR_BATT_REQUEST_FLAGS,
    ATTR_BMS_STATUS,
    ATTR_BMS_PROTECT2,
    ATTR_BMS_WARN2,
    ATTR_BMS_SOC,
    ATTR_BMS_BATTERY_VOLTAGE,
    ATTR_BMS_BATTERY_CURRENT,
    ATTR_BMS_CELL_MAX_TEMP,
    ATTR_BMS_MAX_CHARGE_CURRENT,
    ATTR_BMS_MAX_DISCHARGE_CURRENT,
    ATTR_BMS_CYCLE_COUNT,
    ATTR_BMS_SOH,
    ATTR_BMS_CHARGE_VOLT_LIMIT,
    ATTR_BMS_DISCHARGE_VOLT_LIMIT,
    ATTR_BMS_WARN3,
    ATTR_BMS_PROTECT3,
    ATTR_BMS_CELL_VOLT_MAX,
    ATTR_BMS_CELL_VOLT_MIN,
)

MAXIMUM_DATA_LENGTH = 100


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


SERIAL_NUMBER_REGISTER = GrowattDeviceRegisters(
    name=ATTR_SERIAL_NUMBER, register=3001, value_type=str, length=15
)

STORAGE_HOLDING_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
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
)

STORAGE_HOLDING_REGISTERS_120_TL_XH: tuple[GrowattDeviceRegisters, ...] = (
    GrowattDeviceRegisters(
        name=ATTR_INVERTER_ENABLED,
        register=0,
        value_type=int,
    ),
    FIRMWARE_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_INVERTER_MODEL,
        register=28,
        value_type=custom_function,
        length=2,
        function=model,
    ),
    DEVICE_TYPE_CODE_REGISTER,
    NUMBER_OF_TRACKERS_AND_PHASES_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_MODBUS_VERSION,
        register=88,
        value_type=float,
        scale=100,
    ),
    SERIAL_NUMBER_REGISTER,
    GrowattDeviceRegisters(
        name=ATTR_AC_CHARGE_ENABLED,
        register=3049,
        value_type=int,
        length=1,
    ),
)

STORAGE_INPUT_REGISTERS_120: tuple[GrowattDeviceRegisters, ...] = (
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
    # BDC presence flag (soms nuttig bij debugging/mapping)
    GrowattDeviceRegisters(
        name=ATTR_BDC_NEW_FLAG, register=3164, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_VOLTAGE, register=3169, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_CURRENT, register=3170, value_type=float, scale=10
    ),
    GrowattDeviceRegisters(
        name=ATTR_SOC_PERCENTAGE, register=3171, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_VBUS1_VOLTAGE, register=3172, value_type=float, scale=10
    ),
    GrowattDeviceRegisters(
        name=ATTR_VBUS2_VOLTAGE, register=3173, value_type=float, scale=10
    ),
    GrowattDeviceRegisters(
        name=ATTR_BUCK_BOOST_CURRENT, register=3174, value_type=float, scale=10
    ),
    GrowattDeviceRegisters(
        name=ATTR_LLC_CURRENT, register=3175, value_type=float, scale=10
    ),
    # Batterijtemperaturen (0.1 C schaal, integration hanteert doorgaans *0.1 naar float)
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_TEMPERATURE_A, register=3176, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATTERY_TEMPERATURE_B, register=3177, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_DISCHARGE_POWER, register=3178, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_CHARGE_POWER, register=3180, value_type=float, length=2
    ),
    GrowattDeviceRegisters(
        name=ATTR_OUTPUT_REACTIVE_POWER, register=3021, value_type=float, length=2
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
        name=ATTR_COMM_BOARD_TEMPERATURE, register=3097, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_PRESENT_FFT_A, register=3111, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_INV_START_DELAY, register=3115, value_type=int
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
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_VOLT_CELL_NO, register=3189, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MIN_VOLT_CELL_NO, register=3190, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_AVG_TEMP_A, register=3191, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_CELL_TEMP_A, register=3192, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_AVG_TEMP_B, register=3193, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_CELL_TEMP_B, register=3194, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_AVG_TEMP_C, register=3195, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_SOC, register=3196, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MIN_SOC, register=3197, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_PARALLEL_BATTERY_NUM, register=3198, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_DERATE_REASON, register=3199, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_GAUGE_FCC_AH, register=3200, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_GAUGE_RM_AH, register=3201, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_PROTECT1, register=3202, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_WARN1, register=3203, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_FAULT1, register=3204, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_FAULT2, register=3205, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BAT_ISO_STATUS, register=3210, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BATT_REQUEST_FLAGS, register=3211, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_STATUS, register=3212, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_PROTECT2, register=3213, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_WARN2, register=3214, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_SOC, register=3215, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_BATTERY_VOLTAGE, register=3216, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_BATTERY_CURRENT, register=3217, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_CELL_MAX_TEMP, register=3218, value_type=float
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_CHARGE_CURRENT, register=3219, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_MAX_DISCHARGE_CURRENT, register=3220, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_CYCLE_COUNT, register=3221, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_SOH, register=3222, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_CHARGE_VOLT_LIMIT, register=3223, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_DISCHARGE_VOLT_LIMIT, register=3224, value_type=float, scale=100
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_WARN3, register=3225, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_PROTECT3, register=3226, value_type=int
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_CELL_VOLT_MAX, register=3230, value_type=float, scale=1000
    ),
    GrowattDeviceRegisters(
        name=ATTR_BMS_CELL_VOLT_MIN, register=3231, value_type=float, scale=1000
    ),
)

