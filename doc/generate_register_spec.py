#!/usr/bin/env python3
"""Generate structured register specification and data type catalogues."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

DOC_DIR = Path(__file__).resolve().parent
REPO_ROOT = DOC_DIR.parent
MAPPING_PATH = DOC_DIR / "growatt_local_registers.json"
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
DATA_TYPES_PATH = DOC_DIR / "growatt_register_data_types.json"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str((REPO_ROOT / "custom_components").resolve()))

from custom_components.growatt_local.sensor_types import inverter as inverter_sensors  # noqa: E402
from custom_components.growatt_local.sensor_types import storage as storage_sensors  # noqa: E402
from custom_components.growatt_local.sensor_types import offgrid as offgrid_sensors  # noqa: E402
from custom_components.growatt_local.sensor_types.sensor_entity_description import (  # noqa: E402
    GrowattSensorEntityDescription,
)
from custom_components.growatt_local.sensor_types.switch_entity_description import (  # noqa: E402
    GrowattSwitchEntityDescription,
)


DEVICE_FAMILY_LABELS: dict[str, str] = {
    "tlx": "TL-X/TL-XH single-phase",
    "tl3": "TL3/MAX/MID/MAC three-phase",
    "storage": "Storage MIX/SPA/SPH",
    "offgrid": "Off-grid SPF",
}


@dataclass(slots=True)
class AttributeMeta:
    name: str
    unit: str | None
    device_class: str | None
    entity_category: str | None
    description: str | None = None


def _collect_sensor_meta() -> dict[str, AttributeMeta]:
    meta: dict[str, AttributeMeta] = {}
    modules = (inverter_sensors, storage_sensors, offgrid_sensors)
    for module in modules:
        for attr_name in dir(module):
            value = getattr(module, attr_name)
            if isinstance(value, tuple) and value:
                first = value[0]
                if isinstance(first, GrowattSensorEntityDescription):
                    for desc in value:
                        meta[desc.key] = AttributeMeta(
                            name=desc.name,
                            unit=getattr(desc, "native_unit_of_measurement", None),
                            device_class=getattr(desc, "device_class", None),
                            entity_category=getattr(desc, "entity_category", None),
                            description=getattr(desc, "translation_key", None),
                        )
                elif isinstance(first, GrowattSwitchEntityDescription):
                    for desc in value:
                        meta[desc.key] = AttributeMeta(
                            name=desc.name,
                            unit=None,
                            device_class=None,
                            entity_category="switch",
                            description=None,
                        )
    return meta


ATTRIBUTE_OVERRIDES: dict[str, dict[str, Any]] = {
    "inverter_enabled": {
        "name": "Remote enable",
        "description": "Primary run/stop flag. Set to 1 to allow AC output; 0 places the inverter in standby.",
        "data_type": "binary_flag",
        "read_write": True,
        "category": "control",
    },
    "firmware": {
        "name": "Firmware revisions",
        "description": (
            "Registers 9–14 store two ASCII revision blocks: 9–11 report the inverter firmware, "
            "while 12–14 hold the control/communication board firmware."
        ),
        "data_type": "firmware_blocks",
        "category": "identity",
    },
    "serial number": {
        "name": "Serial number",
        "description": "10-character factory serial number (two ASCII characters per register).",
        "data_type": "serial_ascii_5",
        "category": "identity",
    },
    "Inverter model": {
        "name": "Model code",
        "description": "Encodes inverter hardware options; decoding varies per product family.",
        "data_type": "model_code",
        "category": "identity",
    },
    "device type code": {
        "name": "Device type",
        "description": "Growatt device type identifier mapped to human-friendly product names.",
        "data_type": "device_type_code",
        "category": "identity",
    },
    "number of trackers and phases": {
        "name": "Trackers / phases",
        "description": "High byte = MPPT tracker count, low byte = AC phase count.",
        "data_type": "mppt_phase_tuple",
        "category": "identity",
    },
    "modbus version": {
        "description": "Reported Modbus protocol revision (raw value divided by 100).",
        "category": "identity",
    },
}


REGISTER_OVERRIDES: dict[tuple[str, int], dict[str, Any]] = {
    ("holding", 1): {
        "name": "Grid safety function enables",
        "description": (
            "Bitfield enabling optional grid-code features such as ride-through curves, DRMS, and safety relays. "
            "Bits set to 1 activate the corresponding function."
        ),
        "data_type": "safety_function_flags",
        "category": "grid_protection",
        "read_write": True,
        "source": "manual",
    },
    ("holding", 15): {
        "data_type": "lcd_language",
        "category": "control",
    },
    ("holding", 22): {
        "name": "Modbus baud rate",
        "description": "Selects the RTU baud rate used by the RS485 interface.",
        "data_type": "baud_rate_select",
        "category": "communication",
        "read_write": True,
        "source": "manual",
    },
    ("holding", 30): {
        "name": "Slave address",
        "description": "Modbus device address (1–247).",
        "data_type": "u16",
        "category": "communication",
        "read_write": True,
        "source": "manual",
    },
    ("holding", 31): {
        "name": "Firmware update trigger",
        "description": "Writing the documented magic value starts the bootloader firmware update routine.",
        "data_type": "u16",
        "category": "maintenance",
        "read_write": True,
        "source": "manual",
    },
    ("holding", 32): {
        "name": "Reset user configuration",
        "description": "Clears user-tuned parameters (grid codes, limits) back to defaults when written with the documented key.",
        "data_type": "u16",
        "category": "maintenance",
        "read_write": True,
        "source": "manual",
    },
    ("holding", 33): {
        "name": "Factory reset",
        "description": "Restores factory configuration and clears history counters when executed with the vendor key.",
        "data_type": "u16",
        "category": "maintenance",
        "read_write": True,
        "source": "manual",
    },
}


MANUAL_ENTRIES: list[dict[str, Any]] = [
    {
        "table": "holding",
        "address": 1,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "grid_protection",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 22,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "communication",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 30,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "communication",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 31,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "maintenance",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 32,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "maintenance",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 33,
        "length": 1,
        "families": ["tlx", "tl3", "storage"],
        "category": "maintenance",
        "source": "manual",
    },
    {
        "table": "holding",
        "address": 34,
        "length": 8,
        "name": "Manufacturer string",
        "description": "Eight registers containing an ASCII manufacturer descriptor.",
        "data_type": "ascii_8",
        "category": "identity",
        "source": "manual",
    },
]


MANUAL_DATA_TYPES: dict[str, dict[str, Any]] = {
    "binary_flag": {
        "kind": "enum",
        "registers": 1,
        "choices": {
            "0": {"label": "Disabled"},
            "1": {"label": "Enabled"},
        },
    },
    "safety_function_flags": {
        "kind": "bitfield",
        "registers": 1,
        "bits": [
            {"index": 0, "name": "spi_interface", "description": "Enable the SPI grid-protection interface."},
            {"index": 1, "name": "auto_test", "description": "Allow automatic grid compliance self-test."},
            {"index": 2, "name": "lvfrt", "description": "Low-voltage ride-through curve active."},
            {"index": 3, "name": "freq_derating", "description": "Limit power based on grid frequency."},
            {"index": 4, "name": "soft_start", "description": "Use gradual current ramp when enabling export."},
            {"index": 5, "name": "drms", "description": "Demand Response Management System commands allowed."},
            {"index": 6, "name": "volt_var", "description": "Enable P/V or Q/V grid support modes."},
            {"index": 7, "name": "hvfrt", "description": "High-voltage ride-through curve active."},
            {"index": 8, "name": "rocof", "description": "Trip based on rate-of-change-of-frequency protection."},
            {"index": 9, "name": "q_derate_recover", "description": "Recover reactive power derating when cleared."},
            {"index": 10, "name": "split_phase", "description": "Split-phase output configuration (North America)."},
        ],
        "reserved_bits": [[11, 15]],
    },
    "baud_rate_select": {
        "kind": "enum",
        "registers": 1,
        "choices": {
            "0": {"label": "9600 bit/s"},
            "1": {"label": "38400 bit/s"},
            "2": {"label": "115200 bit/s", "note": "Not supported on legacy firmware"},
        },
    },
    "lcd_language": {
        "kind": "enum",
        "registers": 1,
        "choices": {
            "0": {"label": "Italian"},
            "1": {"label": "English"},
            "2": {"label": "German"},
            "3": {"label": "Spanish"},
            "4": {"label": "French"},
            "5": {"label": "Chinese"},
            "6": {"label": "Polish"},
            "7": {"label": "Portuguese"},
            "8": {"label": "Hungarian"},
        },
    },
    "firmware_blocks": {
        "kind": "ascii_segments",
        "registers": 6,
        "segments": [
            {"name": "inverter", "length": 3, "description": "Main inverter firmware string."},
            {"name": "control", "length": 3, "description": "Control/communication board firmware."},
        ],
        "strip_nulls": True,
    },
    "serial_ascii_5": {
        "kind": "ascii",
        "registers": 5,
        "strip_nulls": True,
    },
    "device_type_code": {
        "kind": "callable",
        "registers": 1,
        "callable": "custom_components.growatt_local.API.device_type.base:device_type",
    },
    "mppt_phase_tuple": {
        "kind": "callable",
        "registers": 1,
        "callable": "custom_components.growatt_local.API.device_type.base:trackers_and_phases",
    },
    "model_code": {
        "kind": "callable_per_family",
        "registers": 2,
        "callable": {
            "tlx": "custom_components.growatt_local.API.device_type.inverter_120:model",
            "tl3": "custom_components.growatt_local.API.device_type.inverter_315:model",
            "storage": "custom_components.growatt_local.API.device_type.storage_120:model",
        },
    },
    "ascii_8": {
        "kind": "ascii",
        "registers": 8,
        "strip_nulls": True,
    },
}


@dataclass(slots=True)
class RawEntry:
    table: str
    address: int
    length: int
    attributes: set[str]
    families: set[str]
    groups: set[str]
    value_types: set[str]
    scales: set[int]
    read_write: bool
    functions: set[str]


def _aggregate_mapping(mapping: dict[str, Any]) -> dict[tuple[str, int], RawEntry]:
    aggregated: dict[tuple[str, int], RawEntry] = {}
    for family, groups in mapping.items():
        for group_name, entries in groups.items():
            table = "holding" if "holding" in group_name else "input"
            for entry in entries:
                address = entry["register"]
                length = entry.get("length", 1)
                key = (table, address)
                raw = aggregated.get(key)
                if raw is None:
                    raw = RawEntry(
                        table=table,
                        address=address,
                        length=length,
                        attributes={entry["name"]},
                        families={family},
                        groups={group_name},
                        value_types={entry.get("value_type", "int")},
                        scales={entry.get("scale") or 1},
                        read_write=bool(entry.get("read_write", False)),
                        functions={entry.get("function")} if entry.get("function") else set(),
                    )
                    aggregated[key] = raw
                else:
                    raw.length = max(raw.length, length)
                    raw.attributes.add(entry["name"])
                    raw.families.add(family)
                    raw.groups.add(group_name)
                    raw.value_types.add(entry.get("value_type", "int"))
                    if scale := entry.get("scale"):
                        raw.scales.add(scale)
                    if entry.get("read_write"):
                        raw.read_write = True
                    if entry.get("function"):
                        raw.functions.add(entry["function"])
    return aggregated


def _default_name(attributes: Iterable[str], attr_meta: dict[str, AttributeMeta]) -> str:
    attrs = list(attributes)
    if len(attrs) == 1:
        attr = attrs[0]
        override = ATTRIBUTE_OVERRIDES.get(attr, {})
        if override.get("name"):
            return override["name"]
        meta = attr_meta.get(attr)
        if meta and meta.name:
            return meta.name
        return attr.replace("_", " ").title()
    return ", ".join(sorted(attr.replace("_", " ").title() for attr in attrs))


def _default_description(attributes: Iterable[str]) -> str:
    attrs = sorted(attributes)
    if not attrs:
        return "Register defined in vendor protocol; no integration mapping yet."
    if len(attrs) == 1:
        return f"Value backing integration attribute `{attrs[0]}`."
    return "Provides multiple integration attributes: " + ", ".join(f"`{a}`" for a in attrs)


def _infer_data_type(raw: RawEntry) -> str | None:
    # Attribute-specific override first
    if raw.attributes:
        for attr in raw.attributes:
            override = ATTRIBUTE_OVERRIDES.get(attr)
            if override and override.get("data_type"):
                return override["data_type"]
    # Register override
    override = REGISTER_OVERRIDES.get((raw.table, raw.address))
    if override and override.get("data_type"):
        return override["data_type"]
    if len(raw.value_types) == 1:
        value_type = next(iter(raw.value_types))
        scale = next(iter(raw.scales)) if raw.scales else 1
        if value_type == "int":
            return "u16"
        if value_type == "float":
            if raw.length == 1:
                return f"u16_div{scale}"
            return f"s32_div{scale}"
        if value_type == "str":
            return f"ascii_{raw.length}"
        if value_type == "custom_function":
            if raw.functions:
                func = next(iter(raw.functions))
                if func == "device_type":
                    return "device_type_code"
                if func == "trackers_and_phases":
                    return "mppt_phase_tuple"
                if func == "model":
                    return "model_code"
    return None


def _normalise_entry(raw: RawEntry, attr_meta: dict[str, AttributeMeta]) -> dict[str, Any]:
    override = REGISTER_OVERRIDES.get((raw.table, raw.address), {})
    attributes = sorted(raw.attributes)
    entry: dict[str, Any] = {
        "table": raw.table,
        "address": raw.address,
        "end_address": raw.address + raw.length - 1,
        "length": raw.length,
        "function_code": 3 if raw.table == "holding" else 4,
        "name": override.get("name") or _default_name(attributes, attr_meta),
        "description": override.get("description") or ATTRIBUTE_OVERRIDES.get(attributes[0], {}).get("description") if attributes else None,
        "category": override.get("category") or ATTRIBUTE_OVERRIDES.get(attributes[0], {}).get("category") if attributes else None,
        "unit": None,
        "data_type": override.get("data_type"),
        "attributes": attributes,
        "families": sorted(raw.families),
        "family_labels": [DEVICE_FAMILY_LABELS.get(f, f) for f in sorted(raw.families)],
        "groups": sorted(raw.groups),
        "read_write": raw.read_write if override.get("read_write") is None else override.get("read_write"),
        "source": override.get("source", "integration" if attributes else "manual"),
    }
    if attr_meta and attributes:
        meta = attr_meta.get(attributes[0])
        if meta:
            if meta.unit and not entry["unit"]:
                entry["unit"] = meta.unit
            if not entry["name"] and meta.name:
                entry["name"] = meta.name
    if not entry["description"]:
        entry["description"] = _default_description(attributes)
    if not entry["data_type"]:
        entry["data_type"] = _infer_data_type(raw)
    if raw.scales:
        entry["divisor"] = next(iter(raw.scales))
    if raw.functions:
        entry["functions"] = sorted(raw.functions)
    return entry


def _merge_manual_entries(entries: dict[tuple[str, int], dict[str, Any]]) -> None:
    for manual in MANUAL_ENTRIES:
        key = (manual["table"], manual["address"])
        if key in entries:
            existing = entries[key]
            existing.update({k: v for k, v in manual.items() if k not in {"table", "address"}})
        else:
            manual_entry = manual.copy()
            manual_entry.setdefault("end_address", manual_entry["address"] + manual_entry.get("length", 1) - 1)
            manual_entry.setdefault("function_code", 3 if manual_entry["table"] == "holding" else 4)
            manual_entry.setdefault("families", [])
            manual_entry.setdefault("family_labels", [])
            manual_entry.setdefault("attributes", [])
            manual_entry.setdefault("groups", [])
            manual_entry.setdefault("read_write", False)
            override = REGISTER_OVERRIDES.get(key, {})
            for field in ("name", "description", "data_type", "category", "source"):
                if field not in manual_entry and field in override:
                    manual_entry[field] = override[field]
            if override.get("read_write") is not None:
                manual_entry["read_write"] = override["read_write"]
            entries[key] = manual_entry


def _build_types(entries: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    types = {name: data.copy() for name, data in MANUAL_DATA_TYPES.items()}
    for entry in entries:
        dtype = entry.get("data_type")
        if not dtype or dtype in types:
            continue
        if dtype.startswith("u16_div"):
            divisor = int(dtype.split("div", 1)[1])
            types[dtype] = {
                "kind": "scaled",
                "registers": 1,
                "signed": False,
                "divisor": divisor,
            }
        elif dtype.startswith("s32_div"):
            divisor = int(dtype.split("div", 1)[1])
            types[dtype] = {
                "kind": "scaled",
                "registers": 2,
                "signed": True,
                "divisor": divisor,
            }
        elif dtype.startswith("ascii_"):
            length = int(dtype.split("_", 1)[1])
            types[dtype] = {
                "kind": "ascii",
                "registers": length,
                "strip_nulls": True,
            }
        elif dtype == "u16":
            types[dtype] = {
                "kind": "integer",
                "registers": 1,
                "signed": False,
            }
    return dict(sorted(types.items()))


def main() -> None:
    with MAPPING_PATH.open("r", encoding="utf-8") as handle:
        mapping = json.load(handle)
    attr_meta = _collect_sensor_meta()
    raw_entries = _aggregate_mapping(mapping)
    entries: dict[tuple[str, int], dict[str, Any]] = {}
    for key, raw in raw_entries.items():
        entry = _normalise_entry(raw, attr_meta)
        entries[key] = entry
    _merge_manual_entries(entries)

    sorted_entries = sorted(entries.values(), key=lambda item: (item["table"], item["address"]))

    generated = datetime.now(UTC).isoformat(timespec="seconds")
    spec = {
        "meta": {
            "generated": generated,
            "generator": "generate_register_spec.py",
            "families": DEVICE_FAMILY_LABELS,
        },
        "holding": [entry for entry in sorted_entries if entry["table"] == "holding"],
        "input": [entry for entry in sorted_entries if entry["table"] == "input"],
    }

    with SPEC_PATH.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    types = _build_types(sorted_entries)
    register_catalogue = [
        {
            "table": entry["table"],
            "address": entry["address"],
            "end_address": entry["end_address"],
            "length": entry["length"],
            "type": entry.get("data_type"),
            "attributes": entry.get("attributes", []),
            "families": entry.get("families", []),
        }
        for entry in sorted_entries
    ]
    data_types = {
        "meta": spec["meta"],
        "types": types,
        "registers": register_catalogue,
    }
    with DATA_TYPES_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data_types, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"Wrote {SPEC_PATH.name} and {DATA_TYPES_PATH.name}")


if __name__ == "__main__":
    main()
