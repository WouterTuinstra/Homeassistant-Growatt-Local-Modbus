"""Config flow for growatt server integration."""
import asyncio
import logging
import traceback
from asyncio.exceptions import TimeoutError
from typing import Any
import voluptuous as vol

from pymodbus.exceptions import ConnectionException

from homeassistant import config_entries

from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_ADDRESS,
    CONF_TYPE,
    CONF_SCAN_INTERVAL,
    CONF_MODEL,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .API.const import DeviceTypes
from .API.exception import ModbusPortException
from .API.growatt import GrowattModbusBase, GrowattSerial, GrowattNetwork, get_device_info
from .API.device_type.base import GrowattDeviceInfo

from .const import (
    CONF_AC_PHASES,
    CONF_DC_STRING,
    CONF_LAYER,
    CONF_SERIAL,
    CONF_TCP,
    CONF_UDP,
    CONF_FRAME,
    CONF_SERIAL_PORT,
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_PARITY,
    CONF_STOPBITS,
    CONF_POWER_SCAN_ENABLED,
    CONF_POWER_SCAN_INTERVAL,
    CONF_SERIAL_NUMBER,
    CONF_FIRMWARE,
    ParityOptions,
    DOMAIN,
)

PARITY_OPTION = [
    selector.SelectOptionDict(value=ParityOptions.NONE, label=ParityOptions.NONE),
    selector.SelectOptionDict(value=ParityOptions.EVEN, label=ParityOptions.EVEN),
    selector.SelectOptionDict(value=ParityOptions.ODD, label=ParityOptions.ODD),
    selector.SelectOptionDict(value=ParityOptions.MARK, label=ParityOptions.MARK),
    selector.SelectOptionDict(value=ParityOptions.SPACE, label=ParityOptions.SPACE),
]

MODBUS_FRAMER_OPTION = [
    selector.SelectOptionDict(value='rtu', label='Modbus RTU'),
    selector.SelectOptionDict(value='socket', label='Modbus TCP'),
]

DEVICETYPES_OPTION = [
    selector.SelectOptionDict(value=DeviceTypes.INVERTER_120, label="RTU 2 - Inverter v1.24"),
    selector.SelectOptionDict(value=DeviceTypes.INVERTER_315, label="RTU - Inverter v3.15"),
]

_LOGGER = logging.getLogger(__name__)


class GrowattLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow class."""

    VERSION = 1

    def __init__(self):
        """Initialise growatt server flow."""
        self.server: GrowattModbusBase | None = None
        self.user_id = None
        self.data: dict[str, Any] = {}
        self.force_next_page = False

    @callback
    def _async_show_selection_form(self, errors=None):
        """Show the initial form to the user to select protocol."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_LAYER, default=CONF_SERIAL): vol.In(
                    [CONF_SERIAL, CONF_TCP, CONF_UDP]
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_serial_form(self, default_values=(None, 9600, 1, ParityOptions.NONE, 8, None), errors=None):
        """Show the serial form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_SERIAL_PORT, default=default_values[0]): str,
                vol.Required(CONF_BAUDRATE, default=default_values[1]): int,
                vol.Required(CONF_STOPBITS, default=default_values[2]): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0,
                        max=2,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),
                vol.Required(CONF_PARITY, default=default_values[3]): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=PARITY_OPTION, mode=selector.SelectSelectorMode.DROPDOWN
                    ),
                ),
                vol.Required(CONF_BYTESIZE, default=default_values[4]): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=5,
                        max=8,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),
                vol.Required(CONF_ADDRESS, default=default_values[5]): int,
            }
        )

        return self.async_show_form(
            step_id="serial", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_network_form(self, default_values=("", 502, None, 'socket'), errors=None):
        """Show the network form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_IP_ADDRESS, default=default_values[0]): str,
                vol.Required(CONF_PORT, default=default_values[1]): int,
                vol.Required(CONF_ADDRESS, default=default_values[2]): int,
                vol.Required(CONF_FRAME, default=default_values[3]): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=MODBUS_FRAMER_OPTION, mode=selector.SelectSelectorMode.DROPDOWN
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="network", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_device_form(
        self,
        name: str = "",
        model: str = "",
        device_type: str = DeviceTypes.INVERTER_120,
        mppt_trackers: int = 1,
        grid_phases: int = 1,
        modbus_version: float | str = "Not supported, Check logs for device info",
        detected_type: str = "unknown",
        scan_interval: int = 60,
        power_scan_enabled: bool = False,
        power_scan_interval: int = 5,
        errors=None,
    ):
        """Show the device form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=name): str,
                vol.Required(CONF_MODEL, default=model): str,
                vol.Required(CONF_TYPE, default=device_type,): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=DEVICETYPES_OPTION
                    ),
                ),
                vol.Required(CONF_DC_STRING, default=mppt_trackers): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=8,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),
                vol.Required(CONF_AC_PHASES, default=grid_phases): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=3,
                        step=2,
                        mode=selector.NumberSelectorMode.BOX,
                    ),
                ),
                vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): int,
                vol.Required(CONF_POWER_SCAN_ENABLED, default=power_scan_enabled): bool,
                vol.Optional(
                    CONF_POWER_SCAN_INTERVAL, default=power_scan_interval
                ): int,
            }
        )

        return self.async_show_form(
            step_id="device",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "modbus_version": modbus_version,
                "device_type": detected_type
            }
        )

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the start of the config flow."""
        if user_input is None:
            return self._async_show_selection_form()

        if CONF_LAYER in user_input:
            self.data = user_input
            if user_input[CONF_LAYER] == CONF_SERIAL:
                return self._async_show_serial_form()
            else:
                return self._async_show_network_form()

    async def async_step_serial(self, user_input=None) -> FlowResult:
        """Handle the serial config flow."""

        if self.data[CONF_LAYER] == CONF_SERIAL and user_input is None:
            return self._async_show_serial_form()

        if user_input is not None and CONF_SERIAL_PORT in user_input:
            try:
                server = GrowattSerial(
                    user_input[CONF_SERIAL_PORT],
                    user_input[CONF_BAUDRATE],
                    user_input[CONF_STOPBITS],
                    user_input[CONF_PARITY],
                    user_input[CONF_BYTESIZE]
                )
                await server.connect()
            except ModbusPortException:
                _LOGGER.error("ERROR", exc_info=True)
                return self._async_show_serial_form(
                    default_values=(
                        user_input[CONF_SERIAL_PORT],
                        user_input[CONF_BAUDRATE],
                        user_input[CONF_STOPBITS],
                        user_input[CONF_PARITY],
                        user_input[CONF_BYTESIZE],
                        user_input[CONF_ADDRESS],
                    ),
                    errors={CONF_SERIAL_PORT: "serial_port"})

            try:
                device_info = await get_device_info(server, user_input[CONF_ADDRESS])
            except TimeoutError:
                _LOGGER.warning(
                    "Device didn't respond on given address ID %s",
                    user_input[CONF_ADDRESS],
                )
                return self._async_show_serial_form(
                    default_values=(
                        user_input[CONF_SERIAL_PORT],
                        user_input[CONF_BAUDRATE],
                        user_input[CONF_STOPBITS],
                        user_input[CONF_PARITY],
                        user_input[CONF_BYTESIZE],
                        user_input[CONF_ADDRESS],
                    ),
                    errors={CONF_ADDRESS: "device_address", "base": "device_timeout"},
                )
            except ConnectionException:
                _LOGGER.error(
                    "Unexpected error when trying to get device info", exc_info=True
                )
                return self._async_show_serial_form(
                    default_values=(
                        user_input[CONF_SERIAL_PORT],
                        user_input[CONF_BAUDRATE],
                        user_input[CONF_STOPBITS],
                        user_input[CONF_PARITY],
                        user_input[CONF_BYTESIZE],
                        user_input[CONF_ADDRESS],
                    ),
                    errors={"base": "device_disconnect"},
                )
            finally:
                server.close()

            self.server = server
            self.data.update(user_input)

            if device_info:
                return self._async_show_device_form(
                    model=device_info.model,
                    device_type=device_info.device_type,
                    mppt_trackers=device_info.mppt_trackers,
                    grid_phases=device_info.grid_phases,
                    modbus_version=device_info.modbus_version,
                    detected_type=device_info.device_type
                )
            else:
                return self._async_show_device_form()

    async def async_step_network(self, user_input=None) -> FlowResult:
        """Handle the network config flow."""
        if user_input is not None and CONF_IP_ADDRESS in user_input:
            try:
                server = GrowattNetwork(
                    self.data[CONF_LAYER],
                    user_input[CONF_IP_ADDRESS],
                    user_input[CONF_PORT],
                    user_input[CONF_FRAME],
                    timeout=5,
                    retries=0,
                )
                await asyncio.wait_for(server.connect(), 3)
            except asyncio.TimeoutError:
                return self._async_show_network_form(
                    default_values=(
                        user_input[CONF_IP_ADDRESS],
                        user_input[CONF_PORT],
                        user_input[CONF_ADDRESS],
                        user_input[CONF_FRAME]
                    ),
                    errors={"base": "network_connection"},
                )
            except Exception as err:
                _LOGGER.error("ERROR", exc_info=err)
                return self._async_show_network_form(
                    default_values=(
                        user_input[CONF_IP_ADDRESS],
                        user_input[CONF_PORT],
                        user_input[CONF_ADDRESS],
                        user_input[CONF_FRAME]
                    ),
                    errors={"base": "network_custom"},
                )

            if not server.connected():
                server.close()
                return self._async_show_network_form(
                    default_values=(
                        user_input[CONF_IP_ADDRESS],
                        user_input[CONF_PORT],
                        user_input[CONF_ADDRESS],
                        user_input[CONF_FRAME]
                    ),
                    errors={"base": "network_connection"},
                )

            try:
                device_info = None
                if not self.force_next_page:
                    device_info = await get_device_info(server, user_input[CONF_ADDRESS])
            except TimeoutError:
                _LOGGER.warning(
                    "Device didn't respond on given address ID %s",
                    user_input[CONF_ADDRESS],
                )
                return self._async_show_network_form(
                    default_values=(
                        user_input[CONF_IP_ADDRESS],
                        user_input[CONF_PORT],
                        user_input[CONF_ADDRESS],
                        user_input[CONF_FRAME]
                    ),
                    errors={CONF_ADDRESS: "device_address", "base": "device_timeout"},
                )
            except ConnectionException:
                _LOGGER.error(
                    "Unexpected error when trying to get device info", exc_info=True
                )
                return self._async_show_network_form(
                    default_values=(
                        user_input[CONF_IP_ADDRESS],
                        user_input[CONF_PORT],
                        user_input[CONF_ADDRESS],
                        user_input[CONF_FRAME]
                    ),
                    errors={"base": "device_disconnect"},
                )
            finally:
                server.close()

            self.server = server
            self.data.update(user_input)

            if device_info:
                return self._async_show_device_form(
                    model=device_info.model,
                    device_type=device_info.device_type,
                    mppt_trackers=device_info.mppt_trackers,
                    grid_phases=device_info.grid_phases,
                    modbus_version=device_info.modbus_version,
                    detected_type=device_info.device_type
                )
            else:
                return self._async_show_device_form()

    async def async_step_device(self, user_input=None) -> FlowResult:
        """Handle the device config flow."""

        if user_input is None:
            return self._async_show_device_form()

        device_info = None
        if self.server and user_input is not None:
            await self.server.connect()
            try:
                device_info = await get_device_info(
                    self.server, self.data[CONF_ADDRESS], user_input[CONF_TYPE]
                )
            except TimeoutError:
                _LOGGER.warning(
                    "Device didn't respond on given address ID %s",
                    self.data[CONF_ADDRESS],
                )
                return self._async_show_device_form(
                    name=user_input[CONF_NAME],
                    model=user_input[CONF_MODEL],
                    device_type=user_input[CONF_TYPE],
                    mppt_trackers=user_input[CONF_DC_STRING],
                    grid_phases=user_input[CONF_AC_PHASES],
                    scan_interval=user_input[CONF_SCAN_INTERVAL],
                    power_scan_enabled=user_input[CONF_POWER_SCAN_ENABLED],
                    power_scan_interval=user_input[CONF_POWER_SCAN_INTERVAL],
                    errors={"base": "device_timeout"},
                )
            except ConnectionException:
                _LOGGER.error(
                    "Unexpected error when trying to get device info", exc_info=True
                )
                return self._async_show_device_form(
                    name=user_input[CONF_NAME],
                    model=user_input[CONF_MODEL],
                    device_type=user_input[CONF_TYPE],
                    mppt_trackers=user_input[CONF_DC_STRING],
                    grid_phases=user_input[CONF_AC_PHASES],
                    scan_interval=user_input[CONF_SCAN_INTERVAL],
                    power_scan_enabled=user_input[CONF_POWER_SCAN_ENABLED],
                    power_scan_interval=user_input[CONF_POWER_SCAN_INTERVAL],
                    errors={"base": "device_disconnect"},
                )
            finally:
                self.server.close()

        if device_info is None:
            return self._async_show_device_form(
                name=user_input[CONF_NAME],
                model=user_input[CONF_MODEL],
                device_type=user_input[CONF_TYPE],
                mppt_trackers=user_input[CONF_DC_STRING],
                grid_phases=user_input[CONF_AC_PHASES],
                scan_interval=user_input[CONF_SCAN_INTERVAL],
                power_scan_enabled=user_input[CONF_POWER_SCAN_ENABLED],
                power_scan_interval=user_input[CONF_POWER_SCAN_INTERVAL],
                errors={"base": "device_type"},
            )

        await self.async_set_unique_id(device_info.serial_number)
        self._abort_if_unique_id_configured()

        self.data[CONF_SERIAL_NUMBER] = device_info.serial_number
        self.data[CONF_FIRMWARE] = device_info.firmware

        self.data.update(user_input)

        return self.async_create_entry(
            title=f"Growatt {self.data[CONF_MODEL]}", data=self.data
        )
