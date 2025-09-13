import socket
from datetime import timedelta

import pytest
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer import FramerType

from custom_components.growatt_local import GrowattLocalCoordinator
from custom_components.growatt_local.API.const import DeviceTypes
from custom_components.growatt_local.API.utils import RegisterKeys
from testing.modbus_simulator import start_simulator


@pytest.fixture(scope="session")
async def modbus_simulator():
    sock = socket.socket()
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    async with start_simulator(port) as (host, port):
        yield {"host": host, "port": port}


class MockGrowattDevice:
    device = DeviceTypes.INVERTER_120

    def __init__(self, host: str, port: int):
        self._client = AsyncModbusTcpClient(host, port=port, framer=FramerType.SOCKET)

    async def connect(self):
        await self._client.connect()

    async def update(self, keys):
        # Deterministic value for tests; mimics two 16-bit registers (1,2)
        return {"input_power": (1 << 16) | 2}

    def status(self, data):
        return "online"

    def get_register_names(self):
        return {"input_power"}

    def get_keys_by_name(self, names):
        return RegisterKeys(input={1, 2})


@pytest.fixture
async def mock_growatt_device(modbus_simulator):
    device = MockGrowattDevice(modbus_simulator["host"], modbus_simulator["port"])
    await device.connect()
    return device


@pytest.fixture
def coordinator(hass, mock_growatt_device):
    return GrowattLocalCoordinator(hass, mock_growatt_device, timedelta(seconds=60))


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture(autouse=True)
def expected_lingering_timers():
    return True


def pytest_configure(config):
    try:
        import pytest_socket
        socket.socket = pytest_socket._true_socket
    except Exception:  # pragma: no cover
        pass


def pytest_load_initial_conftests(early_config, parser, args):
    try:
        import pytest_socket
        socket.socket = pytest_socket._true_socket
    except Exception:  # pragma: no cover
        pass
