from datetime import time
from typing import Optional

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    CONF_MODEL,
    CONF_NAME,
    CONF_TYPE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)

from .API.const import DeviceTypes
from .API.device_type.storage_120 import ChargeDischargeMode, ChargeDischargePeriodValue
from .sensor_types.storage import STORAGE_TIME_TYPES
from .sensor_types.time_entity_description import GrowattTimeEntityDescription
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
    sensor_descriptions: list[GrowattTimeEntityDescription] = []
    supported_key_names = coordinator.growatt_api.get_register_names()

    device_type = DeviceTypes(config_entry.data[CONF_TYPE])
    
    if device_type in (DeviceTypes.HYBRID_120, DeviceTypes.HYBRID_120_TL_XH, DeviceTypes.STORAGE_120):
        for sensor in STORAGE_TIME_TYPES:
            if sensor.key not in supported_key_names:
                continue

            sensor_descriptions.append(sensor)

    coordinator.get_keys_by_name({sensor.key for sensor in sensor_descriptions}, True)

    entities.extend(
        [
            GrowattDeviceEntity(
                coordinator, description=description, entry=config_entry
            )
            for description in sensor_descriptions
        ]
    )

    async_add_entities(entities, True)

class GrowattDeviceEntity(CoordinatorEntity, RestoreEntity, TimeEntity):
    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator, description.key)
        self.entity_description: GrowattTimeEntityDescription = description
        self._config_entry = entry
        self.charge_discharge_period_state = ChargeDischargePeriodValue()

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
        if self.entity_description.charge_discharge_period_starttime:
            return f"{DOMAIN}_{self._config_entry.data[CONF_SERIAL_NUMBER]}_{self.entity_description.key}_starttime"
        elif self.entity_description.charge_discharge_period_endtime:
            return f"{DOMAIN}_{self._config_entry.data[CONF_SERIAL_NUMBER]}_{self.entity_description.key}_endtime"
        else:
            return f"{DOMAIN}_{self._config_entry.data[CONF_SERIAL_NUMBER]}_{self.entity_description.key}"

    async def async_added_to_hass(self) -> None:
        """Call when entity is about to be added to Home Assistant."""
        await super().async_added_to_hass()

        if (state := await self.async_get_last_state()) is None:
            return

        if state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        self._attr_native_value = time.fromisoformat(state.state)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if (state := self.coordinator.data.get(self.entity_description.key)) is None:
            return

        if self.entity_description.charge_discharge_period_starttime:
            self.charge_discharge_period_state = state
            self._attr_native_value = state.start_time
        elif self.entity_description.charge_discharge_period_endtime:
            self.charge_discharge_period_state = state
            self._attr_native_value = state.end_time
        else:
            return  # Not implemented
        self.async_write_ha_state()

    async def async_set_value(self, value: time) -> None:
        if self.entity_description.charge_discharge_period_starttime:
            self.charge_discharge_period_state.start_time = value
            await self.coordinator.write_charge_discharge_period_registers(
                    self.entity_description.key,
                    self.charge_discharge_period_state
                )
        elif self.entity_description.charge_discharge_period_endtime:
            self.charge_discharge_period_state.end_time = value
            await self.coordinator.write_charge_discharge_period_registers(
                    self.entity_description.key,
                    self.charge_discharge_period_state
                )
        else:
            return  # Not implemented
        self._attr_native_value = value
        self.async_write_ha_state()
