#!/usr/bin/env python3
"""Render growatt_registers_spec.md from the JSON specification.

Usage:
    python render_register_spec.py
The script expects ``growatt_registers_spec.json`` (spec extraction) and
``growatt_local_registers.json`` (current integration mapping) to live in the
same directory.  The Markdown output is written beside them.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DOC_DIR = Path(__file__).resolve().parent
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
MAPPING_PATH = DOC_DIR / "growatt_local_registers.json"
OUTPUT_PATH = DOC_DIR / "growatt_registers_spec.md"
REPO_ROOT = DOC_DIR.parent

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str((REPO_ROOT / "custom_components").resolve()))

from growatt_local.sensor_types import inverter as inverter_sensors
from growatt_local.sensor_types import storage as storage_sensors
from growatt_local.sensor_types import offgrid as offgrid_sensors

REG_RANGE = re.compile(r"^(\d+)[–-](\d+)$")
REG_SINGLE = re.compile(r"^(\d+)")


@dataclass(slots=True)
class Category:
    title: str
    description: str
    table_type: str  # "holding" or "input"
    ranges: tuple[tuple[int, int], ...]
    code_groups: tuple[tuple[str, str], ...]
    applies_to: tuple[str, ...]


CATEGORY_DEFINITIONS: tuple[Category, ...] = (
    Category(
        title="Common Holding Registers (0–124)",
        description="Applies to TL-X/TL-XH, TL3/MAX/MID/MAC, and MIX/SPA/SPH storage families.",
        table_type="holding",
        ranges=((0, 124),),
        code_groups=(
            ("tlx", "holding_common"),
            ("tl3", "holding_common"),
            ("storage", "holding_common"),
        ),
        applies_to=("TL-X/TL-XH/TL-XH US", "TL3-X/MAX/MID/MAC", "Storage (MIX/SPA/SPH)"),
    ),
    Category(
        title="TL-X/TL-XH Holding Registers (3000–3124)",
        description="Additional holding registers for TL-X/TL-XH hybrids (MIN series).",
        table_type="holding",
        ranges=((3000, 3124),),
        code_groups=(("tlx", "holding_common"),),
        applies_to=("TL-X/TL-XH/TL-XH US",),
    ),
    Category(
        title="TL-XH US Holding Registers (3125–3249)",
        description="US-specific time schedule and dry-contact configuration registers.",
        table_type="holding",
        ranges=((3125, 3249),),
        code_groups=(("tlx", "holding_common"),),
        applies_to=("TL-XH US",),
    ),
    Category(
        title="TL3/MAX/MID/MAC Holding Registers (125–249)",
        description="Three-phase inverter specific holding registers.",
        table_type="holding",
        ranges=((125, 249),),
        code_groups=(("tl3", "holding_common"),),
        applies_to=("TL3-X/MAX/MID/MAC",),
    ),
    Category(
        title="Storage Holding Registers (1000–1124)",
        description="Storage (MIX/SPA/SPH) battery configuration holding registers.",
        table_type="holding",
        ranges=((1000, 1124),),
        code_groups=(("storage", "holding_common"),),
        applies_to=("Storage (MIX/SPA/SPH)",),
    ),
    Category(
        title="Storage Holding Registers (1125–1249)",
        description="Additional SPA/SPH storage configuration registers.",
        table_type="holding",
        ranges=((1125, 1249),),
        code_groups=(("storage", "holding_common"),),
        applies_to=("Storage SPA/SPH",),
    ),
    Category(
        title="Common Input Registers (0–124)",
        description="Applies to TL3/MAX and legacy inverters for basic PV/AC telemetry.",
        table_type="input",
        ranges=((0, 124),),
        code_groups=(
            ("tlx", "input_common"),
            ("tl3", "input_common"),
            ("storage", "input_common"),
            ("offgrid", "input"),
        ),
        applies_to=("TL-X/TL-XH (legacy mode)", "TL3-X/MAX/MID/MAC", "Storage MIX/SPA/SPH", "Offgrid SPF"),
    ),
    Category(
        title="TL-X/TL-XH Input Registers (3000–3124)",
        description="Primary TL-X/TL-XH telemetry mirror (PV/AC metrics).",
        table_type="input",
        ranges=((3000, 3124),),
        code_groups=(("tlx", "input_tl_xh"),),
        applies_to=("TL-X/TL-XH/TL-XH US",),
    ),
    Category(
        title="TL-X/TL-XH Battery & Hybrid Input Registers (3125–3249)",
        description="Battery energy, power flow, and BMS telemetry for TL-XH hybrids.",
        table_type="input",
        ranges=((3125, 3249),),
        code_groups=(("tlx", "input_tl_xh"), ("storage", "input_tl_xh")),
        applies_to=("TL-X/TL-XH hybrids", "Storage TL-XH"),
    ),
    Category(
        title="TL-X/TL-XH Extended Input Registers (3250–3374)",
        description="Extended diagnostics and reserved registers for TL-XH hybrids.",
        table_type="input",
        ranges=((3250, 3374),),
        code_groups=(("tlx", "input_tl_xh"),),
        applies_to=("TL-X/TL-XH hybrids",),
    ),
    Category(
        title="Storage Input Registers (1000–1124)",
        description="Storage (MIX/SPA/SPH) core telemetry.",
        table_type="input",
        ranges=((1000, 1124),),
        code_groups=(("storage", "input_common"),),
        applies_to=("Storage (MIX/SPA/SPH)",),
    ),
    Category(
        title="Storage Input Registers (1125–1249)",
        description="Additional SPA/SPH telemetry (e.g., DRMS, schedules).",
        table_type="input",
        ranges=((1125, 1249),),
        code_groups=(("storage", "input_common"),),
        applies_to=("Storage SPA/SPH",),
    ),
    Category(
        title="Storage Input Registers (2000–2124)",
        description="SPA-specific grid interaction telemetry.",
        table_type="input",
        ranges=((2000, 2124),),
        code_groups=(("storage", "input_common"),),
        applies_to=("Storage SPA",),
    ),
    Category(
        title="Storage TL-XH Input Registers (3041–3231)",
        description="BDC telemetry (battery module data) for TL-XH hybrids.",
        table_type="input",
        ranges=((3041, 3231),),
        code_groups=(("storage", "input_tl_xh"),),
        applies_to=("Storage TL-XH",),
    ),
    Category(
        title="Offgrid SPF Input Registers",
        description="Observed off-grid register map (from integration implementation).",
        table_type="input",
        ranges=((0, 9999),),
        code_groups=(("offgrid", "input"),),
        applies_to=("Offgrid SPF",),
    ),
)


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Required file missing: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_entries(entries: list[dict]) -> list[dict]:
    normalised: list[dict] = []
    for entry in entries:
        register_field = entry.get("register")
        if isinstance(register_field, int):
            reg_text = str(register_field)
        else:
            reg_text = (register_field or "").replace(" ", "")
        start: int | None
        end: int | None
        if match := REG_RANGE.match(reg_text):
            start = int(match.group(1))
            end = int(match.group(2))
        elif match := REG_SINGLE.match(reg_text):
            start = end = int(match.group(1))
        else:
            start = end = None
        normalised.append({
            **entry,
            "register_start": entry.get("register_start", start),
            "register_end": entry.get("register_end", end if end is not None else start),
        })
    return normalised


def clean_text(text: str | None) -> str:
    if not text:
        return "—"
    text = text.replace("\n", " ")
    replacements = {
        "（": "(",
        "）": ")",
        "，": ",",
        "；": ";",
        "：": ":",
        "。": ".",
        "、": ", ",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text if text else "—"


def value_in_ranges(value: int | None, ranges: Iterable[tuple[int, int]]) -> bool:
    if value is None:
        return False
    return any(start <= value <= end for start, end in ranges)


def build_register_sets(mapping: dict) -> dict[str, dict[str, set[int]]]:
    register_sets: dict[str, dict[str, set[int]]] = {}
    for family, groups in mapping.items():
        family_sets: dict[str, set[int]] = {}
        for group_name, entries in groups.items():
            regs = {entry["register"] for entry in entries}
            family_sets[group_name] = regs
        register_sets[family] = family_sets
    return register_sets


def coverage_stats(entries: list[dict], register_sets: dict[str, dict[str, set[int]]], groups: tuple[tuple[str, str], ...]) -> tuple[int, int, int]:
    spec_regs = {entry.get("register_start") for entry in entries if entry.get("register_start") is not None}
    code_regs: set[int] = set()
    for family, group in groups:
        code_regs.update(register_sets.get(family, {}).get(group, set()))
    covered = spec_regs & code_regs
    missing = spec_regs - code_regs
    return len(spec_regs), len(covered), len(missing)


def collect_attribute_info(category: Category, entry: dict, mapping: dict, attribute_to_sensors: dict[str, set[str]]) -> tuple[str, str]:
    attrs: list[str] = []
    sensor_names: set[str] = set()
    register = entry.get("register_start")
    if register is None:
        return "—", "—"
    for family, group in category.code_groups:
        group_entries = mapping.get(family, {}).get(group, [])
        for item in group_entries:
            if item["register"] == register:
                attr_name = item["name"]
                attrs.append(f"{family}:{attr_name}")
                sensor_names.update(attribute_to_sensors.get(attr_name, set()))
                break
    attr_text = ", ".join(attrs) if attrs else "—"
    sensor_text = ", ".join(sorted(sensor_names)) if sensor_names else "—"
    return attr_text, sensor_text


def render_markdown(spec: dict, mapping: dict) -> str:
    holding_entries = normalize_entries(spec.get("holding", []))
    input_entries = normalize_entries(spec.get("input", []))

    attribute_to_sensors: dict[str, set[str]] = defaultdict(set)
    for desc in inverter_sensors.INVERTER_SENSOR_TYPES:
        attribute_to_sensors[desc.key].add(desc.name)
    for desc in storage_sensors.STORAGE_SENSOR_TYPES:
        attribute_to_sensors[desc.key].add(desc.name)
    for desc in offgrid_sensors.OFFGRID_SENSOR_TYPES:
        attribute_to_sensors[desc.key].add(desc.name)

    register_sets = build_register_sets(mapping)

    lines: list[str] = []
    lines.append("# Growatt Modbus Register Map (Protocol v1.24)")
    lines.append("")
    lines.append(
        "This file is generated from `growatt_registers_spec.json` (parsed from the official Modbus RTU protocol) and cross-references the Home Assistant `growatt_local` integration."
    )
    lines.append("")
    lines.append(
        "**Legend**: Access = spec write flag (`R`, `W`, `R/W`). “Range/Unit” merges the spec range column with the unit, when available. “Attributes” lists the integration attribute(s) mapped to the register; “Sensors” lists Home Assistant sensor entities exposing the attribute. Rows without attributes are not currently surfaced by the integration (typically configuration or reserved registers)."
    )
    lines.append("")
    lines.append(
        "*Descriptions and notes are copied verbatim from the PDF specification. Some spacing may appear collapsed due to automated extraction; consult the original document when exact phrasing is required.*"
    )
    lines.append("")

    summary_header = ["Section", "Spec Registers", "Covered", "Missing"]
    lines.append("## Coverage Summary")
    lines.append("| " + " | ".join(summary_header) + " |")
    lines.append("|" + "|".join([" --- "] * len(summary_header)) + "|")
    for category in CATEGORY_DEFINITIONS:
        entry_source = holding_entries if category.table_type == "holding" else input_entries
        section_entries = [
            entry for entry in entry_source if value_in_ranges(entry.get("register_start"), category.ranges)
        ]
        spec_total, covered, missing = coverage_stats(section_entries, register_sets, category.code_groups)
        lines.append(f"| {category.title} | {spec_total} | {covered} | {missing} |")
    lines.append("")

    for category in CATEGORY_DEFINITIONS:
        entry_source = holding_entries if category.table_type == "holding" else input_entries
        section_entries = [
            entry for entry in entry_source if value_in_ranges(entry.get("register_start"), category.ranges)
        ]
        if not section_entries:
            continue
        lines.append(f"## {category.title}")
        lines.append(category.description)
        lines.append("")
        if category.applies_to:
            lines.append("**Applies to:** " + ", ".join(category.applies_to))
            lines.append("")
        header = [
            "Register",
            "Name",
            "Description",
            "Access",
            "Range/Unit",
            "Initial",
            "Notes",
            "Attributes",
            "Sensors",
        ]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join([" --- "] * len(header)) + "|")
        for entry in section_entries:
            register = entry.get("register", "—")
            name = clean_text(entry.get("name"))
            description = clean_text(entry.get("description"))
            access = entry.get("access", "—") or "—"
            range_unit = " ".join(
                filter(None, [clean_text(entry.get("value")), clean_text(entry.get("unit"))])
            ).strip()
            range_unit = range_unit if range_unit and range_unit != "— —" else "—"
            initial = clean_text(entry.get("initial"))
            notes = clean_text(entry.get("note"))
            attrs, sensors = collect_attribute_info(category, entry, mapping, attribute_to_sensors)
            row = [
                str(register),
                name,
                description,
                access,
                range_unit,
                initial,
                notes,
                attrs,
                sensors,
            ]
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    spec = load_json(SPEC_PATH)
    mapping = load_json(MAPPING_PATH)
    markdown = render_markdown(spec, mapping)
    OUTPUT_PATH.write_text(markdown + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(DOC_DIR)}")


if __name__ == "__main__":
    main()
