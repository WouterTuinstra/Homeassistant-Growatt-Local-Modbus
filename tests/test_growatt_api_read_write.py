"""Regression test for reading and writing simulated registers using the Growatt API module.
Catches issues with write_register argument handling and verifies round-trip values.
"""

import asyncio
import pytest
from pathlib import Path
import sys
import types
import importlib.util

pytestmark = pytest.mark.enable_socket

# Dynamically import the Growatt API from the local repo
ROOT = Path(__file__).parent.parent
CC_DIR = ROOT / "custom_components"
GL_DIR = CC_DIR / "growatt_local"
API_DIR = GL_DIR / "API"
(API_DIR / "__init__.py").touch(exist_ok=True)


def ensure_pkg(name: str, path: Path):
    mod = sys.modules.get(name)
    if mod is None:
        mod = types.ModuleType(name)
        sys.modules[name] = mod
    mod.__path__ = [str(path)]
    return mod


ensure_pkg("custom_components", CC_DIR)
ensure_pkg("custom_components.growatt_local", GL_DIR)
ensure_pkg("custom_components.growatt_local.API", API_DIR)


def import_api(name: str):
    p = API_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(
        f"custom_components.growatt_local.API.{name}", p
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


growatt = import_api("growatt")
utils = import_api("utils")


import socket
from testing.modbus_simulator import start_simulator


@pytest.mark.asyncio
async def test_growatt_api_read_write():
    """Test reading and writing a simulated register using Growatt API over TCP."""
    # Find free port
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()

    async with start_simulator(port=port, force_deterministic=True) as (
        host,
        real_port,
    ):
        # Set up GrowattDevice using TCP
        modbus = growatt.GrowattNetwork("tcp", host, port=real_port)
        device = growatt.GrowattDevice(
            modbus,
            growatt.DeviceTypes.HYBRID_120_TL_XH,
            1,
        )
        await device.connect()
        # Pick a register to test (use register 0 for on/off)
        reg_addr = 0
        # Read initial value
        keys = utils.RegisterKeys(holding={reg_addr})
        result = await device.update(keys)
        initial = result.get("Remote On/Off", None)
        # Write a new value (toggle)
        new_val = 1 if initial == 0 else 0
        # Try writing using the API
        try:
            await device.write_register(reg_addr, [new_val])
        except TypeError as e:
            pytest.fail(f"TypeError in write_register: {e}")
        # Read back and verify
        result2 = await device.update(keys)
        after = result2.get("Remote On/Off", None)
        assert after == new_val, f"Write did not persist: wrote {new_val}, got {after}"
        # Try writing with extra kwargs to catch argument errors
        with pytest.raises(TypeError):
            await device.write_register(reg_addr, [new_val], slave=1)
        # Clean up
        device.close()
