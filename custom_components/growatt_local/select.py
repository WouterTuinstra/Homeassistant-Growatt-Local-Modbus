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
    CONF_TYPE,
)

from .API.const import DeviceTypes
from .API.device_type.storage_120 import ChargeDischargeMode, ChargeDischargePeriodValue
from .sensor_types.inverter import INVERTER_SELECT_TYPES_W_METER
from .sensor_types.storage import STORAGE_SELECT_TYPES
from .sensor_types.select_entity_description import GrowattSelectEntityDescription
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
    sensor_descriptions: list[GrowattSelectEntityDescription] = []
    supported_key_names = coordinator.growatt_api.get_register_names()

    device_type = DeviceTypes(config_entry.data[CONF_TYPE])
    meter_connected = config_entry.data.get(CONF_METER_CONNECTED, False)

    if device_type in (DeviceTypes.INVERTER, DeviceTypes.INVERTER_315, DeviceTypes.INVERTER_120,
                       DeviceTypes.HYBRID_120, DeviceTypes.HYBRID_120_TL_XH):
        if meter_connected:
            for sensor in INVERTER_SELECT_TYPES_W_METER:
                if sensor.key not in supported_key_names:
                    continue
                
                sensor_descriptions.append(sensor)
    
    if device_type in (DeviceTypes.HYBRID_120, DeviceTypes.HYBRID_120_TL_XH, DeviceTypes.STORAGE_120):
        for sensor in STORAGE_SELECT_TYPES:
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

class GrowattDeviceEntity(CoordinatorEntity, RestoreEntity, SelectEntity):
    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator, description.key)
        self.entity_description: GrowattSelectEntityDescription = description
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
        if self.entity_description.charge_discharge_period_mode:
            return f"{DOMAIN}_{self._config_entry.data[CONF_SERIAL_NUMBER]}_{self.entity_description.key}_mode"
        else:
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
        if (state := self.coordinator.data.get(self.entity_description.key)) is None:
            return

        if self.entity_description.charge_discharge_period_mode:
            self.charge_discharge_period_state = state
            self._attr_current_option = state.mode.value
        else:
            if state not in self.options:
                return
            self._attr_current_option = state
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        if self.entity_description.charge_discharge_period_mode:
            if option not in list(ChargeDischargeMode):
                return
            self.charge_discharge_period_state.mode = ChargeDischargeMode(option)
            await self.coordinator.write_charge_discharge_period_registers(
                    self.entity_description.key,
                    self.charge_discharge_period_state
                )
        else:
            value = next((k for k, v in self.entity_description.value_to_state_dict.items() if v == option), None)
            if value is None:
                return
            await self.coordinator.write_register(self.entity_description.key, value)
        self._attr_current_option = option
        self.async_write_ha_state()
