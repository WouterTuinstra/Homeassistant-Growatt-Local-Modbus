"""Stub sensor component APIs for documentation generation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class SensorDeviceClass:
    ENERGY = "energy"
    VOLTAGE = "voltage"
    CURRENT = "current"
    POWER = "power"
    DURATION = "duration"
    TEMPERATURE = "temperature"
    FREQUENCY = "frequency"
    BATTERY = "battery"
    POWER_FACTOR = "power_factor"


class SensorStateClass:
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


@dataclass
class SensorEntityDescription:
    """Minimal data container matching Home Assistant's entity description."""

    key: str
    name: str | None = None
    native_unit_of_measurement: str | None = None
    device_class: str | None = None
    state_class: str | None = None
    entity_registry_enabled_default: bool = True
    suggested_display_precision: int | None = None
    icon: str | None = None
    options: Any | None = None
    value_fn: Any | None = None
    midnight_reset: bool = False
    suggested_unit_of_measurement: str | None = None
    translation_key: str | None = None
