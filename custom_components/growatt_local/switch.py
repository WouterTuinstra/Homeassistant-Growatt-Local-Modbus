from datetime import timedelta

import logging
import re


from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    CONF_MODEL,
    CONF_NAME,
    CONF_TYPE,
)


from pymodbus.exceptions import ModbusIOException



from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .API.const import DeviceTypes
from .API.device_type.base import (
    ATTR_INPUT_POWER,
    ATTR_OUTPUT_POWER,
)

from .sensor_types.sensor_entity_description import GrowattSwitchEntityDescription
from .sensor_types.inverter import INVERTER_SWITCH_TYPES
from .const import (
    CONF_AC_PHASES,
    CONF_DC_STRING,
    CONF_FIRMWARE,
    CONF_SERIAL_NUMBER,
    CONF_POWER_SCAN_ENABLED,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:


    coordinator = hass.data[DOMAIN][config_entry.data[CONF_SERIAL_NUMBER]]

    entities = []
    power_sensor = []
    sensor_descriptions: list[GrowattSwitchEntityDescription] = []

    device_type = DeviceTypes(config_entry.data[CONF_TYPE])

    if device_type in (DeviceTypes.INVERTER, DeviceTypes.INVERTER_315, DeviceTypes.INVERTER_120):
        supported_key_names = coordinator.growatt_api.get_register_names()

        for sensor in INVERTER_SWITCH_TYPES:
            if sensor.key not in supported_key_names:
                continue

            if re.match(r"input_\d+", sensor.key) and not re.match(f"input_[1-{config_entry.data[CONF_DC_STRING]}]", sensor.key):
                continue
            elif re.match(r"output_\d+", sensor.key) and not re.match(f"output_[1-{config_entry.data[CONF_AC_PHASES]}]", sensor.key):
                continue

            sensor_descriptions.append(sensor)

        power_sensor = (ATTR_INPUT_POWER, ATTR_OUTPUT_POWER)

    else:
        _LOGGER.debug(
            "Device type %s was found but is not supported right now",
            config_entry.data[CONF_TYPE],
        )

    coordinator.get_keys_by_name({sensor.key for sensor in sensor_descriptions}, True)

    if config_entry.data[CONF_POWER_SCAN_ENABLED]:
        power_keys = coordinator.get_keys_by_name(power_sensor)

        coordinator.p_keys.update(power_keys)

    entities.extend(
        [
            GrowattDeviceEntity(
                coordinator, description=description, entry=config_entry
            )
            for description in sensor_descriptions
        ]
    )

    async_add_entities(entities, True)


class GrowattDeviceEntity(CoordinatorEntity, RestoreEntity, SwitchEntity):
    """An entity using CoordinatorEntity."""

    def __init__(self, coordinator, description, entry):
        """Pass coordinator to CoordinatorEntity."""


        self._is_on = False
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._attr_unique_id = (
            f"{DOMAIN}_{entry.data[CONF_SERIAL_NUMBER]}_sw_{description.key}"
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data[CONF_SERIAL_NUMBER])},
            manufacturer="Growatt",
            model=entry.data[CONF_MODEL],
            sw_version=entry.data[CONF_FIRMWARE],
            name=entry.data[CONF_NAME],
        )

    async def async_added_to_hass(self) -> None:
        """Call when entity is about to be added to Home Assistant."""
        await super().async_added_to_hass()

        if self.entity_description.midnight_reset:
            self.async_on_remove(
                self.coordinator.async_add_midnight_listener(
                    self._handle_midnight_update, self.coordinator_context
                )
            )

        if (state := await self.async_get_last_state()) is None:
            return

        self._attr_native_value = state.state

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""

        _LOGGER.warning(
            "Turn inverter on"
        )
        self._is_on = True
        try:
            await self.coordinator.set_state(True)
        except ModbusIOException:
            pass; #ignore growatt empty response
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False

        _LOGGER.warning(
            "Turn inverter off"
        )

        try:
            await self.coordinator.set_state(False)

        except ModbusIOException:
            pass; #ignore growatt empty response
        self.async_write_ha_state()





    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if (state := self.coordinator.data.get(self.entity_description.key)) is None:
            return


        _LOGGER.warning(
            "Update inverter state: %s", state
        )

        self._is_on = (state == 1)
        self._attr_native_value = self._is_on
        self.async_write_ha_state()


