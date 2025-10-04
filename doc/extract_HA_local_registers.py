#!/usr/bin/env python3
"""Extract register mappings from the growatt_local integration.

The script imports the device type modules used by the Home Assistant
``growatt_local`` integration and serialises their ``GrowattDeviceRegisters``
collections into a machine-readable JSON snapshot.  This serves as a
lossless export of the integration's current Modbus mapping so that other
consolidation tooling can consume it without importing the integration code
itself.
"""
from __future__ import annotations

import importlib
import inspect
import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

DOC_DIR = Path(__file__).resolve().parent
REPO_ROOT = DOC_DIR.parent
HA_CORE_ROOT = REPO_ROOT.parent.parent

for managed_path in (str(HA_CORE_ROOT), str(REPO_ROOT)):
    try:
        sys.path.remove(managed_path)
    except ValueError:
        pass

sys.path.insert(0, str(HA_CORE_ROOT))
sys.path.insert(1, str(REPO_ROOT))

# Ensure any previous import of the stub homeassistant module is cleared so that
# the real Home Assistant package from ``HA_CORE_ROOT`` is used.
sys.modules.pop("homeassistant", None)

from custom_components.growatt_local.API.device_type.base import (  # noqa: E402
    GrowattDeviceRegisters,
    custom_function,
)

OUTPUT_PATH = DOC_DIR / "HA_local_registers.json"

FUNCTION_USAGE: dict[str, list[dict[str, Any]]] = {}
FUNCTION_OBJECTS: dict[str, Any] = {}

EXCLUDED_DEVICE_IDS: set[str] = {"tl3", "offgrid"}

DEVICE_SPECS: dict[str, dict[str, Any]] = {
    "tlx": {
        "module": "custom_components.growatt_local.API.device_type.inverter_120",
        "groups": {
            "holding_common": "HOLDING_REGISTERS_120",
            "input_common": "INPUT_REGISTERS_120",
            "input_tl_xh": "INPUT_REGISTERS_120_TL_XH",
        },
    },
    "storage": {
        "module": "custom_components.growatt_local.API.device_type.storage_120",
        "groups": {
            "holding_common": "STORAGE_HOLDING_REGISTERS_120",
            "holding_tl_xh": "STORAGE_HOLDING_REGISTERS_120_TL_XH",
            "input_common": "STORAGE_INPUT_REGISTERS_120",
            "input_tl_xh": "STORAGE_INPUT_REGISTERS_120_TL_XH",
        },
    },
}


def describe_value_type(value_type: type) -> str:
    """Return a readable identifier for the register value type."""

    if value_type is custom_function:
        return "custom_function"
    if value_type.__module__ == "builtins":
        return value_type.__name__
    return f"{value_type.__module__}.{value_type.__name__}"


def _normalise_for_json(value: Any) -> Any:
    """Recursively convert values into JSON-serialisable primitives."""

    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_normalise_for_json(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalise_for_json(val) for key, val in value.items()}
    return value


def serialise_register(
    register: GrowattDeviceRegisters,
    *,
    device: str,
    group: str,
) -> dict[str, Any]:
    """Convert a ``GrowattDeviceRegisters`` instance into JSON-friendly data."""

    function_name: str | None = None
    function_path: str | None = None
    if register.function is not None:
        function_name = getattr(register.function, "__qualname__", register.function.__name__)
        function_path = f"{register.function.__module__}.{function_name}"
        FUNCTION_OBJECTS.setdefault(function_path, register.function)
        FUNCTION_USAGE.setdefault(function_path, []).append(
            {
                "device": device,
                "group": group,
                "register": register.register,
                "name": register.name,
            }
        )

    return {
        "name": register.name,
        "register": register.register,
        "length": register.length,
        "scale": register.scale,
        "read_write": bool(register.read_write),
        "value_type": describe_value_type(register.value_type),
        "function": function_name,
        "function_path": function_path,
    }


def extract_group(
    module: Any,
    attribute: str,
    *,
    device: str,
    group: str,
) -> list[dict[str, Any]]:
    """Fetch and serialise a register group from the given module."""

    try:
        value = getattr(module, attribute)
    except AttributeError as err:  # pragma: no cover - defensive
        raise SystemExit(f"Module {module.__name__} is missing attribute {attribute}") from err

    if not isinstance(value, (tuple, list)):
        raise SystemExit(
            f"Attribute {attribute} on {module.__name__} is not a tuple/list of GrowattDeviceRegisters"
        )

    serialised: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, GrowattDeviceRegisters):
            raise SystemExit(
                f"Attribute {attribute} on {module.__name__} contains unexpected item {item!r}"
            )
        serialised.append(
            serialise_register(item, device=device, group=group)
        )

    serialised.sort(key=lambda entry: (entry["register"], entry["name"]))
    return serialised


