import asyncio, sys, types, importlib.util, os
from pathlib import Path

"""

This script allows you to read Modbus registers from a Growatt inverter using the
Growatt Local Modbus integration. It is intended for debugging and exploring
the available registers on your device.

"""

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

    ranges = [
        (0, 124),
        (3000, 3124),
        (3125, 3249),
        (3250, 3374),
    ]
    reg_map = dev.input_register

    for start, end in ranges:
        print(f"\n=== Scanning registers {start}~{end} ===")
        keys = utils.RegisterKeys(input=set(range(start, end + 1)))
        res = await dev.update(keys)
        print("{:<10} {:<30} {:<15}".format("Address", "Name", "Value"))
        print("-" * 60)
        # Build reverse lookup: name -> address for defined registers
        name_to_addr = {reg.name: addr for addr, reg in reg_map.items() if reg}
        # Print all addresses in the range
        for addr in sorted(keys.input):
            reg = reg_map.get(addr)
            if reg:
                name = reg.name
                value = res.get(name, "-")
            else:
                # Try to get value by address if not defined
                # The result dict uses names for defined, but for undefined, try raw register value
                value = None
                # Try to find a value by scanning the result dict for int values
                for v in res.values():
                    if isinstance(v, dict) and addr in v:
                        value = v[addr]
                        break
                if value is None:
                    value = "-"
                name = "?"
            print(f"{addr:<10} {name:<30} {value:<15}")

if __name__ == "__main__":
    asyncio.run(main())
    