"""Growatt Sensor definitions for the Inverter type."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from homeassistant.core import Event
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_HOURS,
)

# NOT WORKING due to relative import into higher located reference
# from .growatt_local.API.device_type.inverter import (
#     ATTR_FREQUENCY,
#     ATTR_INPUT_1_AMPERAGE,
#     ATTR_INPUT_1_ENERGY_TODAY,
#     ATTR_INPUT_1_ENERGY_TOTAL,
#     ATTR_INPUT_1_POWER,
#     ATTR_INPUT_1_VOLTAGE,
#     ATTR_INPUT_2_AMPERAGE,
#     ATTR_INPUT_2_ENERGY_TODAY,
#     ATTR_INPUT_2_ENERGY_TOTAL,
#     ATTR_INPUT_2_POWER,
#     ATTR_INPUT_2_VOLTAGE,
#     ATTR_INPUT_ENERGY_TOTAL,
#     ATTR_INPUT_POWER,
#     ATTR_IPM_TEMPERATURE,
#     ATTR_OPERATION_HOURS,
#     ATTR_OUTPUT_1_AMPERAGE,
#     ATTR_OUTPUT_1_POWER,
#     ATTR_OUTPUT_1_VOLTAGE,
#     ATTR_OUTPUT_2_AMPERAGE,
#     ATTR_OUTPUT_2_POWER,
#     ATTR_OUTPUT_2_VOLTAGE,
#     ATTR_OUTPUT_3_AMPERAGE,
#     ATTR_OUTPUT_3_POWER,
#     ATTR_OUTPUT_3_VOLTAGE,
#     ATTR_OUTPUT_ENERGY_TODAY,
#     ATTR_OUTPUT_ENERGY_TOTAL,
#     ATTR_OUTPUT_POWER,
#     ATTR_OUTPUT_REACTIVE_POWER,
#     ATTR_TEMPERATURE,
# )

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


from .sensor_entity_description import GrowattSensorEntityDescription

INVERTER_SENSOR_TYPES: tuple[GrowattSensorEntityDescription, ...] = (
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_ENERGY_TODAY,
        name="Energy produced today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_ENERGY_TOTAL,
        name="Total energy produced",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_ENERGY_TOTAL,
        name="Total energy input",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_1_VOLTAGE,
        name="Input 1 voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_1_AMPERAGE,
        name="Input 1 Amperage",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_1_POWER,
        name="Input 1 Wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_1_ENERGY_TODAY,
        name="Input 1 energy today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_1_ENERGY_TOTAL,
        name="Input 1 total energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_2_VOLTAGE,
        name="Input 2 voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_2_AMPERAGE,
        name="Input 2 Amperage",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_2_POWER,
        name="Input 2 Wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_2_ENERGY_TODAY,
        name="Input 2 energy today",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        midnight_reset=True,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_2_ENERGY_TOTAL,
        name="Input 2 total energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_1_VOLTAGE,
        name="Output 1 voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_1_AMPERAGE,
        name="Output 1 Amperage",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_1_POWER,
        name="Output 1 Wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_2_VOLTAGE,
        name="Output 2 voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_2_AMPERAGE,
        name="Output 2 Amperage",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_2_POWER,
        name="Output 2 Wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_3_VOLTAGE,
        name="Output 3 voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_3_AMPERAGE,
        name="Output 3 Amperage",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_3_POWER,
        name="Output 3 Wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OPERATION_HOURS,
        name="Running hours",
        native_unit_of_measurement=TIME_HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_INPUT_POWER,
        name="Internal wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_FREQUENCY,
        name="AC frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_POWER,
        name="Output power",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_OUTPUT_REACTIVE_POWER,
        name="Reactive wattage",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_IPM_TEMPERATURE,
        name="Intelligent Power Management temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(
        key=ATTR_TEMPERATURE,
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    GrowattSensorEntityDescription(key="status", name="Status", device_class=f"growatt_local__status"),
)
