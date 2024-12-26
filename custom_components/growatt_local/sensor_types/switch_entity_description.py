"""Sensor Entity Description for the Growatt integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntityDescription


@dataclass
class GrowattSwitchRequiredKeysMixin:
    """Mixin for required keys."""
    key: str
    state_on: str|int
    state_off: str|int
    mask: int = 0


@dataclass
class GrowattSwitchEntityDescription(SwitchEntityDescription, GrowattSwitchRequiredKeysMixin):
    """Describes Growatt sensor entity."""


