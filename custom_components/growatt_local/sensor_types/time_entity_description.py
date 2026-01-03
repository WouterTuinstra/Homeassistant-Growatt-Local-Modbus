from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.time import TimeEntityDescription


@dataclass
class GrowattTimeRequiredKeysMixin:
    """Mixin for required keys."""
    key: str
    charge_discharge_period_starttime: bool = False
    charge_discharge_period_endtime: bool = False


@dataclass
class GrowattTimeEntityDescription(TimeEntityDescription, GrowattTimeRequiredKeysMixin):
    """Describes Growatt time entity."""
