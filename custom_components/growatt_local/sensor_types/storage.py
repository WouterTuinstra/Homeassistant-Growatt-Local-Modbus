"""Growatt Sensor definitions for the Inverter type."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
    PERCENTAGE,
)
from .sensor_entity_description import GrowattSensorEntityDescription
from .switch_entity_description import GrowattSwitchEntityDescription

from ..API.device_type.base import (
    ATTR_AC_CHARGE_ENABLED,
    ATTR_INVERTER_ENABLED,
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
    ATTR_PAC_TO_GRID_TOTAL,
    ATTR_PAC_TO_USER_TOTAL,
    ATTR_BATTERY_TEMPERATURE_A,
    ATTR_BATTERY_TEMPERATURE_B,
    ATTR_COMM_BOARD_TEMPERATURE,
    ATTR_BDC_NEW_FLAG,
    ATTR_PRESENT_FFT_A,
    ATTR_INV_START_DELAY,
    ATTR_OUTPUT_REACTIVE_POWER,
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
    ATTR_BMS_DERATE_REASON,
    ATTR_BMS_GAUGE_FCC_AH,
    ATTR_BMS_GAUGE_RM_AH,
    ATTR_BMS_PROTECT1,
    ATTR_BMS_WARN1,
    ATTR_BMS_FAULT1,
    ATTR_BMS_FAULT2,
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

STORAGE_TL_XH_SWITCH_TYPES: tuple[GrowattSwitchEntityDescription, ...] = (
    GrowattSwitchEntityDescription(
        key=ATTR_AC_CHARGE_ENABLED,
        name="AC Charge",
        state_on=0x1,
        state_off=0x0,
    ),
    GrowattSwitchEntityDescription(
        key=ATTR_INVERTER_ENABLED,
        name="Power control",
        translation_key="inverter_enabled",
        state_on=0x1,
        state_off=0x0,
        mask=0x1,
    ),
)


STORAGE_SENSOR_TYPES: tuple[GrowattSensorEntityDescription, ...] = (
    GrowattSensorEntityDescription(
        key=ATTR_BATTERY_TEMPERATURE_A,
        name="Battery temperature A",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BATTERY_TEMPERATURE_B,
        name="Battery temperature B",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_COMM_BOARD_TEMPERATURE,
        name="Comm board temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BDC_NEW_FLAG,
        name="BDC present",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_PRESENT_FFT_A,
        name="Present FFT A",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INV_START_DELAY,
        name="Inverter start delay",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_SOC_PERCENTAGE,
        name="SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY
    ),
    GrowattSensorEntityDescription(
        key=ATTR_DISCHARGE_POWER,
        name="Discharge Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER
    ),
    GrowattSensorEntityDescription(
        key=ATTR_CHARGE_POWER,
        name="Charge Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER
    ),
    GrowattSensorEntityDescription(
        key=ATTR_POWER_TO_USER,
        name="Power to user",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_POWER_TO_GRID,
        name="Power to grid",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_POWER_USER_LOAD,
        name="Power user load",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_ENERGY_TO_GRID_TOTAL,
        name="Energy To Grid (Total)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_ENERGY_TO_GRID_TODAY,
        name="Energy To Grid (Today)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True
    ),
    GrowattSensorEntityDescription(
        key=ATTR_ENERGY_TO_USER_TOTAL,
        name="Energy To User (Total)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),

    GrowattSensorEntityDescription(
        key=ATTR_ENERGY_TO_USER_TODAY,
        name="Energy To User (Today)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True
    ),
    GrowattSensorEntityDescription(
        key=ATTR_AC_CHARGE_ENABLED,
        name="AC Charge Enabled"
    ),
    GrowattSensorEntityDescription(
        key=ATTR_DISCHARGE_ENERGY_TODAY,
        name="Battery Discharged (Today)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True
    ),
    GrowattSensorEntityDescription(
        key=ATTR_DISCHARGE_ENERGY_TOTAL,
        name="Battery Discharged (Total)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_CHARGE_ENERGY_TODAY,
        name="Battery Charged (Today)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True
    ),
    GrowattSensorEntityDescription(
        key=ATTR_CHARGE_ENERGY_TOTAL,
        name="Battery Charged (Total)",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_PAC_TO_USER_TOTAL,
        name="AC to user total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_PAC_TO_GRID_TOTAL,
        name="AC to grid total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_REACTIVE_POWER,
        name="Reactive power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BATTERY_VOLTAGE,
        name="Battery voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BATTERY_CURRENT,
        name="Battery current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_VBUS1_VOLTAGE,
        name="VBUS1 voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_VBUS2_VOLTAGE,
        name="VBUS2 voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BUCK_BOOST_CURRENT,
        name="Buck/boost current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_LLC_CURRENT,
        name="LLC current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_VOLT_CELL_NO,
        name="BMS max volt cell no",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MIN_VOLT_CELL_NO,
        name="BMS min volt cell no",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_AVG_TEMP_A,
        name="BMS avg temp A",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_CELL_TEMP_A,
        name="BMS max cell temp A",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_AVG_TEMP_B,
        name="BMS avg temp B",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_CELL_TEMP_B,
        name="BMS max cell temp B",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_AVG_TEMP_C,
        name="BMS avg temp C",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_SOC,
        name="BMS max SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MIN_SOC,
        name="BMS min SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_DERATE_REASON,
        name="BMS derate reason",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_GAUGE_FCC_AH,
        name="BMS full charge capacity",
        native_unit_of_measurement="Ah",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_GAUGE_RM_AH,
        name="BMS remaining capacity",
        native_unit_of_measurement="Ah",
    ),
    # Bitfield registers; each bit signals a specific BMS condition.
    # The raw value is exposed so templates can decode individual flags.
    GrowattSensorEntityDescription(
        key=ATTR_BMS_PROTECT1,
        name="BMS protect 1",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_WARN1,
        name="BMS warn 1",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_FAULT1,
        name="BMS fault 1",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_FAULT2,
        name="BMS fault 2",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_STATUS,
        name="BMS status",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_PROTECT2,
        name="BMS protect 2",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_WARN2,
        name="BMS warn 2",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_SOC,
        name="BMS SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_BATTERY_VOLTAGE,
        name="BMS battery voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_BATTERY_CURRENT,
        name="BMS battery current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_CELL_MAX_TEMP,
        name="BMS cell max temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_CHARGE_CURRENT,
        name="BMS max charge current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_MAX_DISCHARGE_CURRENT,
        name="BMS max discharge current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_CYCLE_COUNT,
        name="BMS cycle count",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_SOH,
        name="BMS SOH",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_CHARGE_VOLT_LIMIT,
        name="BMS charge voltage limit",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_DISCHARGE_VOLT_LIMIT,
        name="BMS discharge voltage limit",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_WARN3,
        name="BMS warn 3",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_PROTECT3,
        name="BMS protect 3",
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_CELL_VOLT_MAX,
        name="BMS cell voltage max",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_BMS_CELL_VOLT_MIN,
        name="BMS cell voltage min",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
)
