from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GrowattLocalCoordinator
from .const import DOMAIN

INVERTER_POWER_LIMIT_DESCRIPTION = NumberEntityDescription(
    key="power_limit",
    name="Power Limit",
    native_unit_of_measurement="%",
    native_min_value=0,
    native_max_value=100,
    native_step=1,
    icon="mdi:transmission-tower-export",
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GrowattLocalCoordinator = hass.data[DOMAIN][entry.data["serial_number"]]
    async_add_entities([
        InverterPowerLimitEntity(coordinator, entry, INVERTER_POWER_LIMIT_DESCRIPTION)
    ])
    
class InverterPowerLimitEntity(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.config_entry = entry
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_suggested_object_id = f"{entry.title.lower()}_{description.key}"
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> int:
        return self.coordinator.data.get("power_limit", 0)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.growatt_api.set_power_limit(int(value))
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, self.config_entry.data["serial_number"])
            },
            "name": self.config_entry.title,
            "manufacturer": "Growatt",
            "model": self.config_entry.data.get("model", "Unknown"),
        }
