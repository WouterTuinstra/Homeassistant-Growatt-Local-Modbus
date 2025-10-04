#!/usr/bin/env python3
"""Compare OpenInverterGateway register metadata with the HA spec.

The OpenInverterGateway project ships an Arduino implementation of the
ShineWiFi-X protocol that includes hard-coded register definitions.  This
script parses the TL-XH mapping from ``GrowattTLXH.cpp`` and cross-references
the fields against ``growatt_registers_spec.json`` / ``growatt_register_data_types.json``
used by the Home Assistant ``growatt_local`` integration.

The resulting Markdown summary highlights addresses where the two sources
disagree (scale, units, signedness, etc.) and documents registers that only
appear in one mapping.  Run the script from the repository root:

```
python external/Homeassistant-Growatt-Local-Modbus/doc/compare_openinverter_gateway.py
```

The report is written to ``doc/ref/openinverter_gateway_comparison.md``.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_DIR = Path(__file__).resolve().parent
OIG_PATH = (
    REPO_ROOT
    / "external"
    / "OpenInverterGateway"
    / "SRC"
    / "ShineWiFi-ModBus"
    / "GrowattTLXH.cpp"
)
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
TYPE_PATH = DOC_DIR / "growatt_register_data_types.json"
OUTPUT_PATH = DOC_DIR / "ref" / "openinverter_gateway_comparison.md"


SIZE_MAP = {
    "SIZE_16BIT": 1,
    "SIZE_32BIT": 2,
    "SIZE_16BIT_S": 1,
    "SIZE_32BIT_S": 2,
}

UNIT_MAP = {
    "NONE": None,
    "POWER_W": "W",
    "POWER_KWH": "kWh",
    "VOLTAGE": "V",
    "CURRENT": "A",
    "SECONDS": "s",
    "PERCENTAGE": "%",
    "FREQUENCY": "Hz",
    "TEMPERATURE": "°C",
    "VA": "VA",
    "CURRENT_M": "mA",
    "RESISTANCE_K": "kΩ",
    "POWER_REACTIVE": "var",
}


@dataclass(slots=True)
class OIGEntry:
    table: str
    address: int
    name: str
    registers: int | None
    signed: bool
    multiplier: float
    unit: str | None


@dataclass(slots=True)
class SpecEntry:
    table: str
    address: int
    name: str
    registers: int | None
    signed: bool | None
    multiplier: float | None
    unit: str | None


def parse_oig_registers() -> tuple[dict[str, dict[int, list[OIGEntry]]], dict[str, list[int]]]:
    """Extract register metadata from OpenInverterGateway."""

    text = OIG_PATH.read_text()
    pattern = re.compile(
        r"Protocol\.(Input|Holding)Registers\[[^\]]+\]\s*=\s*sGrowattModbusReg_t\s*{([^}]*)}",
        re.DOTALL,
    )

    tables: dict[str, dict[int, list[OIGEntry]]] = {
        "input": defaultdict(list),
        "holding": defaultdict(list),
    }

    for match in pattern.finditer(text):
        table = match.group(1).lower()
        block = match.group(2)

        lines: list[str] = []
        for raw_line in block.splitlines():
            line = raw_line.split("//", 1)[0].strip()
            if line:
                lines.append(line)
        if not lines:
            continue

        tokens = [tok.strip() for tok in " ".join(lines).split(",") if tok.strip()]
        address = int(tokens[0], 0)
        size_token = tokens[2]
        registers = SIZE_MAP.get(size_token)
        signed = size_token.endswith("_S")
        name_token = tokens[3]
        name = (
            name_token[3:-2]
            if name_token.startswith('F("') and name_token.endswith('")')
            else name_token
        )
        multiplier = float(tokens[4])
        unit_token = tokens[6]
        unit = UNIT_MAP.get(unit_token, unit_token)

        tables[table][address].append(
            OIGEntry(
                table=table,
                address=address,
                name=name,
                registers=registers,
                signed=signed,
                multiplier=multiplier,
                unit=unit,
            )
        )

    duplicates = {
        table: [addr for addr, entries in table_map.items() if len(entries) > 1]
        for table, table_map in tables.items()
    }
    return tables, duplicates


def load_spec_entries() -> dict[str, dict[int, SpecEntry]]:
    spec = json.loads(SPEC_PATH.read_text())
    type_info = json.loads(TYPE_PATH.read_text())["types"]

    tables: dict[str, dict[int, SpecEntry]] = {"input": {}, "holding": {}}

    for table in ("input", "holding"):
        for entry in spec[table]:
            if entry.get("type") != "entry":
                continue
            address = entry["register"]
            start = entry["register_start"]
            end = entry.get("register_end", start)
            registers = end - start + 1
            dtype = entry.get("data_type")
            dtype_info = type_info.get(dtype) if dtype else None
            if dtype_info:
                registers = dtype_info.get("registers", registers)
            scale = dtype_info.get("scale") if dtype_info else None
            unit = entry.get("unit") or (dtype_info.get("unit") if dtype_info else None)
            signed = None
            if dtype_info and dtype_info.get("kind"):
                signed = "signed" in dtype_info["kind"]

            tables[table][address] = SpecEntry(
                table=table,
                address=address,
                name=entry["name"],
                registers=registers,
                signed=signed,
                multiplier=(1 / scale) if scale else None,
                unit=unit,
            )

    return tables


def describe_oig(entry: OIGEntry) -> str:
    signed = "signed" if entry.signed else "unsigned"
    regs = f"{entry.registers or '?'} reg"
    unit = entry.unit or "—"
    return f"{entry.name} ({signed}, {regs}, ×{entry.multiplier:g} {unit})"


def describe_spec(entry: SpecEntry) -> str:
    signed = (
        "signed"
        if entry.signed
        else ("unsigned" if entry.signed is not None else "unspecified")
    )
    regs = f"{entry.registers or '?'} reg"
    unit = entry.unit or "—"
    mult = f"×{entry.multiplier:g}" if entry.multiplier is not None else "×?"
    return f"{entry.name} ({signed}, {regs}, {mult} {unit})"


def build_report() -> str:
    oig_tables, duplicates = parse_oig_registers()
    spec_tables = load_spec_entries()

    mismatches: list[tuple[OIGEntry, SpecEntry, list[str]]] = []
    missing_in_spec: list[OIGEntry] = []

    for table, oig_entries in oig_tables.items():
        spec_entries = spec_tables[table]
        for address, entries in oig_entries.items():
            spec_entry = spec_entries.get(address)
            if spec_entry is None:
                missing_in_spec.extend(entries)
                continue
            for entry in entries:
                issues: list[str] = []
                if (
                    spec_entry.registers is not None
                    and entry.registers is not None
                    and spec_entry.registers != entry.registers
                ):
                    issues.append(
                        f"register width {entry.registers} vs {spec_entry.registers}"
                    )
                if spec_entry.signed is not None and entry.signed != spec_entry.signed:
                    issues.append(
                        "signed" if entry.signed else "unsigned"
                        + " vs "
                        + ("signed" if spec_entry.signed else "unsigned")
                    )
                if spec_entry.unit and entry.unit != spec_entry.unit:
                    issues.append(f"unit {entry.unit or '—'} vs {spec_entry.unit}")
                if (
                    spec_entry.multiplier is not None
                    and abs(entry.multiplier - spec_entry.multiplier) > 1e-9
                ):
                    issues.append(
                        f"scale ×{entry.multiplier:g} vs ×{spec_entry.multiplier:g}"
                    )
                if issues:
                    mismatches.append((entry, spec_entry, issues))

    missing_counts = Counter("holding" if m.table == "holding" else "input" for m in missing_in_spec)

    missing_in_open: list[SpecEntry] = []
    for table, spec_entries in spec_tables.items():
        for address, spec_entry in spec_entries.items():
            if address not in oig_tables[table]:
                missing_in_open.append(spec_entry)

    # Filter missing-in-open entries to ranges that OIG partially covers for readability.
    missing_in_open_tlxh = [
        entry
        for entry in missing_in_open
        if entry.table == "input" and 3000 <= entry.address <= 3184
    ]
    missing_bms = [
        entry
        for entry in missing_in_open
        if entry.table == "input" and 3185 <= entry.address <= 3249
    ]

    def format_issue_list(issues: Iterable[str]) -> str:
        return ", ".join(issues)

    lines: list[str] = []
    lines.append("# OpenInverterGateway TL-XH register comparison")
    lines.append("")
    lines.append(
        "This report is generated by ``compare_openinverter_gateway.py`` and compares "
        "the TL-XH register metadata bundled with the OpenInverterGateway project "
        "against the Home Assistant register specification."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"* Found {len(mismatches)} register(s) where the two sources disagree "
        "on units, scaling, or signedness."
    )
    lines.append(
        f"* OpenInverterGateway defines {missing_counts['input']} input "
        "register(s) that are absent from the Home Assistant spec."
    )
    if missing_counts["holding"]:
        lines.append(
            f"* OpenInverterGateway includes {missing_counts['holding']} holding "
            "register(s) that are not documented in the spec."
        )
    lines.append(
        "* The Home Assistant spec still lists "
        f"{len(missing_in_open_tlxh)} TL-XH telemetry register(s) (3000–3184) "
        "missing from OpenInverterGateway and "
        f"{len(missing_bms)} additional BMS address(es) in the 3185–3249 block."
    )
    for table, dupes in duplicates.items():
        if dupes:
            joined = ", ".join(str(addr) for addr in sorted(dupes))
            lines.append(
                f"* OpenInverterGateway defines multiple names for {table} register(s) {joined}."
            )
    lines.append("")

    if mismatches:
        lines.append("## Conflicting metadata")
        lines.append("")
        lines.append(
            "| Address | OpenInverterGateway | Home Assistant spec | Differences |"
        )
        lines.append("| --- | --- | --- | --- |")
        for entry, spec_entry, issues in sorted(
            mismatches, key=lambda row: (row[0].table, row[0].address, row[0].name)
        ):
            lines.append(
                "| "
                + f"{entry.address}"
                + " | "
                + describe_oig(entry)
                + " | "
                + describe_spec(spec_entry)
                + " | "
                + format_issue_list(issues)
                + " |"
            )
        lines.append("")

    if missing_in_spec:
        lines.append("## Registers missing from the Home Assistant spec")
        lines.append("")
        lines.append(
            "The following addresses are present in ``GrowattTLXH.cpp`` but do not "
            "appear in ``growatt_registers_spec.json``. Names are taken from the "
            "OpenInverterGateway source."
        )
        lines.append("")
        lines.append("| Table | Address | Name |")
        lines.append("| --- | --- | --- |")
        for entry in sorted(missing_in_spec, key=lambda item: (item.table, item.address, item.name)):
            lines.append(f"| {entry.table} | {entry.address} | {entry.name} |")
        lines.append("")

    if missing_in_open_tlxh or missing_bms:
        lines.append("## Registers missing from OpenInverterGateway")
        lines.append("")
        if missing_in_open_tlxh:
            lines.append("### TL-XH telemetry block (3000–3184)")
            lines.append("")
            lines.append("| Address | Name |")
            lines.append("| --- | --- |")
            for spec_entry in sorted(
                missing_in_open_tlxh, key=lambda item: item.address
            ):
                lines.append(f"| {spec_entry.address} | {spec_entry.name} |")
            lines.append("")
        if missing_bms:
            lines.append("### BMS / battery detail block (3185–3249)")
            lines.append("")
            lines.append(
                "OpenInverterGateway stops at register 3184 and omits the "
                "downstream BMS telemetry block present in the Home Assistant spec."
            )
            lines.append("")
            lines.append(
                f"*Home Assistant covers {len(missing_bms)} addresses in this range; see the main spec for details.*"
            )
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUTPUT_PATH.write_text(build_report())


if __name__ == "__main__":
    main()
