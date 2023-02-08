"""Sensor Entity Description for the Growatt integration."""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable, Iterable

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.core import Event


@dataclass
class GrowattRequiredKeysMixin:
    """Mixin for required keys."""

    key: str
    midnight_reset: bool = False


@dataclass
class GrowattSensorEntityDescription(GrowattRequiredKeysMixin, SensorEntityDescription):
    """Describes Growatt sensor entity."""
