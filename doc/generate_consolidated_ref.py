#!/usr/bin/env python3
"""Generate consolidated_register_ref.json by merging vendor and curated specs."""

from __future__ import annotations

import hashlib
import json
import re
import pickle
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

try:
    import networkx as nx
except ImportError:  # pragma: no cover - optional at runtime if graph not used
    nx = None

DOC_DIR = Path(__file__).resolve().parent
VENDOR_TABLE_PATH = (
    DOC_DIR / "Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English-tables.json"
)
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
HA_LOCAL_PATH = DOC_DIR / "HA_local_registers.json"
OPENINVERTER_PATH = DOC_DIR / "openinverter_gateway_registers.json"
INVERTER_TO_MQTT_PATH = DOC_DIR / "inverter_to_mqtt_registers.json"
GRAPH_PATH = DOC_DIR / "register_graph.gpickle"
GROTT_LAYOUTS_PATH = DOC_DIR / "grott_register_layouts.json"
OUTPUT_PATH = DOC_DIR / "consolidated_register_ref.json"

# Maximum number of BDC slots described by algebraic vendor ranges
MAX_BDC_SLOTS = 10
# Excluded vendor ranges (skip generating blocks for these at this time)
EXCLUDED_VENDOR_RANGES: list[tuple[int, int]] = [(5000, 5399)]  # BDC holding mirrors

REGISTER_PATTERN = re.compile(r"^(\d+)(?:\.(\d+))?$")
REGISTER_RANGE_PATTERN = re.compile(r"^(\d+)\s*[~\-]\s*(\d+)$")


@dataclass(slots=True)
class VendorRow:
    register: Optional[int]
    register_end: Optional[int]
    raw_register: str
    variable: Optional[str]
    description: Optional[str]
    access: Optional[str]
    value: Optional[str]
    unit: Optional[str]
    initial: Optional[str]
    note: Optional[str]
    page: Optional[int]

    def to_json(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "register": self.register,
            "raw_register": self.raw_register,
            "variable": self.variable,
            "description": self.description,
            "access": self.access,
            "value": self.value,
            "unit": self.unit,
            "initial": self.initial,
            "note": self.note,
            "page": self.page,
        }
        # Do not include register_end in row JSON; rows are per-address entries
        return {k: v for k, v in data.items() if v is not None}


@dataclass(slots=True)
class RangeEntry:
    table: str
    start: int
    end: int
    data: Dict[str, Any]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_graph(path: Path) -> Optional[nx.MultiDiGraph]:
    if nx is None or not path.exists():
        return None
    with path.open("rb") as handle:
        return pickle.load(handle)


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalise_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return text


def parse_register(raw: Optional[str]) -> Optional[int]:
    if raw is None:
        return None
    token = raw.strip()
    if not token:
        return None
    token_no_space = token.replace(" ", "")
    if token_no_space.endswith("."):
        token_no_space = token_no_space[:-1]
    if match := REGISTER_PATTERN.match(token_no_space):
        integer_part = match.group(1)
        try:
            return int(integer_part)
        except ValueError:
            return None
    if match := REGISTER_RANGE_PATTERN.match(token_no_space):
        try:
            return int(match.group(1))
        except ValueError:
            return None
    digits = re.findall(r"\d+", token_no_space)
    if digits:
        try:
            return int(digits[0])
        except ValueError:
            return None
    return None


def sanitise_vendor_row(row: Dict[str, Any]) -> VendorRow:
    raw_register = normalise_text(row.get("register")) or ""
    register: Optional[int] = None
    register_end: Optional[int] = None
    token = raw_register
    token_no_space = token.replace(" ", "")
    if token_no_space.endswith("."):
        token_no_space = token_no_space[:-1]

    # The vendor tables occasionally express array slots algebraically (e.g.
    # "5000+(N-1)*40--- 5039+(N-1)*40"). Those entries should not be coerced
    # into numeric addresses – keep them as raw metadata only.
    if any(symbol in token_no_space for symbol in ("+", "*", "(", ")")):
        register = None
        register_end = None
    elif match := REGISTER_PATTERN.match(token_no_space):
        try:
            register = int(match.group(1))
        except ValueError:
            register = None
    elif match := REGISTER_RANGE_PATTERN.match(token_no_space):
        try:
            register = int(match.group(1))
            register_end = int(match.group(2))
        except ValueError:
            register = None
            register_end = None
    else:
        digits = re.findall(r"\d+", token_no_space)
        if digits:
            try:
                register = int(digits[0])
            except ValueError:
                register = None
            if register is not None and len(digits) > 1 and (
                "~" in token_no_space or "-" in token_no_space
            ):
                try:
                    register_end = int(digits[1])
                except ValueError:
                    register_end = None

    access = normalise_text(row.get("write_or_not"))
    if access:
        access = access.upper()
    description = normalise_text(row.get("description"))
    variable = normalise_text(row.get("variable"))
    value = normalise_text(row.get("value"))
    unit = normalise_text(row.get("unit"))
    initial = normalise_text(row.get("initial"))
    note = normalise_text(row.get("note"))
    page_raw = row.get("page")
    page: Optional[int]
    if isinstance(page_raw, int):
        page = page_raw
    else:
        try:
            page = int(str(page_raw).strip()) if page_raw is not None else None
        except ValueError:
            page = None
    return VendorRow(
        register=register,
        register_end=register_end,
        raw_register=raw_register,
        variable=variable,
        description=description,
        access=access,
        value=value,
        unit=unit,
        initial=initial,
        note=note,
        page=page,
    )


def ranges_overlap(start_a: int, end_a: int, start_b: int, end_b: int) -> bool:
    return not (end_a < start_b or end_b < start_a)


def build_vendor_index(
    rows: Iterable[Dict[str, Any]],
    table_name: str,
) -> Tuple[Dict[int, List[VendorRow]], List[VendorRow], List[int]]:
    index: Dict[int, List[VendorRow]] = {}
    orphans: List[VendorRow] = []
    ordered_registers: List[int] = []
    seen_registers: set[int] = set()
    for raw_row in rows:
        entry = sanitise_vendor_row(raw_row)
        if entry.register is None:
            orphans.append(entry)
            continue
        start_reg = entry.register
        end_reg = (
            entry.register_end
            if entry.register_end and entry.register_end >= start_reg
            else start_reg
        )
        # Expand inclusive range into individual addresses
        for addr in range(start_reg, end_reg + 1):
            # Skip excluded ranges entirely
            if any(lo <= addr <= hi for (lo, hi) in EXCLUDED_VENDOR_RANGES):
                continue
            row_copy = VendorRow(
                register=addr,
                register_end=None,
                raw_register=entry.raw_register,
                variable=entry.variable,
                description=entry.description,
                access=entry.access,
                value=entry.value,
                unit=entry.unit,
                initial=entry.initial,
                note=entry.note,
                page=entry.page,
            )
            index.setdefault(addr, []).append(row_copy)
            if addr not in seen_registers:
                seen_registers.add(addr)
                ordered_registers.append(addr)
    return index, orphans, ordered_registers


def drop_optionals(
    data: Dict[str, Any], required: Iterable[str] = ()
) -> Dict[str, Any]:
    required_set = set(required)
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if key in required_set:
            result[key] = value
            continue
        if value is None:
            continue
        if isinstance(value, (list, dict)) and not value:
            continue
        result[key] = value
    return result


def compact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: value
        for key, value in data.items()
        if value not in (None, "", [], {})
    }


def summarise_spec_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = (
        "type",
        "name",
        "description",
        "access",
        "unit",
        "range",
        "initial",
        "note",
        "attributes",
        "sensors",
    )
    summary = compact_dict({key: payload.get(key) for key in allowed_fields})
    supplements = payload.get("supplemental_entries")
    if isinstance(supplements, list):
        filtered: List[Dict[str, Any]] = []
        for entry in supplements:
            if not isinstance(entry, dict):
                continue
            filtered_entry = compact_dict(
                {key: entry.get(key) for key in allowed_fields}
            )
            if filtered_entry:
                filtered.append(filtered_entry)
        if filtered:
            summary["supplemental_entries"] = filtered
    return summary


def summarise_vendor_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = (
        "variable",
        "description",
        "access",
        "value",
        "unit",
        "initial",
        "note",
        "page",
    )
    rows: List[Dict[str, Any]] = []
    for row in payload.get("rows", []) or []:
        if not isinstance(row, dict):
            continue
        filtered = compact_dict({key: row.get(key) for key in allowed_fields})
        if filtered:
            rows.append(filtered)
    summary: Dict[str, Any] = {}
    if rows:
        summary["rows"] = rows
    missing = payload.get("missing_registers")
    if missing:
        summary["missing_registers"] = missing
    return summary


