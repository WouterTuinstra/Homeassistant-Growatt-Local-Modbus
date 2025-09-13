import pytest
from datetime import timedelta

from custom_components.growatt_local import GrowattLocalCoordinator
from custom_components.growatt_local.API.const import DeviceTypes
from custom_components.growatt_local.API.utils import RegisterKeys


@pytest.fixture
def hass_instance(hass):
    """Return Home Assistant instance for tests."""
    return hass


class MockGrowattDevice:
    device = DeviceTypes.INVERTER_120

    async def connect(self):
        return None

    async def update(self, keys):
        return {"input_power": 0}

    def status(self, data):
        return "online"

    def get_register_names(self):
        return {"input_power"}

    def get_keys_by_name(self, names):
        return RegisterKeys()


@pytest.fixture
def mock_growatt_device():
    """Return a mocked Growatt device."""
    return MockGrowattDevice()


@pytest.fixture
def coordinator(hass, mock_growatt_device):
    """Coordinator using the mocked device."""
    return GrowattLocalCoordinator(hass, mock_growatt_device, timedelta(seconds=60))


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations loaded from this repository."""
    yield


@pytest.fixture(autouse=True)
def expected_lingering_timers():
    """Allow lingering timers during shutdown."""
    return True
