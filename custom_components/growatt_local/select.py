from typing import Optional

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    CONF_MODEL,
    CONF_NAME,
)

from .API.device_type.base import EXPORT_POWER_LIMIT_ENABLE_CODES

from .sensor_types.inverter import INVERTER_EXPORT_POWER_LIMIT_ENABLE
from . import GrowattLocalCoordinator
from .const import (
    CONF_FIRMWARE,
    CONF_METER_CONNECTED,
    CONF_SERIAL_NUMBER,
    DOMAIN,
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: GrowattLocalCoordinator = hass.data[DOMAIN][config_entry.data[CONF_SERIAL_NUMBER]]
    entities = []

    meter_connected = config_entry.data.get(CONF_METER_CONNECTED, False)

    if meter_connected:
        entities.append(
            InverterSelectEntity(
                coordinator, 
                entry=config_entry, 
                description=INVERTER_EXPORT_POWER_LIMIT_ENABLE
            )
        )
        coordinator.get_keys_by_name((INVERTER_EXPORT_POWER_LIMIT_ENABLE.key,), True)

    async_add_entities(entities, True)

class InverterSelectEntity(CoordinatorEntity, RestoreEntity, SelectEntity):
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

    async def async_added_to_hass(self) -> None:
        """Call when entity is about to be added to Home Assistant."""
        await super().async_added_to_hass()

        if (state := await self.async_get_last_state()) is None:
            return

        if state.state not in self.options:
            return

        self._attr_current_option = state.state

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if (state := self.coordinator.data.get(self.entity_description.key)) not in self.options:
            return
        self._attr_current_option = state
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        value = next((k for k, v in EXPORT_POWER_LIMIT_ENABLE_CODES.items() if v == option), None)
        if value is None:
            return
        await self.coordinator.write_register(self.entity_description.key, value)
        self._attr_current_option = option
        self.async_write_ha_state()