def summarise_home_assistant_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    seen: set[Tuple[Optional[str], Optional[str], Optional[str]]] = set()
    group_devices: Dict[str, set[str]] = {}
    for device in payload.get("devices", []) or []:
        device_name = device.get("device")
        for group in device.get("groups", []) or []:
            group_name = group.get("group")
            for entry in group.get("entries", []) or []:
                name = entry.get("name") or entry.get("variable")
                key = (device_name, group_name, name)
                if key in seen:
                    continue
                seen.add(key)
                summary_entry = compact_dict(
                    {
                        "device": device_name,
                        "group": group_name,
                        "name": name,
                        "read_write": entry.get("read_write"),
                        "value_type": entry.get("value_type"),
                        "unit": entry.get("unit"),
                        "scale": entry.get("scale"),
                    }
                )
                if summary_entry:
                    entries.append(summary_entry)
                if group_name and device_name:
                    group_devices.setdefault(group_name, set()).add(device_name)
    result: Dict[str, Any] = {}
    if group_devices:
        result["groups"] = [
            {
                "group": group,
                "devices": sorted(devices),
            }
            for group, devices in sorted(group_devices.items())
        ]
    if entries:
        result["entries"] = entries
    return result


def summarise_openinverter_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    for device in payload.get("devices", []) or []:
        device_name = device.get("device")
        for entry in device.get("entries", []) or []:
            summary_entry = compact_dict(
                {
                    "device": device_name,
                    "label": entry.get("label"),
                    "enum": entry.get("enum"),
                    "enum_value": entry.get("enum_value"),
                    "mqtt_key": entry.get("mqtt_key"),
                    "unit": entry.get("unit"),
                    "length": entry.get("length"),
                    "default": entry.get("default"),
                }
            )
            if summary_entry:
                entries.append(summary_entry)
    if entries:
        return {"entries": entries}
    return {}


def summarise_inverter_to_mqtt_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    for op in payload.get("operations", []) or []:
        base = compact_dict(
            {
                "file": op.get("file"),
                "function": op.get("function"),
                "operation": op.get("operation"),
            }
        )
        for entry in op.get("entries", []) or []:
            summary_entry = base.copy()
            summary_entry.update(
                compact_dict(
                    {
                        "variable": entry.get("variable"),
                        "mqtt_key": entry.get("mqtt_key"),
                        "registers": entry.get("registers"),
                        "buffer_indexes": entry.get("buffer_indexes"),
                    }
                )
            )
            if summary_entry:
                entries.append(summary_entry)
    if entries:
        return {"entries": entries}
    return {}


def summarise_grott_source(payload: Dict[str, Any]) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    for entry in payload.get("fields", []) or []:
        summary_entry = compact_dict(
            {
                "layout": entry.get("layout"),
                "field": entry.get("field"),
                "type": entry.get("type"),
                "divide": entry.get("divide"),
                "register_count": entry.get("register_count"),
                "include_by_default": entry.get("include_by_default"),
                "extra": entry.get("extra"),
            }
        )
        if summary_entry:
            entries.append(summary_entry)
    summary: Dict[str, Any] = {}
    if entries:
        summary["fields"] = entries
    for key in ("exported_at", "grott_version", "mqtt_topic_template"):
        if payload.get(key):
            summary[key] = payload.get(key)
    return summary