def describe_function(path: str, func: Any) -> dict[str, Any]:
    """Capture metadata about a decoder/helper function used by the integration."""

    details: dict[str, Any] = {
        "module": func.__module__,
        "qualname": getattr(func, "__qualname__", getattr(func, "__name__", path.split(".")[-1])),
        "doc": inspect.getdoc(func),
        "signature": None,
        "defined_in": None,
        "usage": FUNCTION_USAGE.get(path, []),
    }

    try:
        details["signature"] = str(inspect.signature(func))
    except (TypeError, ValueError):
        details["signature"] = None

    try:
        source_file = inspect.getsourcefile(func)
        if source_file:
            rel_path = Path(source_file).resolve()
            try:
                rel_path = rel_path.relative_to(REPO_ROOT)
            except ValueError:
                pass
            details["defined_in"] = str(rel_path)
    except (OSError, TypeError):
        details["defined_in"] = None

    return details


def collect_function_metadata() -> dict[str, Any]:
    """Return metadata for all custom decoder functions referenced by registers."""

    return {
        path: describe_function(path, func)
        for path, func in sorted(FUNCTION_OBJECTS.items())
    }


def collect_enum_metadata() -> dict[str, Any]:
    """Extract enumerations and lookup tables defined by the integration."""

    metadata: dict[str, Any] = {}

    base_module = importlib.import_module(
        "custom_components.growatt_local.API.device_type.base"
    )
    for attr, key in (
        ("DEVICE_TYPE_CODES", "device_type_codes"),
        ("INVERTER_DERATINGMODES", "inverter_derating_modes"),
        ("INVERTER_WARNINGCODES", "inverter_warning_codes"),
        ("INVERTER_FAULTCODES", "inverter_fault_codes"),
    ):
        value = getattr(base_module, attr, None)
        if value is not None:
            metadata[key] = _normalise_for_json(value)

    if "offgrid" not in EXCLUDED_DEVICE_IDS:
        offgrid_module = importlib.import_module(
            "custom_components.growatt_local.API.device_type.offgrid"
        )
        offgrid_status = getattr(offgrid_module, "OffgridStatus", None)
        if isinstance(offgrid_status, type) and issubclass(offgrid_status, Enum):
            metadata["offgrid_status"] = {
                member.name: member.value
                for member in offgrid_status  # type: ignore[call-overload]
            }
        for attr, key in (
            ("OFFGRID_WARNINGCODES", "offgrid_warning_codes"),
            ("OFFGRID_FAULTCODES", "offgrid_fault_codes"),
        ):
            value = getattr(offgrid_module, attr, None)
            if value is not None:
                metadata[key] = _normalise_for_json(value)

    return metadata


SENSOR_MODULE_SPECS = {
    "inverter": (
        "custom_components.growatt_local.sensor_types.inverter",
        "INVERTER_SENSOR_TYPES",
    ),
    "storage": (
        "custom_components.growatt_local.sensor_types.storage",
        "STORAGE_SENSOR_TYPES",
    ),
    "offgrid": (
        "custom_components.growatt_local.sensor_types.offgrid",
        "OFFGRID_SENSOR_TYPES",
    ),
}


def serialise_sensor_description(description: Any) -> dict[str, Any]:
    """Convert a Growatt sensor entity description to JSON-safe data."""

    if is_dataclass(description):
        data = asdict(description)
    else:
        data = dict(description.__dict__)

    return {key: _normalise_for_json(value) for key, value in data.items()}


def collect_sensor_metadata() -> dict[str, list[dict[str, Any]]]:
    """Gather sensor entity metadata from the integration."""

    sensor_metadata: dict[str, list[dict[str, Any]]] = {}

    for key, (module_path, attribute) in SENSOR_MODULE_SPECS.items():
        if key in EXCLUDED_DEVICE_IDS:
            continue
        module = importlib.import_module(module_path)
        sensor_list = getattr(module, attribute, ())
        serialised = [serialise_sensor_description(item) for item in sensor_list]
        sensor_metadata[key] = serialised

    return sensor_metadata


def load_sensor_translations() -> dict[str, Any]:
    """Load the sensor translation strings bundled with the integration."""

    sensor_strings_path = REPO_ROOT / "custom_components" / "growatt_local" / "strings.sensor.json"
    if sensor_strings_path.exists():
        with sensor_strings_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return {}

def build_snapshot() -> dict[str, Any]:
    """Construct the integration register snapshot."""

    devices: dict[str, dict[str, list[dict[str, Any]]]] = {}

    for device_key, spec in DEVICE_SPECS.items():
        if device_key in EXCLUDED_DEVICE_IDS:
            continue
        module_path: str = spec["module"]
        module = importlib.import_module(module_path)
        groups: dict[str, str] = spec["groups"]
        device_groups: dict[str, list[dict[str, Any]]] = {}
        for group_key, attribute in groups.items():
            device_groups[group_key] = extract_group(
                module,
                attribute,
                device=device_key,
                group=group_key,
            )
        devices[device_key] = device_groups

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "custom_components.growatt_local.API",
        "devices": devices,
        "metadata": {
            "functions": collect_function_metadata(),
            "enums": collect_enum_metadata(),
            "sensor_types": collect_sensor_metadata(),
            "sensor_translations": load_sensor_translations(),
        },
    }


def main() -> None:
    snapshot = build_snapshot()
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2)
        handle.write("\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
