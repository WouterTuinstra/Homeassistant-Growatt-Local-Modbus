from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.select import SelectEntityDescription


@dataclass
class GrowattSelectRequiredKeysMixin:
    """Mixin for required keys."""
    key: str
    value_to_state_dict: dict
    charge_discharge_period_mode: bool = False


@dataclass
class GrowattSelectEntityDescription(SelectEntityDescription, GrowattSelectRequiredKeysMixin):
    """Describes Growatt select entity."""
