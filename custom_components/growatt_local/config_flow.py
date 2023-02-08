"""Config flow for growatt server integration."""
import asyncio
import logging
import traceback
from asyncio.exceptions import TimeoutError
from typing import Optional
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

from .API.const import DeviceTypes
from .API.exception import ModbusPortException
from .API.growatt import GrowattModbusBase, GrowattSerial, GrowattNetwork

from .const import (
    CONF_AC_PHASES,
    CONF_DC_STRING,
    CONF_LAYER,
    CONF_SERIAL,
    CONF_TCP,
    CONF_UDP,
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

_LOGGER = logging.getLogger(__name__)


class GrowattLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow class."""

    VERSION = 1

    def __init__(self):
        """Initialise growatt server flow."""
        self.server: Optional[GrowattModbusBase] = None
        self.server_shared = False
        self.user_id = None
        self.data = {}
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
    def _async_show_serial_form(self, errors=None):
        """Show the serial form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_SERIAL_PORT): str,
                vol.Required(CONF_BAUDRATE, default=9600): int,
                vol.Required(CONF_STOPBITS, default=1): vol.In((0, 1, 2)),
                vol.Required(CONF_PARITY, default=ParityOptions.NONE): vol.In(
                    (
                        ParityOptions.NONE,
                        ParityOptions.EVEN,
                        ParityOptions.ODD,
                        ParityOptions.MARK,
                        ParityOptions.SPACE,
                    )
                ),
                vol.Required(CONF_BYTESIZE, default=8): vol.In((5, 6, 7, 8)),
            }
        )

        return self.async_show_form(
            step_id="serial", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_network_form(self, default_values=("", 502), errors=None):
        """Show the network form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_IP_ADDRESS, default=default_values[0]): str,
                vol.Required(CONF_PORT, default=default_values[1]): int,
            }
        )

        return self.async_show_form(
            step_id="network", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_device_form(
        self,
        default_values=(None, DeviceTypes.INVERTER.value, 60, False, 0),
        errors=None,
    ):
        """Show the device form to the user."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS, default=default_values[0]): int,
                vol.Required(
                    CONF_TYPE,
                    default=default_values[1],
                ): vol.In([DeviceTypes.INVERTER.value]),
                vol.Optional(CONF_SCAN_INTERVAL, default=default_values[2]): int,
                vol.Required(CONF_POWER_SCAN_ENABLED, default=default_values[3]): bool,
                vol.Optional(
                    CONF_POWER_SCAN_INTERVAL, default=default_values[4]
                ): int,
            }
        )

        return self.async_show_form(
            step_id="device", data_schema=data_schema, errors=errors
        )

    @callback
    def _async_show_inverter_form(
        self, name="", model="", strings=1, phases=1, errors=None
    ):
        """Show the inverter form to the user."""
        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=name): str,
                vol.Optional(CONF_MODEL, default=model): str,
                vol.Required(CONF_DC_STRING, default=strings): vol.In((1, 2)),
                vol.Required(CONF_AC_PHASES, default=phases): vol.In((1, 3)),
            }
        )

        return self.async_show_form(
            step_id="inverter", data_schema=data_schema, errors=errors
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

        if self.data[CONF_LAYER] == CONF_SERIAL and CONF_SERIAL_PORT in user_input:
            try:
                server = GrowattSerial(**user_input)
                await server.connect()
            except ModbusPortException:
                _LOGGER.error("ERROR", exc_info=True)
                return self._async_show_serial_form({CONF_SERIAL_PORT: "serial_port"})

            self.server = server

            self.data.update(user_input)
            return self._async_show_device_form()

    async def async_step_network(self, user_input=None) -> FlowResult:
        """Handle the network config flow."""
        if CONF_IP_ADDRESS in user_input:
            try:
                server = GrowattNetwork(
                    self.data[CONF_LAYER],
                    user_input[CONF_IP_ADDRESS],
                    user_input[CONF_PORT],
                    timeout=5,
                    retries=0,
                )
                await asyncio.wait_for(server.connect(), 3)
            except asyncio.TimeoutError:
                return self._async_show_network_form(
                    (user_input[CONF_IP_ADDRESS], user_input[CONF_PORT]),
                    {"base": "network_connection"},
                )
            except Exception as err:
                _LOGGER.error("ERROR", exc_info=err)
                return self._async_show_network_form(
                    (user_input[CONF_IP_ADDRESS], user_input[CONF_PORT]),
                    {"base": "network_custom"},
                )

            if not server.connected():
                server.close()
                return self._async_show_network_form(
                    (user_input[CONF_IP_ADDRESS], user_input[CONF_PORT]),
                    {"base": "network_connection"},
                )

            self.data.update(user_input)

            self.server = server

            return self._async_show_device_form()

    async def async_step_device(self, user_input=None) -> FlowResult:
        """Handle the device config flow."""

        if CONF_ADDRESS in user_input:
            try:
                if not self.force_next_page:
                    serial_number, model, firmware = await self.server.get_device_info(
                        user_input[CONF_ADDRESS]
                    )
                else:
                    # REMOVE WHEN FINISHED
                    serial_number, model, firmware = ("123456", "ABCD", "1.0")
            except TimeoutError:
                _LOGGER.warning(
                    "Device didn't respond on given address ID %s",
                    user_input[CONF_ADDRESS],
                )
                return self._async_show_device_form(
                    (
                        user_input[CONF_ADDRESS],
                        user_input[CONF_TYPE],
                        user_input[CONF_SCAN_INTERVAL],
                        user_input[CONF_POWER_SCAN_ENABLED],
                        user_input[CONF_POWER_SCAN_INTERVAL],
                    ),
                    {CONF_ADDRESS: "device_address", "base": "device_timeout"},
                )
            except ConnectionException:
                _LOGGER.error(
                    "Unexpected error when trying to get device info", exc_info=True
                )
                return self._async_show_device_form(
                    (
                        user_input[CONF_ADDRESS],
                        user_input[CONF_TYPE],
                        user_input[CONF_SCAN_INTERVAL],
                        user_input[CONF_POWER_SCAN_ENABLED],
                        user_input[CONF_POWER_SCAN_INTERVAL],
                    ),
                    {"base": "device_disconnect"},
                )

            self.data.update(user_input)
            self.data[CONF_SERIAL_NUMBER] = serial_number
            self.data[CONF_MODEL] = model
            self.data[CONF_FIRMWARE] = firmware

            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()

            await self.server.close()

            if user_input[CONF_TYPE] == DeviceTypes.INVERTER.value:
                return self._async_show_inverter_form(
                    user_input[CONF_TYPE].capitalize(), model
                )

    async def async_step_inverter(self, user_input=None) -> FlowResult:
        """Handle the inverter config flow."""

        if CONF_SERIAL_NUMBER in self.data:
            self.data.update(user_input)

            return self.async_create_entry(
                title=f"Growatt {self.data[CONF_MODEL]}", data=self.data
            )
