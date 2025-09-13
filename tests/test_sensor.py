from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import (
    CONF_NAME,
    CONF_MODEL,
    CONF_TYPE,
    CONF_SCAN_INTERVAL,
)

from custom_components.growatt_local.const import (
    CONF_SERIAL_NUMBER,
    CONF_FIRMWARE,
    CONF_DC_STRING,
    CONF_AC_PHASES,
    CONF_POWER_SCAN_ENABLED,
    CONF_POWER_SCAN_INTERVAL,
    CONF_INVERTER_POWER_CONTROL,
    DOMAIN,
)
from custom_components.growatt_local.API.const import DeviceTypes
from custom_components.growatt_local import sensor


async def test_sensor_setup(hass, coordinator):
    """Test setting up the sensor platform."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_SERIAL_NUMBER: "abc123",
            CONF_MODEL: "Model",
            CONF_TYPE: DeviceTypes.INVERTER_120,
            CONF_DC_STRING: 1,
            CONF_AC_PHASES: 1,
            CONF_FIRMWARE: "1.0",
        },
        options={
            CONF_NAME: "Growatt",
            CONF_SCAN_INTERVAL: 60,
            CONF_POWER_SCAN_ENABLED: False,
            CONF_POWER_SCAN_INTERVAL: 5,
            CONF_INVERTER_POWER_CONTROL: False,
        },
    )
    entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})["abc123"] = coordinator

    entities = []

    def async_add_entities(new_entities, update_before_add=False):
        entities.extend(new_entities)

    await sensor.async_setup_entry(hass, entry, async_add_entities)

    assert entities
    assert entities[0].entity_description.key == "input_power"
