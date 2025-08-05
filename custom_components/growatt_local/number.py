from typing import Optional

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.const import (
    CONF_MODEL,
    CONF_NAME,
)

from .API.const import DeviceTypes

from .sensor_types.inverter import INVERTER_OUTPUT_POWER_LIMIT
from . import GrowattLocalCoordinator
from .const import (
    CONF_FIRMWARE,
    CONF_SERIAL_NUMBER,
    CONF_INVERTER_POWER_CONTROL,
    DOMAIN,
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GrowattLocalCoordinator = hass.data[DOMAIN][config_entry.data[CONF_SERIAL_NUMBER]]
    entities = []

    if config_entry.options.get(CONF_INVERTER_POWER_CONTROL, False):
        entities.append(InverterPowerLimitEntity(coordinator, entry=config_entry, description=INVERTER_OUTPUT_POWER_LIMIT))
        coordinator.get_keys_by_name(INVERTER_OUTPUT_POWER_LIMIT.key, True)

    async_add_entities(entities, True)

class InverterPowerLimitEntity(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._config_entry = entry

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_SERIAL_NUMBER])},
            manufacturer="Growatt",
            model=entry.data[CONF_MODEL],
            sw_version=entry.data[CONF_FIRMWARE],
            name=entry.options[CONF_NAME],
        )

    @property
    def name(self):
        return f"{self._config_entry.options[CONF_NAME]} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{DOMAIN}_{self._config_entry.data[CONF_SERIAL_NUMBER]}_{self.entity_description.key}"

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.write_register (self.entity_description.key, int(value))
        self._attr_native_value = value
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if (state := self.coordinator.data.get(self.entity_description.key)) is None:
            return
        self._attr_native_value = state
        self.async_write_ha_state()
