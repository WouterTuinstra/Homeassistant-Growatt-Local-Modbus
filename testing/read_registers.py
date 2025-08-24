import asyncio, sys, types, importlib.util, os
from pathlib import Path


# Find project root by searching upwards for custom_components
def find_project_root(start: Path) -> Path:
    cur = start.resolve()
    while not (cur / "custom_components").is_dir():
        if cur.parent == cur:
            raise RuntimeError("Could not find project root containing custom_components")
        cur = cur.parent
    return cur

ROOT = find_project_root(Path(__file__).parent)
CC_DIR   = ROOT / "custom_components"
GL_DIR   = CC_DIR / "growatt_local"
API_DIR  = GL_DIR / "API"
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
    spec = importlib.util.spec_from_file_location(f"custom_components.growatt_local.API.{name}", p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

growatt = import_api("growatt")
utils   = import_api("utils")

# ---- Serial config (auto-detect by-id, fallback to ttyUSB0) ----
byid = Path("/dev/serial/by-id")
DEFAULT_PORT = "/dev/ttyUSB0"
SERIAL_PORT = os.environ.get("SERIAL_PORT")
if not SERIAL_PORT:
    SERIAL_PORT = str(next(byid.glob("*"), Path(DEFAULT_PORT))) if byid.exists() else DEFAULT_PORT

BAUDRATE       = 115200
STOPBITS       = 1
PARITY         = "N"
BYTESIZE       = 8
MODBUS_ADDRESS = 1
DEVICE_TYPE    = growatt.DeviceTypes.HYBRID_120_TL_XH
# ---------------------------------------------------------------

async def main():
    dev = growatt.GrowattDevice(
        growatt.GrowattSerial(
            SERIAL_PORT,
            baudrate=BAUDRATE,
            stopbits=STOPBITS,
            parity=PARITY,
            bytesize=BYTESIZE,
        ),
        DEVICE_TYPE,
        MODBUS_ADDRESS,
    )
    await dev.connect()
    # Read a small TL-XH window to verify comms
    keys = utils.RegisterKeys(input=set(range(3000, 3010)))
    res = await dev.update(keys)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
    