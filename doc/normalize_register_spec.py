#!/usr/bin/env python3
"""Clean and enrich growatt_registers_spec.json.

- Normalises whitespace/Unicode punctuation in textual fields.
- Ensures register numbers are stored as integers.
- Adds attribute mappings (and corresponding sensor labels) derived from
  HA_local_registers.json and the integration sensor descriptions.

Run this script after updating the extracted JSON to keep the dataset tidy.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DOC_DIR = Path(__file__).resolve().parent
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
MAPPING_PATH = DOC_DIR / "HA_local_registers.json"
OUTPUT_PATH = SPEC_PATH
REPO_ROOT = DOC_DIR.parent

sys.path.insert(0, str(REPO_ROOT))

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import types
import sys


def load_sensor_module(name: str):
    sensor_dir = REPO_ROOT / "custom_components" / "growatt_local" / "sensor_types"
    module_path = sensor_dir / f"{name}.py"
    if "growatt_local" not in sys.modules:
        pkg = types.ModuleType("growatt_local")
        pkg.__path__ = [str((REPO_ROOT / "custom_components" / "growatt_local").resolve())]
        sys.modules["growatt_local"] = pkg
    if "growatt_local.sensor_types" not in sys.modules:
        subpkg = types.ModuleType("growatt_local.sensor_types")
        subpkg.__path__ = [str(sensor_dir.resolve())]
        sys.modules["growatt_local.sensor_types"] = subpkg
    loader = SourceFileLoader(f"growatt_local.sensor_types.{name}", str(module_path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


inverter_sensors = load_sensor_module("inverter")
storage_sensors = load_sensor_module("storage")
offgrid_sensors = load_sensor_module("offgrid")

REG_RANGE = re.compile(r"^(\d+)[–-](\d+)$")
REG_SINGLE = re.compile(r"^(\d+)$")

PUNCTUATION_REPLACEMENTS = {
    "（": "(",
    "）": ")",
    "，": ",",
    "；": ";",
    "：": ":",
    "。": ".",
    "、": ", ",
    "\u3000": " ",
}

WHITESPACE_RE = re.compile(r"\s+")


def load_json(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    for src, dst in PUNCTUATION_REPLACEMENTS.items():
        value = value.replace(src, dst)
    value = WHITESPACE_RE.sub(" ", value)
    value = value.replace(" ,", ",")
    value = value.replace(" ;", ";")
    value = value.replace(" :", ":")
    return value.strip()


def normalise_register(field: str | int | None) -> int | None:
    if field is None:
        return None
    if isinstance(field, int):
        return field
    field = field.strip()
    if not field:
        return None
    if match := REG_SINGLE.match(field):
        return int(match.group(1))
    if match := REG_RANGE.match(field):
        return int(match.group(1))
    # Fallback: grab first integer-like token
    digits = re.findall(r"\d+", field)
    if digits:
        return int(digits[0])
    raise ValueError(f"Unrecognised register format: {field}")


def collect_attribute_sources(mapping: dict[str, Any]):
    reg_to_attrs: defaultdict[tuple[str, int], set[str]] = defaultdict(set)
    for family_groups in mapping.values():
        for group_name, entries in family_groups.items():
            group_type = "holding" if "holding" in group_name else "input"
            for entry in entries:
                reg_to_attrs[(group_type, entry["register"])] |= {entry["name"]}
    attr_to_sensor_names: defaultdict[str, set[str]] = defaultdict(set)
    for desc in (*inverter_sensors.INVERTER_SENSOR_TYPES, *storage_sensors.STORAGE_SENSOR_TYPES, *offgrid_sensors.OFFGRID_SENSOR_TYPES):
        attr_to_sensor_names[desc.key].add(desc.name)
    return reg_to_attrs, attr_to_sensor_names


def enrich_entries(
    entries: list[dict[str, Any]],
    table_type: str,
    reg_to_attrs: dict[tuple[str, int], set[str]],
    attr_to_sensor: dict[str, set[str]],
):
    enriched: list[dict[str, Any]] = []
    for entry in entries:
        if entry.get("type") == "section":
            title = clean_text(entry.get("title"))
            enriched.append({"type": "section", "title": title or ""})
            continue

        register = normalise_register(entry.get("register"))
        register_start = normalise_register(entry.get("register_start"))
        register_end = normalise_register(entry.get("register_end"))
        if register is None:
            register = register_start
        if register_start is None:
            register_start = register
        if register_end is None:
            register_end = register

        access = clean_text(entry.get("access"))
        if access:
            upper = access.upper()
            if upper in {"R", "W", "R/W"}:
                access = upper

        spec_name = clean_text(entry.get("name"))
        description = clean_text(entry.get("description"))
        range_field = clean_text(entry.get("range")) or clean_text(entry.get("value"))
        unit = clean_text(entry.get("unit"))
        initial = clean_text(entry.get("initial"))
        note = clean_text(entry.get("note"))
        data_type_field = entry.get("data_type")
        data_type: str | None
        if isinstance(data_type_field, str):
            data_type = data_type_field.strip() or None
        elif isinstance(data_type_field, list):
            # Preserve simple list-valued annotations as comma-separated names.
            joined = ", ".join(str(item).strip() for item in data_type_field if str(item).strip())
            data_type = joined or None
        else:
            data_type = None

        attrs = sorted(reg_to_attrs.get((table_type, register or 0), set()))
        sensors: set[str] = set()
        for attr in attrs:
            sensors.update(attr_to_sensor.get(attr, set()))
        display_name = spec_name
        if attrs:
            if sensors:
                display_name = sorted(sensors)[0]
            else:
                display_name = attrs[0].replace('_', ' ').title()
        if not display_name:
            display_name = spec_name or None

        cleaned_entry: dict[str, Any] = {
            "type": "entry",
            "section": clean_text(entry.get("section")),
            "register": register,
            "register_start": register_start,
            "register_end": register_end,
            "name": display_name,
            "description": description,
            "access": access,
            "range": range_field,
            "unit": unit,
            "initial": initial,
            "note": note,
        }

        if data_type:
            cleaned_entry["data_type"] = data_type

        if spec_name and spec_name != display_name:
            cleaned_entry["spec_name"] = spec_name

        if attrs:
            cleaned_entry["attributes"] = attrs
        if sensors:
            cleaned_entry["sensors"] = sorted(sensors)

        enriched.append(cleaned_entry)
    return enriched


def main() -> None:
    spec = load_json(SPEC_PATH)
    mapping = load_json(MAPPING_PATH)
    reg_to_attrs, attr_to_sensor = collect_attribute_sources(mapping)

    spec["holding"] = enrich_entries(spec.get("holding", []), "holding", reg_to_attrs, attr_to_sensor)
    spec["input"] = enrich_entries(spec.get("input", []), "input", reg_to_attrs, attr_to_sensor)

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"Normalised {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
