from unittest.mock import AsyncMock, Mock, patch

from homeassistant import config_entries
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_ADDRESS,
    CONF_NAME,
    CONF_MODEL,
    CONF_TYPE,
    CONF_SCAN_INTERVAL,
)

from custom_components.growatt_local.const import (
    CONF_LAYER,
    CONF_TCP,
    CONF_FRAME,
    CONF_DC_STRING,
    CONF_AC_PHASES,
    CONF_POWER_SCAN_ENABLED,
    CONF_POWER_SCAN_INTERVAL,
    CONF_INVERTER_POWER_CONTROL,
    CONF_SERIAL_NUMBER,
    DOMAIN,
)
from custom_components.growatt_local.API.const import DeviceTypes
from custom_components.growatt_local.API.device_type.base import GrowattDeviceInfo


async def test_user_step_form(hass):
    """Test that the initial form is served."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"


async def test_network_flow_creates_entry(hass):
    """Test completing the network config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_LAYER: CONF_TCP}
    )

    device_info = GrowattDeviceInfo(
        serial_number="abc123",
        model="Model",
        firmware="1.0",
        mppt_trackers=1,
        grid_phases=1,
        modbus_version=1.0,
        device_type=DeviceTypes.INVERTER_120,
    )

    mock_network = AsyncMock()
    mock_network.connect.return_value = None
    # connected and close are synchronous in implementation; use normal Mock to avoid un-awaited coroutine warnings
    mock_network.connected = Mock(return_value=True)
    mock_network.close = Mock(return_value=None)

    with patch(
        "custom_components.growatt_local.config_flow.GrowattNetwork",
        return_value=mock_network,
    ), patch(
        "custom_components.growatt_local.config_flow.get_device_info",
        return_value=device_info,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_IP_ADDRESS: "1.2.3.4",
                CONF_PORT: 502,
                CONF_ADDRESS: 1,
                CONF_FRAME: "socket",
            },
        )
        assert result["type"] == "form"
        assert result["step_id"] == "device"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "Growatt",
                CONF_MODEL: "Model",
                CONF_TYPE: DeviceTypes.INVERTER_120,
                CONF_DC_STRING: 1,
                CONF_AC_PHASES: 1,
                CONF_SCAN_INTERVAL: 60,
                CONF_POWER_SCAN_ENABLED: False,
                CONF_POWER_SCAN_INTERVAL: 5,
                CONF_INVERTER_POWER_CONTROL: False,
            },
        )

    assert result["type"] == "create_entry"
    assert result["data"][CONF_SERIAL_NUMBER] == "abc123"