def summarise_sources(sources: Dict[str, Any]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {}
    for name, payload in sources.items():
        if not payload:
            continue
        if name == "spec":
            spec_summary = summarise_spec_source(payload)
            if spec_summary:
                summary[name] = spec_summary
            continue
        if name == "vendor":
            vendor_summary = summarise_vendor_source(payload)
            if vendor_summary:
                summary[name] = vendor_summary
            continue
        if name == "home_assistant":
            ha_summary = summarise_home_assistant_source(payload)
            if ha_summary:
                summary[name] = ha_summary
            continue
        if name == "openinverter_gateway":
            oi_summary = summarise_openinverter_source(payload)
            if oi_summary:
                summary[name] = oi_summary
            continue
        if name == "inverter_to_mqtt":
            mqtt_summary = summarise_inverter_to_mqtt_source(payload)
            if mqtt_summary:
                summary[name] = mqtt_summary
            continue
        if name == "grott":
            grott_summary = summarise_grott_source(payload)
            if grott_summary:
                summary[name] = grott_summary
            continue
        summary[name] = payload
    return summary


def apply_consolidated_fields(
    block: Dict[str, Any], consolidated: Optional[Dict[str, Any]]
) -> None:
    if not consolidated:
        return
    for key, value in consolidated.items():
        if value in (None, "", [], {}):
            continue
        target_key = "note" if key == "note" else key
        if target_key in block and block[target_key] not in (None, "", [], {}):
            continue
        block[target_key] = value

def build_consolidated_entry(
    entry: Dict[str, Any], section_title: Optional[str]
) -> Dict[str, Any]:
    consolidated = {
        "section": entry.get("section") or section_title,
        "name": entry.get("name"),
        "description": entry.get("description"),
        "access": entry.get("access"),
        "unit": entry.get("unit"),
        "range": entry.get("range"),
        "initial": entry.get("initial"),
        "note": entry.get("note"),
        "data_type": entry.get("data_type"),
        "attributes": entry.get("attributes"),
        "sensors": entry.get("sensors"),
    }
    return drop_optionals(consolidated)


def build_spec_source(
    entry: Dict[str, Any], section_title: Optional[str]
) -> Dict[str, Any]:
    attrs = entry.get("attributes")
    sensors = entry.get("sensors")
    spec_source = {
        "type": entry.get("type"),
        "section": entry.get("section") or section_title,
        "name": entry.get("name"),
        "spec_name": entry.get("spec_name"),
        "description": entry.get("description"),
        "access": entry.get("access"),
        "unit": entry.get("unit"),
        "range": entry.get("range"),
        "initial": entry.get("initial"),
        "note": entry.get("note"),
        "data_type": entry.get("data_type"),
        "attributes": attrs if isinstance(attrs, list) else None,
        "sensors": sensors if isinstance(sensors, list) else None,
        "register": entry.get("register"),
        "register_start": entry.get("register_start"),
        "register_end": entry.get("register_end"),
        "access_raw": entry.get("access"),
    }
    return drop_optionals(
        spec_source, required=("register", "register_start", "register_end")
    )


def build_register_blocks(
    table: str,
    spec_entries: List[Dict[str, Any]],
    vendor_index: Dict[int, List[VendorRow]],
    vendor_order: List[int],
    external_collectors: Optional[
        Dict[str, Callable[[str, int, int], Optional[Dict[str, Any]]]]
    ] = None,
) -> Tuple[List[Dict[str, Any]], List[int]]:
    blocks: List[Dict[str, Any]] = []
    used_vendor_registers: List[int] = []
    current_section: Optional[str] = None
    coverage: List[Tuple[int, int, Dict[str, Any]]] = []
    remaining_vendor: Dict[int, List[Dict[str, Any]]] = {
        register: [row.to_json() for row in rows]
        for register, rows in vendor_index.items()
    }
    consumed_vendor_registers: set[int] = set()

    for entry in spec_entries:
        entry_type = entry.get("type")
        if entry_type == "section":
            current_section = entry.get("title")
            continue
        if entry_type != "entry":
            continue

        start = entry.get("register_start") or entry.get("register")
        end = entry.get("register_end") or start
        if start is None or end is None:
            continue
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if end < start:
            start, end = end, start

        # Skip excluded ranges entirely
        for lo, hi in EXCLUDED_VENDOR_RANGES:
            if not (end < lo or start > hi):
                # overlaps with excluded
                break
        else:
            pass
        if any(not (end < lo or start > hi) for lo, hi in EXCLUDED_VENDOR_RANGES):
            continue

        parent_block: Optional[Dict[str, Any]] = None
        for cov_start, cov_end, block in coverage:
            if start >= cov_start and end <= cov_end:
                parent_block = block
                break

        if parent_block is not None:
            supplemental = build_spec_source(entry, current_section)
            if supplemental:
                parent_spec = parent_block.setdefault("sources", {}).setdefault(
                    "spec", {}
                )
                parent_spec.setdefault("supplemental_entries", []).append(supplemental)
            continue

        length = end - start + 1 if end >= start else 1
        block_id = f"{table}:{start}" if start == end else f"{table}:{start}-{end}"

        vendor_rows: List[Dict[str, Any]] = []
        missing_registers: List[int] = []
        for address in range(start, end + 1):
            rows = vendor_index.get(address)
            if not rows:
                # If vendor rows are missing for this address, check whether any
                # external collector (openinverter, inverter_to_mqtt, home_assistant)
                # provides coverage for this single register. If so, treat the
                # address as covered (don't list it as missing) and mark it as
                # consumed so it is not emitted again as a vendor-only block.
                covered_by_external = False
                if external_collectors:
                    for _name, collector in external_collectors.items():
                        try:
                            if collector and collector(table, address, address):
                                covered_by_external = True
                                break
                        except Exception:
                            # Be defensive: any collector errors should not stop
                            # generation; treat as not covered
                            continue
                if covered_by_external:
                    used_vendor_registers.append(address)
                    consumed_vendor_registers.add(address)
                    continue
                missing_registers.append(address)
                continue
            used_vendor_registers.append(address)
            consumed_vendor_registers.add(address)
            vendor_rows.extend(
                remaining_vendor.get(address, [row.to_json() for row in rows])
            )

        consolidated = build_consolidated_entry(entry, current_section)
        spec_source = build_spec_source(entry, current_section)

        sources: Dict[str, Any] = {"spec": spec_source}
        if vendor_rows or missing_registers:
            vendor_src: Dict[str, Any] = {"rows": vendor_rows}
            if missing_registers:
                vendor_src["missing_registers"] = missing_registers
            sources["vendor"] = vendor_src

        if external_collectors:
            for name, collector in external_collectors.items():
                if collector is None:
                    continue
                external_data = collector(table, start, end)
                if external_data:
                    # Remove redundant tables for compact output
                    if name == "openinverter_gateway":
                        for device in external_data.get("devices", []):
                            reg_to_topic = device.pop("register_to_mqtt_topic", None)
                            device.pop("mqtt_keys", None)
                            device.pop("mqtt_topic_to_registers", None)
                            for entry in device.get("entries", []):
                                label = entry.get("label")
                                if label and reg_to_topic and label in reg_to_topic:
                                    entry["mqtt_key"] = reg_to_topic[label]
                    if name == "inverter_to_mqtt":
                        for op in external_data.get("operations", []):
                            mqtt_keys = op.pop("mqtt_keys", None)
                            for entry in op.get("entries", []):
                                variable = entry.get("variable")
                                if variable and mqtt_keys and variable in mqtt_keys:
                                    entry["mqtt_key"] = variable
                    sources[name] = external_data

        block = {
            "id": block_id,
            "table": table,
            "start_register": start,
            "end_register": end,
            "length": length,
            "sources": sources,
        }
        apply_consolidated_fields(block, consolidated)
        block["sources"] = summarise_sources(block.get("sources", {}))
        if not block["sources"]:
            block.pop("sources", None)
        blocks.append(block)
        coverage.append((start, end, block))

    # Include any vendor registers not covered by the curated spec as standalone blocks
    used_set = set(used_vendor_registers)
    vendor_only_blocks: List[Dict[str, Any]] = []
    for register in vendor_order:
        # Skip excluded ranges entirely
        if any(lo <= register <= hi for (lo, hi) in EXCLUDED_VENDOR_RANGES):
            continue
        if register in consumed_vendor_registers:
            continue
        vendor_rows = remaining_vendor.get(register, [])
        if not vendor_rows:
            continue
        vendor_src: Dict[str, Any] = {"rows": vendor_rows}
        block = {
            "id": f"{table}:{register}",
            "table": table,
            "start_register": register,
            "end_register": register,
            "length": 1,
            "sources": {
                "vendor": vendor_src,
            },
        }
        if external_collectors:
            for name, collector in external_collectors.items():
                if collector is None:
                    continue
                external_data = collector(table, register, register)
                if external_data:
                    block["sources"][name] = external_data
        block["sources"] = summarise_sources(block.get("sources", {}))
        if not block["sources"]:
            block.pop("sources", None)
        vendor_only_blocks.append(block)
        used_vendor_registers.append(register)
        consumed_vendor_registers.add(register)

    blocks.extend(vendor_only_blocks)

    blocks.sort(key=lambda item: (item["start_register"], item["end_register"]))
    return blocks, used_vendor_registers


def collect_orphan_vendor_rows(
    vendor_index: Dict[int, List[VendorRow]],
    vendor_orphans: List[VendorRow],
    used_registers: Iterable[int],
) -> List[Dict[str, Any]]:
    used_set = set(used_registers)
    leftovers: List[Dict[str, Any]] = []
    for register, rows in vendor_index.items():
        if register in used_set:
            continue
        leftovers.extend([row.to_json() for row in rows])
    leftovers.extend([row.to_json() for row in vendor_orphans])
    leftovers.sort(
        key=lambda row: (row.get("register", 999999), row.get("raw_register", ""))
    )
    return leftovers


def prepare_home_assistant_entries(data: Dict[str, Any]) -> List[RangeEntry]:
    devices = data.get("devices", {})
    function_index = data.get("metadata", {}).get("functions", {})
    entries: List[RangeEntry] = []

    for device, groups in devices.items():
        if not isinstance(groups, dict):
            continue
        for group_name, items in groups.items():
            if not isinstance(items, list):
                continue
            if group_name.startswith("holding"):
                table = "holding"
            elif group_name.startswith("input"):
                table = "input"
            else:
                continue
            for item in items:
                register = item.get("register")
                length = item.get("length", 1) or 1
                if not isinstance(register, int):
                    continue
                if not isinstance(length, int) or length < 1:
                    length = 1
                start = register
                end = register + length - 1

                payload: Dict[str, Any] = {
                    "device": device,
                    "group": group_name,
                    "name": item.get("name"),
                    "register": register,
                    "length": length,
                    "scale": item.get("scale"),
                    "read_write": item.get("read_write"),
                    "value_type": item.get("value_type"),
                    "function": item.get("function"),
                    "function_path": item.get("function_path"),
                }

                function_path = item.get("function_path")
                if isinstance(function_path, str):
                    function_details = function_index.get(function_path)
                    if function_details:
                        payload["function_details"] = {
                            key: function_details.get(key)
                            for key in (
                                "module",
                                "qualname",
                                "signature",
                                "defined_in",
                                "doc",
                            )
                            if function_details.get(key) is not None
                        }

                entries.append(
                    RangeEntry(table=table, start=start, end=end, data=payload)
                )

    return entries


SIZE_TO_LENGTH = {
    "SIZE_16BIT": 1,
    "SIZE_16BIT_S": 1,
    "SIZE_32BIT": 2,
    "SIZE_32BIT_S": 2,
}


def prepare_openinverter_entries(data: Dict[str, Any]) -> List[RangeEntry]:
    devices = data.get("devices", {})
    entries: List[RangeEntry] = []

    for device, info in devices.items():
        if not isinstance(info, dict):
            continue
        for table_key, table_name in (
            ("input_registers", "input"),
            ("holding_registers", "holding"),
        ):
            register_items = info.get(table_key, [])
            if not isinstance(register_items, list):
                continue
            for item in register_items:
                address = item.get("address")
                size = item.get("size")
                if not isinstance(address, int):
                    continue
                length = SIZE_TO_LENGTH.get(size, 1)
                start = address
                end = address + length - 1

                payload: Dict[str, Any] = {
                    "device": device,
                    "file": info.get("file"),
                    "enum": item.get("enum"),
                    "enum_value": item.get("enum_value"),
                    "label": item.get("label"),
                    "address": address,
                    "length": length,
                    "size": size,
                    "default": item.get("default"),
                    "multiplier": item.get("multiplier"),
                    "resolution": item.get("resolution"),
                    "unit": item.get("unit"),
                    "frontend": item.get("frontend"),
                    "plot": item.get("plot"),
                }
                if item.get("comment"):
                    payload["comment"] = item.get("comment")
                entries.append(
                    RangeEntry(table=table_name, start=start, end=end, data=payload)
                )

    return entries


def prepare_inverter_to_mqtt_entries(data: Dict[str, Any]) -> List[RangeEntry]:
    code_index = data.get("code", {})
    entries: List[RangeEntry] = []

    for file_path, info in code_index.items():
        if not isinstance(info, dict):
            continue
        reads = info.get("reads", [])
        if isinstance(reads, list):
            for read in reads:
                table = "input" if read.get("type") == "input" else "holding"
                read_start = read.get("start_register")
                read_length = read.get("length")
                if not isinstance(read_start, int) or not isinstance(read_length, int):
                    continue
                for entry in read.get("entries", []):
                    registers = entry.get("registers")
                    if not isinstance(registers, list) or not registers:
                        continue
                    try:
                        register_numbers = [int(reg) for reg in registers]
                    except (TypeError, ValueError):
                        continue
                    start = min(register_numbers)
                    end = max(register_numbers)

                    payload: Dict[str, Any] = {
                        "file": file_path,
                        "function": read.get("function"),
                        "operation": "read",
                        "read_start_register": read_start,
                        "read_length": read_length,
                        "variable": entry.get("variable"),
                        "registers": register_numbers,
                        "buffer_indexes": entry.get("buffer_indexes"),
                        "expression": entry.get("expression"),
                    }
                    entries.append(
                        RangeEntry(table=table, start=start, end=end, data=payload)
                    )

        writes = info.get("writes", [])
        if isinstance(writes, list):
            for write in writes:
                address = write.get("address")
                if not isinstance(address, int):
                    continue
                payload = {
                    "file": file_path,
                    "operation": "write",
                    "address": address,
                    "call": write.get("call"),
                }
                entries.append(
                    RangeEntry(
                        table="holding", start=address, end=address, data=payload
                    )
                )

    return entries


def prepare_grott_entries(data: Dict[str, Any]) -> List[RangeEntry]:
    layouts = data.get("layouts", {})
    entries: List[RangeEntry] = []

    for layout_id, layout in layouts.items():
        fields = layout.get("fields", [])
        if not isinstance(fields, list):
            continue
        for field in fields:
            if not isinstance(field, dict):
                continue
            start = field.get("register_start")
            end = field.get("register_end", start)
            if start is None:
                continue
            if not isinstance(start, int):
                continue
            if end is None or not isinstance(end, int):
                end = start
            if end < start:
                start, end = end, start

            payload: Dict[str, Any] = {
                "layout": layout_id,
                "field": field.get("field"),
            }
            for key in (
                "byte_offset",
                "length_bytes",
                "type",
                "divide",
                "register_count",
            ):
                if field.get(key) is not None:
                    payload[key] = field.get(key)
            if "include_by_default" in field:
                payload["include_by_default"] = field["include_by_default"]
            if "extra" in field:
                payload["extra"] = field["extra"]

            entries.append(
                RangeEntry(
                    table="input",
                    start=start,
                    end=end,
                    data=payload,
                )
            )

    return entries


def build_home_assistant_collector(entries: List[RangeEntry]):
    def collector(table: str, start: int, end: int) -> Optional[Dict[str, Any]]:
        matches = [
            entry
            for entry in entries
            if entry.table == table
            and ranges_overlap(entry.start, entry.end, start, end)
        ]
        if not matches:
            return None

        grouped: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for entry in matches:
            payload = entry.data
            device = payload.get("device")
            group_name = payload.get("group")
            if not device or not group_name:
                continue
            item = {
                key: value
                for key, value in payload.items()
                if key not in {"device", "group"}
            }
            item["start_register"] = entry.start
            item["end_register"] = entry.end
            grouped[device][group_name].append(item)

        devices: List[Dict[str, Any]] = []
        for device in sorted(grouped):
            groups_payload: List[Dict[str, Any]] = []
            for group_name in sorted(grouped[device]):
                entries_payload = grouped[device][group_name]
                entries_payload.sort(
                    key=lambda item: (
                        item.get("start_register", 0),
                        item.get("end_register", 0),
                    )
                )
                groups_payload.append(
                    {
                        "group": group_name,
                        "entries": entries_payload,
                    }
                )
            devices.append(
                {
                    "device": device,
                    "groups": groups_payload,
                }
            )

        return {"devices": devices}

    return collector


def build_openinverter_collector(entries: List[RangeEntry]):
    # Load the full openinverter data for mqtt_keys
    openinverter_data = None
    try:
        openinverter_path = OPENINVERTER_PATH
        if openinverter_path.exists():
            with open(openinverter_path, encoding="utf-8") as f:
                openinverter_data = json.load(f)
    except FileNotFoundError:
        pass

    def collector(table: str, start: int, end: int) -> dict | None:
        matches = [
            entry
            for entry in entries
            if entry.table == table
            and ranges_overlap(entry.start, entry.end, start, end)
        ]
        if not matches:
            return None

        grouped: dict[str, list[dict]] = defaultdict(list)
        mqtt_keys_map = {}
        register_to_topic_map = {}
        topic_to_registers_map = {}
        if openinverter_data:
            for device, info in openinverter_data.get("devices", {}).items():
                mqtt_keys = info.get("mqtt_keys", [])
                mqtt_keys_map[device] = mqtt_keys
                # Build register label to topic mapping
                reg_map = {}
                topic_map = defaultdict(list)
                # For input/holding registers, map label to topic
                for reg_type in ("input_registers", "holding_registers"):
                    for reg in info.get(reg_type, []):
                        label = reg.get("label")
                        address = reg.get("address")
                        if label and label in mqtt_keys:
                            reg_map[label] = (
                                label  # topic is label (can be customized if needed)
                            )
                            topic_map[label].append(address)
                register_to_topic_map[device] = reg_map
                topic_to_registers_map[device] = dict(topic_map)

        for entry in matches:
            payload = {
                key: value for key, value in entry.data.items() if key not in {"device"}
            }
            payload["start_register"] = entry.start
            payload["end_register"] = entry.end
            grouped[entry.data.get("device", "unknown")].append(payload)

        devices: list[dict] = []
        for device in sorted(grouped):
            device_entries = grouped[device]
            device_entries.sort(
                key=lambda item: (
                    item.get("start_register", 0),
                    item.get("end_register", 0),
                )
            )
            devices.append(
                {
                    "device": device,
                    "entries": device_entries,
                    "mqtt_keys": mqtt_keys_map.get(device, []),
                    "register_to_mqtt_topic": register_to_topic_map.get(device, {}),
                    "mqtt_topic_to_registers": topic_to_registers_map.get(device, {}),
                }
            )

        return {"devices": devices}

    return collector


def build_inverter_to_mqtt_collector(entries: List[RangeEntry]):
    # Load the full inverter_to_mqtt data for mqtt_keys if present
    inverter_to_mqtt_data = None
    try:
        mqtt_path = INVERTER_TO_MQTT_PATH
        if mqtt_path.exists():
            with open(mqtt_path, encoding="utf-8") as f:
                inverter_to_mqtt_data = json.load(f)
    except FileNotFoundError:
        pass

    def collector(table: str, start: int, end: int) -> Optional[Dict[str, Any]]:
        matches = [
            entry
            for entry in entries
            if entry.table == table
            and ranges_overlap(entry.start, entry.end, start, end)
        ]
        if not matches:
            return None

        grouped: Dict[Tuple[str, str, str, int], Dict[str, Any]] = {}
        # Build per-file var->topic map if available
        var_topic_by_file: dict[str, dict[str, str]] = {}
        if inverter_to_mqtt_data:
            for file_path, info in inverter_to_mqtt_data.get("code", {}).items():
                mapping = info.get("mqtt_var_to_topic", {})
                if isinstance(mapping, dict):
                    var_topic_by_file[file_path] = mapping

        for entry in matches:
            data = entry.data
            operation = data.get("operation") or "read"
            if operation == "read":
                key = (
                    data.get("file", ""),
                    data.get("function", ""),
                    operation,
                    data.get("read_start_register", entry.start),
                )
            else:
                key = (data.get("file", ""), "", operation, entry.start)

            if key not in grouped:
                grouped[key] = {
                    "file": data.get("file"),
                    "function": data.get("function"),
                    "operation": operation,
                    "read_start_register": data.get("read_start_register"),
                    "read_length": data.get("read_length"),
                    "entries": [],
                }

                if operation == "write":
                    grouped[key]["address"] = data.get("address")
                    grouped[key]["call"] = data.get("call")

            if operation == "read":
                grouped[key]["entries"].append(
                    {
                        "variable": data.get("variable"),
                        "registers": data.get("registers"),
                        "buffer_indexes": data.get("buffer_indexes"),
                        "expression": data.get("expression"),
                        "start_register": entry.start,
                        "end_register": entry.end,
                    }
                )
            else:
                grouped[key]["entries"].append(
                    {
                        "start_register": entry.start,
                        "end_register": entry.end,
                    }
                )

        operations = list(grouped.values())
        for operation in operations:
            operation_entries = operation.get("entries", [])
            operation_entries.sort(
                key=lambda item: (
                    item.get("start_register", 0),
                    item.get("end_register", 0),
                )
            )
            # Attach mqtt_key per entry based on file-level mapping
            file_path = operation.get("file") or ""
            var_map = var_topic_by_file.get(file_path, {})
            for ent in operation_entries:
                var = ent.get("variable")
                if isinstance(var, str) and var in var_map:
                    ent["mqtt_key"] = var_map[var]

        operations.sort(
            key=lambda item: (
                item.get("file") or "",
                item.get("operation") or "",
                item.get("read_start_register")
                if item.get("read_start_register") is not None
                else -1,
                item.get("address") if item.get("address") is not None else -1,
            )
        )

        return {"operations": operations}

    return collector


def build_grott_collector(
    entries: List[RangeEntry],
    exported_at: Optional[str],
    version: Optional[str],
    mqtt_topic_template: Optional[str],
):
    meta: Dict[str, Any] = {}
    if exported_at:
        meta["exported_at"] = exported_at
    if version:
        meta["grott_version"] = version
    if mqtt_topic_template:
        meta["mqtt_topic_template"] = mqtt_topic_template

    def collector(table: str, start: int, end: int) -> Optional[Dict[str, Any]]:
        matches = [
            entry
            for entry in entries
            if entry.table == table
            and ranges_overlap(entry.start, entry.end, start, end)
        ]
        if not matches:
            return None

        fields: List[Dict[str, Any]] = []
        for entry in matches:
            payload = dict(entry.data)
            payload["start_register"] = entry.start
            payload["end_register"] = entry.end
            if entry.start == entry.end:
                payload["register"] = entry.start
            fields.append(payload)

        fields.sort(
            key=lambda item: (
                item.get("start_register", 0),
                item.get("end_register", 0),
                item.get("field") or "",
            )
        )

        result: Dict[str, Any] = {"fields": fields}
        result.update(meta)
        return result

    return collector


def collect_enum_values(graph: nx.MultiDiGraph, dtype_id: str) -> List[Dict[str, Any]]:
    values: List[Dict[str, Any]] = []
    if dtype_id not in graph:
        return values
    node_attrs = graph.nodes.get(dtype_id, {})
    if isinstance(node_attrs.get("enum_values"), list):
        for entry in node_attrs["enum_values"]:
            if not isinstance(entry, dict):
                continue
            values.append({
                "value": entry.get("value"),
                "label": entry.get("label"),
                "description": entry.get("description"),
                "sources": entry.get("sources"),
            })
    if values:
        return values
    for _, target, data in graph.out_edges(dtype_id, data=True):
        if data.get("type") == "DATATYPE_HAS_ENUM_VALUE":
            node = graph.nodes.get(target, {})
            if node.get("type") == "enum_value":
                values.append(
                    {
                        "value": node.get("value"),
                        "label": node.get("label"),
                        "description": node.get("description"),
                    }
                )
    values.sort(key=lambda item: item.get("value"))
    return values


def collect_bitflags(graph: nx.MultiDiGraph, node_id: str) -> List[Dict[str, Any]]:
    flags: Dict[int, Dict[str, Any]] = {}
    if node_id not in graph:
        return []
    node_attrs = graph.nodes.get(node_id, {})
    if isinstance(node_attrs.get("bitflags"), list):
        for entry in node_attrs["bitflags"]:
            bit = entry.get("bit")
            if bit is None:
                continue
            flags[bit] = {
                "bit": bit,
                "label": entry.get("label"),
                "description": entry.get("description"),
                "sources": entry.get("sources"),
            }
    if flags:
        return [flags[k] for k in sorted(flags)]
    for _, target, data in graph.out_edges(node_id, data=True):
        if data.get("type") in {"DATATYPE_HAS_BITFLAG", "REGISTER_HAS_BITFLAG"}:
            node = graph.nodes.get(target, {})
            if node.get("type") == "bitflag":
                bit = node.get("bit")
                if bit is None:
                    continue
                flags[bit] = {
                    "bit": bit,
                    "label": node.get("label"),
                    "description": node.get("description"),
                }
    return [flags[k] for k in sorted(flags)]


def collect_register_data(graph: nx.MultiDiGraph, reg_id: str) -> Dict[str, Any]:
    attrs = graph.nodes.get(reg_id, {})
    register_no = attrs.get("register")
    table = attrs.get("table")
    register_info: Dict[str, Any] = {
        "id": reg_id,
        "register": register_no,
    }
    if table:
        register_info["table"] = table

    if attrs.get("attributes"):
        register_info["attributes"] = attrs.get("attributes")
    if attrs.get("families"):
        register_info["families"] = attrs.get("families")
    if attrs.get("manual_descriptions"):
        register_info["descriptions"] = attrs.get("manual_descriptions")

    payloads = attrs.get("payloads") or {}
    if payloads:
        payload_summary = {}
        for source, entries in payloads.items():
            if source == "vendor_range":
                continue
            payload_summary[source] = entries
        register_info["sources"] = payload_summary

    description: Optional[str] = None
    tooltip: Optional[str] = None
    help_text: Optional[str] = None
    unit_hint: Optional[str] = None
    writable = False
    if payloads:
        for source, entries in payload_summary.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                name = entry.get("name") or entry.get("variable")
                if not description and name:
                    description = name
                desc_text = entry.get("description")
                if not tooltip and desc_text:
                    tooltip = desc_text
                note_text = entry.get("note")
                if not help_text and note_text:
                    help_text = note_text
                unit_val = entry.get("unit")
                if not unit_hint and unit_val:
                    unit_hint = unit_val
                access = entry.get("access") or entry.get("write_or_not")
                if isinstance(access, str) and "W" in access.upper():
                    writable = True

    canonical_dtype_id: Optional[str] = None
    canonical_attrs: Dict[str, Any] = {}
    for _, dtype_id, edge_data in graph.out_edges(reg_id, data=True):
        if edge_data.get("type") == "REGISTER_HAS_CANONICAL_DATATYPE":
            canonical_dtype_id = dtype_id
            canonical_attrs = graph.nodes.get(dtype_id, {}) or {}
            break

    data_types: List[Dict[str, Any]] = []
    for _, dtype_id, edge_data in graph.out_edges(reg_id, data=True):
        if edge_data.get("type") != "REGISTER_HAS_DATATYPE":
            continue
        dtype_attrs = graph.nodes.get(dtype_id, {})
        if dtype_attrs.get("type") != "data_type":
            continue
        entry = {
            "id": dtype_id,
            "namespace": dtype_attrs.get("namespace"),
            "length_bytes": dtype_attrs.get("length_bytes"),
            "signed": dtype_attrs.get("signed"),
            "textual": dtype_attrs.get("textual"),
            "text_category": dtype_attrs.get("text_category"),
            "divide": dtype_attrs.get("divide"),
            "scale": dtype_attrs.get("scale"),
            "multiplier": dtype_attrs.get("multiplier"),
            "unit": dtype_attrs.get("unit"),
            "source": edge_data.get("source"),
        }
        enums = collect_enum_values(graph, dtype_id)
        if enums:
            entry["enum_values"] = enums
        bitflags = collect_bitflags(graph, dtype_id)
        if bitflags:
            entry["bitflags"] = bitflags
        if dtype_attrs.get("raw"):
            entry["raw"] = dtype_attrs.get("raw")
        if dtype_attrs.get("annotations"):
            entry["annotations"] = dtype_attrs.get("annotations")
        data_types.append(entry)

    if canonical_dtype_id and canonical_attrs.get("type") == "data_type":
            canonical_entry = {
                "id": canonical_dtype_id,
                "namespace": canonical_attrs.get("namespace"),
                "length_bytes": canonical_attrs.get("length_bytes"),
                "signed": canonical_attrs.get("signed"),
                "textual": canonical_attrs.get("textual"),
                "text_category": canonical_attrs.get("text_category"),
                "divide": canonical_attrs.get("divide"),
                "scale": canonical_attrs.get("scale"),
                "multiplier": canonical_attrs.get("multiplier"),
                "unit": canonical_attrs.get("unit"),
                "annotations": canonical_attrs.get("annotations"),
                "raw": canonical_attrs.get("raw"),
                "sources": canonical_attrs.get("sources"),
                "source": "canonical",
            }
            data_types.append(canonical_entry)
    if canonical_dtype_id:
        register_info["data_type"] = canonical_dtype_id
    elif data_types:
        # No canonical mapping; fall back to first available data type id
        register_info["data_type"] = data_types[0]["id"]

    if data_types:
        unique: Dict[Tuple[Any, Any], Dict[str, Any]] = {}
        for entry in data_types:
            key = (entry.get("id"), entry.get("source"))
            if key not in unique:
                unique[key] = entry
        data_types = list(unique.values())
        preferred_id: Optional[str] = None
        for entry in data_types:
            if entry.get("namespace") == "canonical" and entry.get("text_category"):
                preferred_id = entry.get("id")
                break
        if preferred_id is None and canonical_dtype_id:
            preferred_id = canonical_dtype_id
        if preferred_id is None and data_types:
            preferred_id = data_types[0].get("id")
        if preferred_id:
            register_info["data_type"] = preferred_id
            alt_ids = [
                item["id"]
                for item in data_types
                if item.get("id") and item.get("id") != preferred_id
            ]
            if alt_ids:
                register_info["alternate_data_types"] = sorted(set(alt_ids))

    if canonical_dtype_id and not unit_hint:
        unit_hint = canonical_attrs.get("unit")
    length_bytes = canonical_attrs.get("length_bytes")
    if isinstance(length_bytes, str) and length_bytes.isdigit():
        length_bytes = int(length_bytes)
    data_width_words: Optional[int]
    if isinstance(length_bytes, int) and length_bytes > 0:
        data_width_words = (length_bytes + 1) // 2
    else:
        data_width_words = None

    ha_entities: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for entity_id, _, edge_data in graph.in_edges(reg_id, data=True):
        if edge_data.get("type") != "ENTITY_MAPS_REGISTER":
            continue
        entity_attrs = graph.nodes.get(entity_id, {})
        if entity_attrs.get("type") != "ha_entity":
            continue
        key = (
            entity_attrs.get("device"),
            entity_attrs.get("group"),
            entity_attrs.get("name"),
        )
        ha_entities[key] = {
            "device": entity_attrs.get("device"),
            "group": entity_attrs.get("group"),
            "name": entity_attrs.get("name"),
        }
    if ha_entities:
        register_info.setdefault("home_assistant", []).extend(ha_entities.values())

    if register_info.get("home_assistant"):
        group_devices: Dict[str, set[str]] = {}
        for entry in register_info["home_assistant"]:
            group_name = entry.get("group")
            device_name = entry.get("device")
            if not group_name or not device_name:
                continue
            group_devices.setdefault(group_name, set()).add(device_name)
        if group_devices:
            register_info["device_groups"] = [
                {
                    "group": group,
                    "devices": sorted(devices),
                }
                for group, devices in sorted(group_devices.items())
            ]

    grott_fields: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for field_id, _, edge_data in graph.in_edges(reg_id, data=True):
        if edge_data.get("type") != "FIELD_MAPS_REGISTER":
            continue
        field_attrs = graph.nodes.get(field_id, {})
        if field_attrs.get("type") != "grott_field":
            continue
        key = (field_attrs.get("layout"), field_attrs.get("field"))
        grott_fields[key] = {
            "layout": field_attrs.get("layout"),
            "field": field_attrs.get("field"),
            "byte_offset": field_attrs.get("byte_offset"),
            "length_bytes": field_attrs.get("length_bytes"),
            "divide": field_attrs.get("divide"),
        }
    if grott_fields:
        register_info.setdefault("grott_fields", []).extend(grott_fields.values())

    mqtt_ops: List[Dict[str, Any]] = []
    for op_id, _, edge_data in graph.in_edges(reg_id, data=True):
        edge_type = edge_data.get("type")
        if edge_type not in {
            "MQTT_OPERATION_MAPS_REGISTER",
            "MQTT_OPERATION_WRITES_REGISTER",
        }:
            continue
        op_attrs = graph.nodes.get(op_id, {})
        op_type = op_attrs.get("type")
        if op_type not in {"inverter_to_mqtt_read", "inverter_to_mqtt_write"}:
            continue
        entry = {
            "operation": "read" if op_type.endswith("read") else "write",
            "file": op_attrs.get("file"),
            "function": op_attrs.get("function"),
            "call": op_attrs.get("call"),
            "edge": edge_type,
            "variable": edge_data.get("variable"),
            "expression": edge_data.get("expression"),
            "buffer_indexes": edge_data.get("buffer_indexes"),
            "registers": edge_data.get("registers"),
            "register_count": edge_data.get("register_count"),
            "section": edge_data.get("section"),
        }
        section_id = entry.get("section")
        if section_id:
            section_attrs = graph.nodes.get(section_id, {})
            if section_attrs.get("label"):
                entry["section_label"] = section_attrs.get("label")
        mqtt_ops.append(entry)
    if mqtt_ops:
        register_info["inverter_to_mqtt"] = mqtt_ops

    if description:
        register_info["description"] = description
    if tooltip:
        register_info["tooltip"] = tooltip
    if help_text:
        register_info["help"] = help_text
    if unit_hint:
        register_info["unit"] = unit_hint
    register_info["writable"] = writable
    if data_width_words:
        register_info["data_width_words"] = data_width_words
    if canonical_attrs.get("annotations"):
        register_info["annotations"] = canonical_attrs.get("annotations")

    return register_info


def collect_section_tree(
    graph: nx.MultiDiGraph,
    section_id: str,
    visited: Optional[set[str]] = None,
) -> Dict[str, Any]:
    if visited is None:
        visited = set()
    if section_id in visited:
        return {"id": section_id}
    visited.add(section_id)

    attrs = graph.nodes.get(section_id, {})
    data: Dict[str, Any] = {
        "id": section_id,
        "label": attrs.get("label"),
        "kind": attrs.get("kind"),
        "index": attrs.get("index"),
        "start_register": attrs.get("start_register"),
        "end_register": attrs.get("end_register"),
        "instance_start_register": attrs.get("instance_start_register"),
        "instance_end_register": attrs.get("instance_end_register"),
        "register_offset": attrs.get("register_offset"),
        "slot_size": attrs.get("slot_size"),
    }
    metadata = attrs.get("metadata")
    if metadata:
        data["metadata"] = metadata

    canonical_mappings: List[Dict[str, Any]] = []
    register_instances: List[Dict[str, Any]] = []
    range_links: set[str] = set()
    mirror_links: List[Dict[str, Any]] = []
    child_sections: List[Tuple[Optional[int], str]] = []

    for _, target_id, edge_data in graph.out_edges(section_id, data=True):
        edge_type = edge_data.get("type")
        if edge_type == "SECTION_MAPS_CANONICAL_REGISTER":
            canonical_mappings.append(
                drop_optionals(
                    {
                        "canonical_register": target_id,
                        "instance_register": edge_data.get("instance_register"),
                        "offset": edge_data.get("offset"),
                        "slot_index": edge_data.get("slot_index"),
                    },
                    required=("canonical_register",),
                )
            )
        elif edge_type == "SECTION_CONTAINS_REGISTER":
            target_attrs = graph.nodes.get(target_id, {})
            register_instances.append(
                drop_optionals(
                    {
                        "register": target_attrs.get("register"),
                        "table": target_attrs.get("table"),
                        "offset": edge_data.get("offset"),
                    },
                    required=("register",),
                )
            )
        elif edge_type == "SECTION_IN_RANGE":
            range_links.add(target_id)
        elif edge_type == "SECTION_MIRRORS_SECTION":
            mirror_links.append(
                drop_optionals(
                    {
                        "section": target_id,
                        "offset": edge_data.get("offset"),
                        "slot_index": edge_data.get("slot_index"),
                    },
                    required=("section",),
                )
            )
        elif edge_type == "SECTION_HAS_CHILD":
            child_sections.append((edge_data.get("index"), target_id))

    if canonical_mappings:
        canonical_mappings.sort(key=lambda item: (item.get("offset") or 0, item.get("canonical_register")))
        data["canonical_mappings"] = canonical_mappings

    if register_instances:
        register_instances.sort(key=lambda item: item.get("register", 0))
        data["register_instances"] = register_instances

    if range_links:
        data["ranges"] = sorted(range_links)

    if mirror_links:
        mirror_links.sort(key=lambda item: (item.get("slot_index") or 0, item.get("section")))
        data["mirrors"] = mirror_links

    if child_sections:
        child_sections.sort(key=lambda item: (item[0] if item[0] is not None else 0, item[1]))
        children_payload = [
            collect_section_tree(graph, child_id, visited)
            for _, child_id in child_sections
        ]
        data["sections"] = children_payload
        if attrs.get("kind") == "template" and attrs.get("slot_count"):
            list_payload = {
                "count": attrs.get("slot_count"),
                "stride": attrs.get("slot_size"),
                "instances": [
                    drop_optionals(
                        {
                            "section": child.get("id"),
                            "slot_index": child.get("index"),
                            "instance_start_register": child.get("instance_start_register"),
                            "instance_end_register": child.get("instance_end_register"),
                            "register_offset": child.get("register_offset"),
                        },
                        required=("section",),
                    )
                    for child in children_payload
                ],
            }
            data["list"] = list_payload

    return drop_optionals(data, required=("id",))


def collect_sections_for_range(graph: nx.MultiDiGraph, range_id: str) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for _, section_id, edge_data in graph.out_edges(range_id, data=True):
        if edge_data.get("type") != "RANGE_HAS_SECTION":
            continue
        if section_id in seen:
            continue
        parents = [
            target
            for _, target, edge_info in graph.out_edges(section_id, data=True)
            if edge_info.get("type") == "SECTION_CHILD_OF"
        ]
        if parents:
            parent_in_same_range = False
            for parent in parents:
                edge_bundle = graph.get_edge_data(range_id, parent) or {}
                if any(data.get("type") == "RANGE_HAS_SECTION" for data in edge_bundle.values()):
                    parent_in_same_range = True
                    break
            if parent_in_same_range:
                continue
        sections.append(collect_section_tree(graph, section_id, set()))
        seen.add(section_id)

    sections.sort(
        key=lambda item: (
            item.get("index") if item.get("index") is not None else 0,
            item.get("id"),
        )
    )
    return sections


def build_canonical_registers(graph: nx.MultiDiGraph) -> Dict[str, Dict[str, Any]]:
    canonical: Dict[str, Dict[str, Any]] = {}
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "register":
            continue
        register_info = collect_register_data(graph, node_id)
        if not register_info.get("register") or not register_info.get("table"):
            continue
        canonical[node_id] = drop_optionals(
            register_info,
            required=("id", "register", "table", "data_type"),
        )
    return canonical


def _derive_range_description(range_attrs: Dict[str, Any]) -> Optional[str]:
    metadata = range_attrs.get("metadata") or {}
    for source_key in ("spec", "vendor", "manual"):
        for entry in metadata.get(source_key, []) or []:
            if not isinstance(entry, dict):
                continue
            if entry.get("name"):
                return entry["name"]
            if entry.get("section"):
                return entry["section"]
            if entry.get("variable"):
                return entry["variable"]
    notes = range_attrs.get("notes")
    if isinstance(notes, list) and notes:
        return notes[0]
    return None


def build_ranges_for_table(
    graph: nx.MultiDiGraph,
    table: str,
    canonical_registers: Dict[str, Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
    ranges: List[Dict[str, Any]] = []
    section_cache: Dict[str, List[Dict[str, Any]]] = {}

    for range_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "register_range" or attrs.get("table") != table:
            continue
        start = attrs.get("start_register")
        end = attrs.get("end_register")
        if start is None or end is None:
            continue

        range_info: Dict[str, Any] = {
            "id": range_id,
            "table": table,
            "start_register": start,
            "end_register": end,
            "length": attrs.get("length"),
        }
        description = _derive_range_description(attrs)
        if description:
            range_info["description"] = description
        if attrs.get("notes"):
            range_info["notes"] = attrs.get("notes")
        if attrs.get("metadata"):
            range_info["metadata"] = attrs.get("metadata")

        families: Dict[str, Dict[str, Any]] = {}
        for family_id, _, edge_data in graph.in_edges(range_id, data=True):
            if edge_data.get("type") != "FAMILY_SUPPORTS_RANGE":
                continue
            family_attrs = graph.nodes.get(family_id, {})
            entry = families.setdefault(
                family_id,
                {
                    "id": family_id,
                    "name": family_attrs.get("name"),
                },
            )
            note = edge_data.get("note")
            if note and not entry.get("note"):
                entry["note"] = note
        if families:
            range_info["supported_families"] = [
                families[fam_id]
                for fam_id in sorted(families.keys())
            ]

        sections = collect_sections_for_range(graph, range_id)
        if sections:
            range_info["sections"] = sections
            section_cache[range_id] = sections

        covered_registers: set[str] = set()

        def _collect_section_registers(section: Dict[str, Any]) -> None:
            for mapping in section.get("canonical_mappings", []) or []:
                reg = mapping.get("canonical_register")
                if reg:
                    covered_registers.add(reg)
            for child in section.get("sections", []) or []:
                _collect_section_registers(child)

        for section in sections:
            _collect_section_registers(section)

        canonical_ids: set[str] = set()
        for _, reg_id, edge_data in graph.out_edges(range_id, data=True):
            if edge_data.get("type") != "RANGE_CONTAINS_REGISTER":
                continue
            if reg_id in canonical_registers:
                canonical_ids.add(reg_id)

        remaining = sorted(
            canonical_ids - covered_registers,
            key=lambda reg: canonical_registers[reg]["register"],
        )
        if remaining:
            range_info["canonical_registers"] = remaining

        ranges.append(drop_optionals(range_info, required=("id", "table")))

    ranges.sort(key=lambda item: (item.get("start_register", 0), item.get("end_register", 0)))
    return ranges, section_cache


def build_family_list(
    graph: nx.MultiDiGraph,
    range_sections: Dict[str, List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    families: List[Dict[str, Any]] = []
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "device_family":
            continue
        entry: Dict[str, Any] = {
            "id": node_id,
            "name": attrs.get("name"),
        }
        if attrs.get("aliases"):
            entry["aliases"] = attrs.get("aliases")

        supported_ranges: set[str] = set()
        for _, range_id, edge_data in graph.out_edges(node_id, data=True):
            if edge_data.get("type") == "FAMILY_SUPPORTS_RANGE":
                supported_ranges.add(range_id)
        if supported_ranges:
            entry["ranges"] = sorted(supported_ranges)

        sections: set[str] = set()
        for range_id in supported_ranges:
            for section in range_sections.get(range_id, []):
                sections.add(section.get("id"))
                for child in section.get("sections", []) or []:
                    sections.add(child.get("id"))
        if sections:
            entry["sections"] = sorted(sec for sec in sections if sec)

        families.append(drop_optionals(entry, required=("id", "name")))

    families.sort(key=lambda item: item.get("name") or item["id"])
    return families


def collect_block_sources(
    graph: nx.MultiDiGraph, block_id: str, registers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    sources: Dict[str, Any] = {}

    def add_to_source(name: str, item: Dict[str, Any]) -> None:
        bucket = sources.setdefault(name, [])
        bucket.append(item)

    for reg in registers:
        register_no = reg.get("register")
        payloads: Dict[str, List[Dict[str, Any]]] = reg.get("payloads", {})
        for source_name, rows in payloads.items():
            if source_name in {"vendor", "spec", "manual"}:
                for row in rows:
                    entry = {"register": register_no}
                    entry.update(row)
                    add_to_source(source_name, entry)

    grott_entries: List[Dict[str, Any]] = []
    for reg in registers:
        for field in reg.get("grott_fields", []) or []:
            item = dict(field)
            item["register"] = reg.get("register")
            grott_entries.append(item)
    if grott_entries:
        sources["grott"] = grott_entries

    ha_entries: List[Dict[str, Any]] = []
    ha_group_devices: Dict[str, set[str]] = {}
    ha_by_register: Dict[int, List[Dict[str, Any]]] = {}
    for reg in registers:
        for entity in reg.get("home_assistant", []) or []:
            register_no = reg.get("register")
            item = dict(entity)
            item["register"] = register_no
            ha_entries.append(item)
            if entity.get("group") and entity.get("device"):
                ha_group_devices.setdefault(entity["group"], set()).add(entity["device"])
            if register_no is not None:
                bucket = ha_by_register.setdefault(register_no, [])
                bucket.append(item)
    if ha_entries:
        payload: Dict[str, Any] = {}
        if ha_group_devices:
            payload["groups"] = [
                {
                    "group": group,
                    "devices": sorted(devices),
                }
                for group, devices in sorted(ha_group_devices.items())
            ]
        payload["registers"] = [
            {
                "register": register,
                "entries": items,
            }
            for register, items in sorted(ha_by_register.items())
        ]
        sources["home_assistant"] = payload

    mqtt_entries: List[Dict[str, Any]] = []
    for reg in registers:
        for op in reg.get("inverter_to_mqtt", []) or []:
            item = dict(op)
            item["register"] = reg.get("register")
            mqtt_entries.append(item)
    if mqtt_entries:
        sources["inverter_to_mqtt"] = mqtt_entries

    return sources


def collect_block_from_graph(
    graph: nx.MultiDiGraph, block_id: str
) -> Optional[Dict[str, Any]]:
    attrs = graph.nodes.get(block_id)
    if not attrs or attrs.get("type") != "register_block":
        return None
    table = attrs.get("table")
    start = attrs.get("start_register")
    end = attrs.get("end_register")
    if table is None or start is None or end is None:
        return None

    registers_data: List[Dict[str, Any]] = []
    seen_registers: set[str] = set()
    for _, reg_id, edge_data in graph.out_edges(block_id, data=True):
        if edge_data.get("type") not in {"BLOCK_CONTAINS", "REGISTER_IN_BLOCK"}:
            continue
        node = graph.nodes.get(reg_id, {})
        if node.get("type") != "register":
            continue
        if reg_id in seen_registers:
            continue
        seen_registers.add(reg_id)
        registers_data.append(collect_register_data(graph, reg_id))

    registers_data.sort(key=lambda item: item.get("register", 0))

    sources = collect_block_sources(graph, block_id, registers_data)

    block = {
        "id": block_id,
        "table": table,
        "start_register": start,
        "end_register": end,
        "length": end - start + 1,
        "registers": registers_data,
        "sources": sources,
    }

    block_group_devices: Dict[str, set[str]] = {}
    for register in registers_data:
        for entry in register.get("device_groups", []) or []:
            group_name = entry.get("group")
            devices = entry.get("devices") or []
            if not group_name:
                continue
            bucket = block_group_devices.setdefault(group_name, set())
            for device in devices:
                bucket.add(device)
    if block_group_devices:
        block["device_groups"] = [
            {
                "group": group,
                "devices": sorted(devices),
            }
            for group, devices in sorted(block_group_devices.items())
        ]

    block_vendor_families: Dict[Tuple[str, str, int, int], Dict[str, Any]] = {}
    for family_node, _, edge_data in graph.in_edges(block_id, data=True):
        if edge_data.get("type") != "FAMILY_SUPPORTS_BLOCK":
            continue
        family_attrs = graph.nodes.get(family_node, {})
        table_name = edge_data.get("table")
        start = edge_data.get("range_start")
        end = edge_data.get("range_end")
        note = edge_data.get("note")
        key = (family_node, table_name, start, end)
        entry = block_vendor_families.setdefault(
            key,
            {
                "id": family_node,
                "name": family_attrs.get("name"),
                "table": table_name,
                "start": start,
                "end": end,
                "note": note,
                "aliases": family_attrs.get("aliases"),
                "devices": family_attrs.get("devices"),
            },
        )
        if note and not entry.get("note"):
            entry["note"] = note
    if block_vendor_families:
        block["vendor_families"] = sorted(
            block_vendor_families.values(),
            key=lambda item: (
                item.get("table") or "",
                item.get("start") or -1,
                item.get("end") or -1,
                item.get("id") or "",
            ),
        )

    mirrors: List[Dict[str, Any]] = []
    for _, target, edge_data in graph.out_edges(block_id, data=True):
        if edge_data.get("type") == "BLOCK_MIRRORS_BLOCK":
            mirrors.append(
                {
                    "block": target,
                    "offset": edge_data.get("offset"),
                }
            )
    if mirrors:
        block["mirrors"] = mirrors

    return block


def summarise_vendor_families(graph: nx.MultiDiGraph) -> List[Dict[str, Any]]:
    families: List[Dict[str, Any]] = []
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "device_family":
            continue

        entry: Dict[str, Any] = {
            "id": node_id,
            "name": attrs.get("name"),
        }

        aliases = attrs.get("aliases")
        if aliases:
            entry["aliases"] = aliases

        devices: set[str] = set(attrs.get("devices", []) or [])
        for _, device_node, edge_data in graph.out_edges(node_id, data=True):
            if edge_data.get("type") != "VENDOR_FAMILY_HAS_DEVICE":
                continue
            device_attrs = graph.nodes.get(device_node, {})
            device_name = device_attrs.get("name") or device_node.split(":")[-1]
            devices.add(device_name)
        if devices:
            entry["devices"] = sorted(devices)

        tables: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for _, block_id, edge_data in graph.out_edges(node_id, data=True):
            if edge_data.get("type") != "FAMILY_SUPPORTS_BLOCK":
                continue
            table_name = edge_data.get("table")
            start = edge_data.get("range_start")
            end = edge_data.get("range_end")
            note = edge_data.get("note")
            tables[table_name].append(
                {
                    "start": start,
                    "end": end,
                    "note": note,
                }
            )

        if tables:
            normalised_tables: Dict[str, List[Dict[str, Any]]] = {}
            for table_name, items in tables.items():
                seen: set[Tuple[int, int, Optional[str]]] = set()
                deduped: List[Dict[str, Any]] = []
                for item in items:
                    key = (
                        item.get("start"),
                        item.get("end"),
                        item.get("note"),
                    )
                    if key in seen:
                        continue
                    seen.add(key)
                    deduped.append(item)
                deduped.sort(key=lambda info: (info.get("start") or -1, info.get("end") or -1))
                normalised_tables[table_name] = deduped
            entry["tables"] = normalised_tables

        sources: List[Dict[str, Any]] = []
        for _, source_id, edge_data in graph.out_edges(node_id, data=True):
            if edge_data.get("type") != "SOURCED_FROM":
                continue
            source_attrs = graph.nodes.get(source_id, {})
            sources.append(
                {
                    "id": source_id,
                    "path": source_attrs.get("path"),
                    "sha256": source_attrs.get("sha256"),
                }
            )
        if sources:
            entry["sources"] = sources

    families.append(entry)

    families.sort(key=lambda item: (item.get("name") or "", item["id"]))
    return families


def summarise_data_types(graph: nx.MultiDiGraph) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") != "data_type":
            continue

        namespace = attrs.get("namespace") or "unknown"
        entry: Dict[str, Any] = {
            "id": node_id,
            "namespace": namespace,
            "length_bytes": attrs.get("length_bytes"),
            "signed": attrs.get("signed"),
            "textual": attrs.get("textual"),
            "text_category": attrs.get("text_category"),
            "divide": attrs.get("divide"),
            "scale": attrs.get("scale"),
            "multiplier": attrs.get("multiplier"),
            "unit": attrs.get("unit"),
            "sources": attrs.get("sources"),
            "conflicts": attrs.get("conflicts"),
        }

        enum_values = attrs.get("enum_values") or collect_enum_values(graph, node_id)
        if enum_values:
            entry["enum_values"] = enum_values

        bitflags = attrs.get("bitflags") or collect_bitflags(graph, node_id)
        if bitflags:
            entry["bitflags"] = bitflags

        raw = attrs.get("raw")
        if raw is not None:
            entry["raw"] = raw

        source_datatypes = attrs.get("source_datatypes")
        if source_datatypes:
            entry["source_datatypes"] = source_datatypes
        annotations = attrs.get("annotations")
        if annotations:
            entry["annotations"] = annotations

        grouped[namespace].append(drop_optionals(entry))

    for entries in grouped.values():
        entries.sort(key=lambda item: item.get("id"))

    return grouped


def generate_from_graph(graph: nx.MultiDiGraph) -> Dict[str, Any]:
    canonical_registers = build_canonical_registers(graph)

    tables: Dict[str, Dict[str, Any]] = {}
    range_sections: Dict[str, List[Dict[str, Any]]] = {}
    for table in ("holding", "input"):
        ranges, section_map = build_ranges_for_table(graph, table, canonical_registers)
        tables[table] = {"ranges": ranges}
        range_sections.update(section_map)

    families = build_family_list(graph, range_sections)
    data_types = summarise_data_types(graph)

    source_files = {
        "register_graph": {
            "path": str(GRAPH_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(GRAPH_PATH),
        },
    }

    meta = {
        "version": "0.5.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_consolidated_ref.py",
        "source_files": source_files,
    }

    return {
        "meta": meta,
        "tables": tables,
        "canonical_registers": canonical_registers,
        "families": families,
        "data_types": data_types,
    }


def generate_payload_from_sources() -> Dict[str, Any]:
    vendor_tables = load_json(VENDOR_TABLE_PATH)
    spec_data = load_json(SPEC_PATH)

    ha_data = load_json(HA_LOCAL_PATH) if HA_LOCAL_PATH.exists() else None
    openinverter_data = (
        load_json(OPENINVERTER_PATH) if OPENINVERTER_PATH.exists() else None
    )
    inverter_to_mqtt_data = (
        load_json(INVERTER_TO_MQTT_PATH) if INVERTER_TO_MQTT_PATH.exists() else None
    )
    grott_data = load_json(GROTT_LAYOUTS_PATH) if GROTT_LAYOUTS_PATH.exists() else None

    ha_entries = prepare_home_assistant_entries(ha_data) if ha_data else []
    openinverter_entries = (
        prepare_openinverter_entries(openinverter_data) if openinverter_data else []
    )
    inverter_to_mqtt_entries = (
        prepare_inverter_to_mqtt_entries(inverter_to_mqtt_data)
        if inverter_to_mqtt_data
        else []
    )
    grott_entries = prepare_grott_entries(grott_data) if grott_data else []

    external_collectors: Dict[
        str, Callable[[str, int, int], Optional[Dict[str, Any]]]
    ] = {}
    if ha_entries:
        external_collectors["home_assistant"] = build_home_assistant_collector(
            ha_entries
        )
    if openinverter_entries:
        external_collectors["openinverter_gateway"] = build_openinverter_collector(
            openinverter_entries
        )
    if inverter_to_mqtt_entries:
        external_collectors["inverter_to_mqtt"] = build_inverter_to_mqtt_collector(
            inverter_to_mqtt_entries
        )
    if grott_entries:
        external_collectors["grott"] = build_grott_collector(
            grott_entries,
            grott_data.get("exported_at") if grott_data else None,
            grott_data.get("grott_version") if grott_data else None,
            grott_data.get("mqtt_topic_template") if grott_data else None,
        )

    holding_index, holding_orphans, holding_order = build_vendor_index(
        vendor_tables.get("holding", []), "holding"
    )
    input_index, input_orphans, input_order = build_vendor_index(
        vendor_tables.get("input", []), "input"
    )

    holding_blocks, used_holding = build_register_blocks(
        "holding",
        spec_data.get("holding", []),
        holding_index,
        holding_order,
        external_collectors or None,
    )
    input_blocks, used_input = build_register_blocks(
        "input",
        spec_data.get("input", []),
        input_index,
        input_order,
        external_collectors or None,
    )

    holding_orphan_rows = collect_orphan_vendor_rows(
        holding_index, holding_orphans, used_holding
    )
    input_orphan_rows = collect_orphan_vendor_rows(
        input_index, input_orphans, used_input
    )

    source_files: Dict[str, Any] = {
        "vendor_tables": {
            "path": str(VENDOR_TABLE_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(VENDOR_TABLE_PATH),
        },
        "spec_json": {
            "path": str(SPEC_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(SPEC_PATH),
        },
    }
    if ha_data:
        source_files["ha_local"] = {
            "path": str(HA_LOCAL_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(HA_LOCAL_PATH),
        }
    if openinverter_data:
        source_files["openinverter_gateway"] = {
            "path": str(OPENINVERTER_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(OPENINVERTER_PATH),
        }
    if inverter_to_mqtt_data:
        source_files["inverter_to_mqtt"] = {
            "path": str(INVERTER_TO_MQTT_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(INVERTER_TO_MQTT_PATH),
        }
    if grott_data:
        source_files["grott_register_layouts"] = {
            "path": str(GROTT_LAYOUTS_PATH.relative_to(DOC_DIR)),
            "sha256": sha256sum(GROTT_LAYOUTS_PATH),
        }

    meta = {
        "version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_consolidated_ref.py",
        "source_files": source_files,
    }

    tables = {
        "holding": {
            "register_blocks": holding_blocks,
            "orphan_vendor_rows": holding_orphan_rows,
        },
        "input": {
            "register_blocks": input_blocks,
            "orphan_vendor_rows": input_orphan_rows,
        },
    }

    return {
        "meta": meta,
        "tables": tables,
    }


def generate_payload() -> Dict[str, Any]:
    graph = load_graph(GRAPH_PATH)
    if graph is not None:
        return generate_from_graph(graph)
    return generate_payload_from_sources()


def _prune_redundant_mqtt_tables(node: Any) -> Any:
    """Recursively remove redundant MQTT mapping tables from payload."""
    if isinstance(node, dict):
        # Keys to remove entirely
        drop_keys = {
            "mqtt_keys",
            "register_to_mqtt_topic",
            "mqtt_topic_to_registers",
        }
        cleaned: dict[str, Any] = {}
        for k, v in node.items():
            if k in drop_keys:
                continue
            cleaned[k] = _prune_redundant_mqtt_tables(v)
        return cleaned
    if isinstance(node, list):
        return [_prune_redundant_mqtt_tables(item) for item in node]
    return node


def main() -> None:
    payload = generate_payload()
    # Final compacting pass: remove redundant MQTT tables
    payload = _prune_redundant_mqtt_tables(payload)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
