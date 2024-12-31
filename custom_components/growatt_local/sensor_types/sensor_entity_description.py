"""Sensor Entity Description for the Growatt integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntityDescription


@dataclass
class GrowattSensorRequiredKeysMixin:
    """Mixin for required keys."""

    key: str
    midnight_reset: bool = False


@dataclass
class GrowattSensorEntityDescription(GrowattSensorRequiredKeysMixin, SensorEntityDescription):
    """Describes Growatt sensor entity."""
