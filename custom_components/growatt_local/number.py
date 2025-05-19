from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, CONF_MODEL, CONF_NAME, CONF_FIRMWARE, CONF_SERIAL_NUMBER
from .sensor_types.inverter import INVERTER_POWER_LIMIT
from .sensor_types.number_entity_description import GrowattNumberEntityDescription


class GrowattNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, config_entry, description: GrowattNumberEntityDescription):
        super().__init__(coordinator)
        self.entity_description = description
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{config_entry.data[CONF_SERIAL_NUMBER]}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_SERIAL_NUMBER])},
            manufacturer="Growatt",
            model=config_entry.data[CONF_MODEL],
            sw_version=config_entry.data[CONF_FIRMWARE],
            name=config_entry.options[CONF_NAME],
        )

    @property
    def native_value(self) -> int:
        return self.coordinator.data.get(self.entity_description.key, 0)

    async def async_set_native_value(self, value: float) -> None:
        raw_value = int(value)
        await self.coordinator.write_register(self.entity_description.register, raw_value)
        await self.coordinator.force_refresh()

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.data[CONF_SERIAL_NUMBER]]
    async_add_entities([
        GrowattNumber(coordinator, config_entry, INVERTER_POWER_LIMIT)
    ])
