"""The Growatt server PV inverter sensor integration."""
import asyncio
from datetime import date, timedelta
import logging
from collections.abc import Callable, Sequence
from typing import Any, Optional

from pymodbus.exceptions import ConnectionException

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.sun import get_astral_event_next
from homeassistant.util import dt as dt_util
from homeassistant.const import (
    CONF_ADDRESS,
    CONF_IP_ADDRESS,
    CONF_MODEL,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TYPE,
    SUN_EVENT_SUNRISE,
    SUN_EVENT_SUNSET,
)

from homeassistant.helpers.event import (
    async_track_sunrise,
    async_track_sunset,
    async_track_time_change,
)

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_LAYER,
    CONF_SERIAL,
    CONF_SERIAL_NUMBER,
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
    DOMAIN,
    PLATFORMS,
)

from .API.const import DeviceTypes
from .API.growatt import GrowattDevice, GrowattSerial, GrowattNetwork


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Load the saved entities."""

    if entry.data[CONF_LAYER] == CONF_SERIAL:
        device_layer = GrowattSerial(
            entry.data[CONF_SERIAL_PORT],
            entry.data[CONF_BAUDRATE],
            entry.data[CONF_STOPBITS],
            entry.data[CONF_PARITY],
            entry.data[CONF_BYTESIZE],
        )
    elif entry.data[CONF_LAYER] in (CONF_TCP, CONF_UDP):
        device_layer = GrowattNetwork(
            entry.data[CONF_LAYER],
            entry.data[CONF_IP_ADDRESS],
            entry.data[CONF_PORT],
            entry.data[CONF_FRAME],
        )
    else:
        _LOGGER.warning(
            "Device layer %s is not supported right now",
            entry.data[CONF_LAYER],
        )
        return False

    device = GrowattDevice(
        device_layer, DeviceTypes(entry.data[CONF_TYPE]), entry.data[CONF_ADDRESS]
    )

    await device.connect()

    coordinator = GrowattLocalCoordinator(
        hass,
        device,
        timedelta(seconds=entry.data[CONF_SCAN_INTERVAL]),
        timedelta(seconds=entry.data[CONF_POWER_SCAN_INTERVAL])
        if entry.data[CONF_POWER_SCAN_ENABLED]
        else None,
    )

    hass.data.setdefault(DOMAIN, {})[entry.data[CONF_SERIAL_NUMBER]] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    hass.data[DOMAIN][entry.data[CONF_SERIAL_NUMBER]].growatt_api.close()

    if unload_ok:
        del hass.data[DOMAIN][entry.data[CONF_SERIAL_NUMBER]]
    return unload_ok


class GrowattLocalCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        growatt_api: GrowattDevice,
        update_interval: timedelta,
        power_interval: Optional[timedelta] = None,
    ) -> None:
        """Initialize my coordinator."""
        self.interval = power_interval if power_interval else update_interval
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=self.interval,
        )
        self.data = {}
        self.growatt_api = growatt_api
        self._failed_update_count = 0
        self.keys = set()
        self.p_keys = set()
        self._midnight_listeners: dict[
            CALLBACK_TYPE, tuple[CALLBACK_TYPE, object | None]
        ] = {}

        if power_interval:
            self._counter = self._max_counter = update_interval / power_interval
        else:
            self._counter = self._max_counter = 0

        self._sun_is_down = self.sun_down()

        async_track_sunrise(self.hass, self.sunrise)
        async_track_sunset(self.hass, self.sunset, timedelta(minutes=-10))

        async_track_time_change(self.hass, self.midnight, 0, 0, 0)

    @callback
    def async_update_listeners(self) -> None:
        """Update only the registered listeners for which we have new data."""
        for update_callback, context in set(self._listeners.values()):
            if context in self.data.keys():
                update_callback()

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        status = None
        data = {}

        if self._sun_is_down:
            return {"status": "Offline"}

        try:
            if self._counter >= self._max_counter or self._failed_update_count > 0:
                self._counter = 0
                data = await self.growatt_api.update(self.keys)
            else:
                self._counter += 1
                data = await self.growatt_api.update(self.p_keys)
            self._failed_update_count = 0
        except ConnectionException:
            if self._failed_update_count % 60 == 0:
                _LOGGER.warning("Modbus connection got interupted retrying to reconnect", exc_info=True)
                await self.growatt_api.connect()
            self._failed_update_count += 1
            status = "not_connected"
        except asyncio.TimeoutError:
            self._failed_update_count += 1
            status = "no_response"

        if status is None:
            status = self.growatt_api.status(data)

        if status:
            data["status"] = status

        return data

    async def sunrise(self):
        """Callback function when sunrise occours."""
        _LOGGER.info("System waking up on sunrise")
        self.update_interval = self.interval
        self._sun_is_down = False
        await self.async_request_refresh()

    async def sunset(self):
        """Callback function when sunset occours."""
        _LOGGER.info("System going into sleep mode")
        self._sun_is_down = True
        await self.async_request_refresh()
        self.update_interval = timedelta(hours=1)
        self._failed_update_count = 0
        self._counter = 0

    def sun_down(self) -> bool:
        """Customized datetimes and inversion for the implemented sun_up function of home assistant"""

        utc_point_in_time = dt_util.utcnow()

        next_sunrise = get_astral_event_next(
            self.hass, SUN_EVENT_SUNRISE, utc_point_in_time + timedelta(minutes=5)
        )
        next_sunset = get_astral_event_next(
            self.hass, SUN_EVENT_SUNSET, utc_point_in_time + timedelta(minutes=15)
        )

        return next_sunrise < next_sunset

    @callback
    def midnight(self, datetime=None):
        for update_callback, context in set(self._midnight_listeners.values()):
            self.data.update({context: 0})
            update_callback()

    @callback
    def async_add_midnight_listener(
        self, update_callback: CALLBACK_TYPE, context: Any = None
    ) -> Callable[[], None]:
        """Listeners for midnight update."""
        schedule_refresh = not self._midnight_listeners

        @callback
        def remove_midnight_listener() -> None:
            """Remove midnight listener."""
            self._midnight_listeners.pop(remove_midnight_listener)
            if not self._midnight_listeners:
                # determine if time track can be removed
                pass

        self._midnight_listeners[remove_midnight_listener] = (update_callback, context)

        # This is the first listener, set up interval.
        if schedule_refresh:
            async_track_time_change(self.hass, self.midnight, 0, 0, 0)

        return remove_midnight_listener

    @callback
    def get_keys_by_name(
        self, names: Sequence[str], update_keys: bool = False
    ) -> set[int]:
        """
        Loopup modbus register values based on name.
        Setting update_keys automaticly extends the list of keys to request.
        """
        keys = self.growatt_api.get_keys_by_name(names)
        if update_keys:
            self.keys.update(keys)

        return keys
