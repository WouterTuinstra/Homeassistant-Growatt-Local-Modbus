from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntityDescription

from homeassistant.components.number import NumberEntityDescription

@dataclass
class GrowattNumberRequiredKeysMixin:
    """Mixin for required keys."""
    key: str



@dataclass
class GrowattNumberEntityDescription(NumberEntityDescription, GrowattNumberRequiredKeysMixin):
    """Describes Growatt number entity."""


