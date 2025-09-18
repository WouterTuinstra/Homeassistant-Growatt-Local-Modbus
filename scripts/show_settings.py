"""Utility to inspect Growatt Modbus register catalog and capture snapshots.

This CLI consumes the structured register specification under
``doc/growatt_registers_spec.json`` together with the data-type catalogue
``doc/growatt_register_data_types.json``.  It can:

* decode holding/input register dumps from a live inverter (via the Modbus
  proxy that ships with Home Assistant),
* render the interpreted values to the terminal or JSON,
* persist snapshots that can be replayed by the simulator, and
* synthesise default snapshots with realistic placeholder values for pytest.

The module exposes helper classes (`RegisterSpec`, `DataTypeCatalog`) that are
imported by the unit tests to validate decoding behaviour.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

# Ensure repository modules (custom_components) are importable when the script
# is executed directly from a cloned checkout.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
CUSTOM_COMPONENTS = REPO_ROOT / "custom_components"
if str(CUSTOM_COMPONENTS) not in sys.path:
    sys.path.insert(0, str(CUSTOM_COMPONENTS))

from custom_components.growatt_local.API.const import DeviceTypes
from custom_components.growatt_local.API.growatt import (  # type: ignore
    GrowattNetwork,
    get_register_information,
)

LOG = logging.getLogger("growatt.show_settings")

DOC_DIR = REPO_ROOT / "doc"
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
DATA_TYPES_PATH = DOC_DIR / "growatt_register_data_types.json"
SNAPSHOT_DIR = REPO_ROOT / "testing" / "snapshots"

FAMILY_DEVICE_TYPES: dict[str, List[DeviceTypes]] = {
    "tlx": [DeviceTypes.INVERTER_120, DeviceTypes.HYBRID_120_TL_XH],
    "storage": [DeviceTypes.STORAGE_120, DeviceTypes.HYBRID_120],
    "tl3": [DeviceTypes.INVERTER_315],
    "offgrid": [DeviceTypes.OFFGRID_SPF],
}
FAMILY_DEFAULT_DEVICE: dict[str, DeviceTypes] = {
    family: types[0] for family, types in FAMILY_DEVICE_TYPES.items()
}

DEFAULT_ASCII_SERIAL: dict[str, str] = {
    "tlx": "TLX42A0010",
    "storage": "STO42B0021",
    "tl3": "TL342C0032",
    "offgrid": "OFF42D0043",
}
DEFAULT_FIRMWARE_SEGMENTS: dict[str, Dict[str, str]] = {
    "tlx": {"inverter": "INV2.5", "control": "COM1.7"},
    "storage": {"inverter": "INV1.9", "control": "COM1.4"},
    "tl3": {"inverter": "INV3.6", "control": "COM2.1"},
    "offgrid": {"inverter": "INV1.4", "control": "COM0.9"},
}
MANUFACTURER_STRING = "Growatt Power    "  # 16 characters

# ---------------------------------------------------------------------------
# Helpers for type conversion
# ---------------------------------------------------------------------------

def _combine_registers(values: Sequence[int], *, signed: bool = False) -> int:
    """Combine ``values`` (big-endian) into a single integer."""

    result = 0
    for value in values:
        result = (result << 16) | (value & 0xFFFF)
    if signed:
        bits = 16 * len(values)
        sign_bit = 1 << (bits - 1)
        if result & sign_bit:
            result -= 1 << bits
    return result


def _split_registers(value: int, length: int) -> List[int]:
    """Split ``value`` into ``length`` 16-bit registers (big-endian)."""

    if length <= 0:
        return []
    bits = length * 16
    mask = (1 << bits) - 1
    value &= mask
    regs: List[int] = []
    for shift in reversed(range(length)):
        regs.append((value >> (shift * 16)) & 0xFFFF)
    return regs


def _decode_ascii(registers: Sequence[int], *, strip_nulls: bool = True) -> str:
    chars: List[str] = []
    for value in registers:
        chars.append(chr((value >> 8) & 0xFF))
        chars.append(chr(value & 0xFF))
    text = "".join(chars)
    return text.rstrip("\x00") if strip_nulls else text


def _encode_ascii(text: str, length: int) -> List[int]:
    data = text[: length * 2].ljust(length * 2, " ")
    regs: List[int] = []
    for idx in range(0, len(data), 2):
        regs.append((ord(data[idx]) << 8) | ord(data[idx + 1]))
    while len(regs) < length:
        regs.append(0)
    return regs[:length]


# ---------------------------------------------------------------------------
# Data classes for registers and decoded output
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class RegisterEntry:
    table: str
    address: int
    end_address: int
    length: int
    name: str
    description: Optional[str]
    category: Optional[str]
    unit: Optional[str]
    data_type: Optional[str]
    attributes: List[str]
    families: List[str]
    read_write: bool
    source: Optional[str]
    groups: List[str] = field(default_factory=list)
    divisor: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RegisterEntry":
        return cls(
            table=data.get("table", ""),
            address=int(data["address"]),
            end_address=int(data.get("end_address", data["address"])),
            length=int(data.get("length", 1)),
            name=data.get("name", f"Register {data['address']}"),
            description=data.get("description"),
            category=data.get("category"),
            unit=data.get("unit"),
            data_type=data.get("data_type"),
            attributes=list(data.get("attributes", [])),
            families=list(data.get("families", [])),
            read_write=bool(data.get("read_write", False)),
            source=data.get("source"),
            groups=list(data.get("groups", [])),
            divisor=data.get("divisor"),
        )


@dataclass(slots=True)
class DecodedRegister:
    entry: RegisterEntry
    raw: List[Optional[int]]
    decoded: Dict[str, Any]

    @property
    def address_range(self) -> str:
        start = self.entry.address
        end = self.entry.address + self.entry.length - 1
        return f"{start:04d}" if start == end else f"{start:04d}-{end:04d}"


# ---------------------------------------------------------------------------
# Data type catalogue
# ---------------------------------------------------------------------------


class DataTypeCatalog:
    def __init__(self, data: Mapping[str, Any]):
        self.meta = data.get("meta", {})
        self.types: Dict[str, Dict[str, Any]] = dict(data.get("types", {}))

    @classmethod
    def load(cls, path: Path) -> "DataTypeCatalog":
        with path.open("r", encoding="utf-8") as fh:
            return cls(json.load(fh))

    def decode(
        self,
        type_name: str,
        values: Sequence[int],
        *,
        family: Optional[str] = None,
        entry: Optional[RegisterEntry] = None,
    ) -> Dict[str, Any]:
        info = self.types.get(type_name)
        if not info:
            return {
                "display": str(list(values)),
                "value": list(values),
                "raw_value": _combine_registers(values),
            }

        kind = info.get("kind")
        registers = info.get("registers", len(values))
        registers = max(registers, len(values))
        values = list(values)[:registers]
        if any(v is None for v in values):
            return {"display": "<missing>", "value": None}

        if kind == "ascii":
            text = _decode_ascii(values, strip_nulls=info.get("strip_nulls", True))
            return {"display": text, "value": text}
        if kind == "ascii_segments":
            segments: Dict[str, str] = {}
            offset = 0
            for seg in info.get("segments", []):
                length = int(seg.get("length", 0))
                part = values[offset : offset + length]
                text = _decode_ascii(part, strip_nulls=info.get("strip_nulls", True))
                segments[seg.get("name", f"segment_{offset}")] = text
                offset += length
            display = ", ".join(f"{k}={v}" for k, v in segments.items())
            return {"display": display, "value": segments}
        if kind == "enum":
            raw = _combine_registers(values)
            choices = info.get("choices", {})
            choice = choices.get(str(raw)) or {}
            label = choice.get("label", str(raw))
            if note := choice.get("note"):
                label = f"{label} ({note})"
            return {"display": label, "value": raw, "label": choice.get("label", label)}
        if kind == "integer":
            signed = bool(info.get("signed", False))
            raw = _combine_registers(values, signed=signed)
            return {"display": str(raw), "value": raw}
        if kind == "scaled":
            signed = bool(info.get("signed", False))
            raw = _combine_registers(values, signed=signed)
            divisor = info.get("divisor", 1) or 1
            value = raw / divisor
            return {"display": f"{value:g}", "value": value, "raw_value": raw}
        if kind == "bitfield":
            raw = _combine_registers(values)
            flags: Dict[str, bool] = {}
            set_bits: List[str] = []
            for bit in info.get("bits", []):
                idx = int(bit.get("index", 0))
                name = bit.get("name", f"bit_{idx}")
                enabled = bool(raw & (1 << idx))
                flags[name] = enabled
                if enabled:
                    set_bits.append(name)
            return {
                "display": ", ".join(set_bits) if set_bits else "none",
                "value": raw,
                "flags": flags,
                "set": set_bits,
            }
        if kind == "callable":
            callable_path = info.get("callable")
            func = self._resolve_callable(callable_path)
            if func is None:
                return {"display": str(list(values)), "value": list(values)}
            arg: Any = values if len(values) > 1 else values[0]
            result = func(arg)
            return {"display": str(result), "value": result}
        if kind == "callable_per_family":
            mapping = info.get("callable", {})
            path = None
            if family and family in mapping:
                path = mapping[family]
            elif mapping:
                path = next(iter(mapping.values()))
            func = self._resolve_callable(path)
            arg = values if len(values) > 1 else values[0]
            result = func(arg) if func else arg
            return {"display": str(result), "value": result}

        raw = _combine_registers(values)
        return {"display": str(raw), "value": raw}

    def default_raw(self, entry: RegisterEntry, *, family: str) -> List[int]:
        type_name = entry.data_type
        if type_name and type_name in self.types:
            info = self.types[type_name]
            if type_name == "binary_flag":
                return [1]
            if type_name == "baud_rate_select":
                return [1]  # 38400 bit/s
            if type_name == "serial_ascii_5":
                serial = DEFAULT_ASCII_SERIAL.get(family, "SN00000000")
                return _encode_ascii(serial, entry.length)
            if type_name == "firmware_blocks":
                segments = info.get("segments", [])
                defaults = DEFAULT_FIRMWARE_SEGMENTS.get(family, {})
                values: List[int] = []
                for seg in segments:
                    length = int(seg.get("length", 0))
                    text = defaults.get(seg.get("name", ""), seg.get("name", "").upper())
                    values.extend(_encode_ascii(text, length))
                return values
            if type_name == "model_code":
                if family == "tl3":
                    return [0x2345, 0x6789]
                return [0x1234, 0x5678]
            if type_name == "device_type_code":
                mapping = {
                    "tlx": 0x0200,
                    "storage": 0x0C00,
                    "tl3": 0x0800,
                    "offgrid": 0x0D00,
                }
                return [mapping.get(family, 0x0200)]
            if type_name == "mppt_phase_tuple":
                mapping = {
                    "tlx": 0x0201,
                    "storage": 0x0201,
                    "tl3": 0x0203,
                    "offgrid": 0x0101,
                }
                return [mapping.get(family, 0x0201)]
            if type_name == "lcd_language":
                return [1]  # English
            if type_name == "safety_function_flags":
                return [0b00001101]
            if type_name == "ascii_8":
                return _encode_ascii(MANUFACTURER_STRING, entry.length)
            if type_name == "u16":
                return [42]
            if type_name == "u16_div10":
                return [self._encode_scaled_default(entry, divisor=10)]
            if type_name == "u16_div100":
                return [self._encode_scaled_default(entry, divisor=100)]
            if type_name == "u16_div1000":
                return [self._encode_scaled_default(entry, divisor=1000)]
            if type_name == "s32_div10":
                value = int(self._encode_scaled_default(entry, divisor=10, bits=32))
                return _split_registers(value, 2)
            if type_name == "s32_div7200":
                value = int(self._encode_scaled_default(entry, divisor=7200, bits=32))
                return _split_registers(value, 2)

        # Fallback for unspecified types
        if entry.length > 1:
            base = int(self._encode_scaled_default(entry, divisor=entry.divisor or 1, bits=32))
            return _split_registers(base, entry.length)
        return [self._encode_scaled_default(entry, divisor=entry.divisor or 1)]

    def _encode_scaled_default(
        self,
        entry: RegisterEntry,
        *,
        divisor: float,
        bits: int = 16,
    ) -> int:
        value = self._suggest_measurement(entry)
        scaled = int(round(value * divisor))
        limit = 1 << bits
        scaled %= limit
        return scaled

    def _suggest_measurement(self, entry: RegisterEntry) -> float:
        name = entry.name.lower()
        unit = (entry.unit or "").lower()
        if "frequency" in name or unit == "hz":
            return 50.0
        if "temperature" in name or "temp" in name:
            return 27.0
        if "soc" in name or unit == "%":
            return 78.0
        if "battery" in name:
            if unit == "v":
                return 51.4
            if unit == "a":
                return 12.5
        if "pv" in name or "input" in name:
            if unit == "v":
                return 385.0
            if unit == "a":
                return 8.2
            if unit == "w":
                return 2450.0
        if "grid" in name or "output" in name:
            if unit == "v":
                return 230.0
            if unit == "a":
                return 5.4
            if unit == "w":
                return 2400.0
        if "energy" in name and unit in {"kwh", "kvarh"}:
            return 3.75
        if unit == "var":
            return 120.0
        if unit == "v":
            return 230.0
        if unit == "a":
            return 5.0
        if unit == "w":
            return 1800.0
        if unit == "h":
            return 1234.0
        return 42.0

    def _resolve_callable(self, path: Optional[str]):
        if not path:
            return None
        module_name, _, func_name = path.partition(":")
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:  # pragma: no cover - defensive
            LOG.warning("Failed to import %s", module_name)
            return None
        return getattr(module, func_name, None)


# ---------------------------------------------------------------------------
# Register specification loader / decoder
# ---------------------------------------------------------------------------


class RegisterSpec:
    def __init__(self, spec: Mapping[str, Any], data_types: DataTypeCatalog):
        self.meta = spec.get("meta", {})
        self.tables: Dict[str, List[RegisterEntry]] = {}
        for table_name in ("holding", "input"):
            entries = [RegisterEntry.from_dict(item) for item in spec.get(table_name, [])]
            self.tables[table_name] = sorted(entries, key=lambda e: (e.address, e.length))
        self.data_types = data_types

    @classmethod
    def load(cls, spec_path: Path = SPEC_PATH, type_path: Path = DATA_TYPES_PATH) -> "RegisterSpec":
        with spec_path.open("r", encoding="utf-8") as fh:
            spec_data = json.load(fh)
        type_catalog = DataTypeCatalog.load(type_path)
        return cls(spec_data, type_catalog)

    @property
    def families(self) -> Dict[str, str]:
        return dict(self.meta.get("families", {}))

    def entries_for_family(self, family: str, table: str) -> List[RegisterEntry]:
        entries = self.tables.get(table, [])
        filtered = [
            entry
            for entry in entries
            if not entry.families or family in entry.families
        ]
        return filtered

    def decode_entry(
        self,
        entry: RegisterEntry,
        table_values: Mapping[int, int],
        *,
        family: str,
    ) -> DecodedRegister:
        raw: List[Optional[int]] = []
        for offset in range(entry.length):
            raw.append(table_values.get(entry.address + offset))
        if entry.data_type:
            present_values = [v for v in raw if v is not None]
            decoded = (
                self.data_types.decode(entry.data_type, present_values, family=family, entry=entry)
                if len(present_values) == len(raw)
                else {"display": "<missing>", "value": None}
            )
        else:
            decoded = self._decode_generic(entry, raw)
        return DecodedRegister(entry=entry, raw=raw, decoded=decoded)

    def _decode_generic(self, entry: RegisterEntry, raw: Sequence[Optional[int]]) -> Dict[str, Any]:
        if any(v is None for v in raw):
            return {"display": "<missing>", "value": None}
        values = [int(v) for v in raw]
        divisor = entry.divisor or 1
        if entry.length > 1:
            raw_value = _combine_registers(values, signed=True)
            value = raw_value / divisor
            return {"display": f"{value:g}", "value": value, "raw_value": raw_value}
        raw_value = values[0]
        value = raw_value / divisor
        return {"display": f"{value:g}", "value": value, "raw_value": raw_value}

    def decode_tables(
        self,
        tables: Mapping[str, Mapping[int, int]],
        *,
        family: str,
    ) -> Dict[str, List[DecodedRegister]]:
        decoded: Dict[str, List[DecodedRegister]] = {}
        for table_name, table_values in tables.items():
            entries = self.entries_for_family(family, table_name)
            decoded[table_name] = [
                self.decode_entry(entry, table_values, family=family) for entry in entries
            ]
        return decoded

    def generate_default_snapshot(self, family: str) -> Dict[str, Any]:
        tables: Dict[str, Dict[int, int]] = {"holding": {}, "input": {}}
        for table_name, entries in self.tables.items():
            for entry in entries:
                if entry.families and family not in entry.families:
                    continue
                raw_values = self.data_types.default_raw(entry, family=family)
                for idx, value in enumerate(raw_values):
                    tables.setdefault(table_name, {})[entry.address + idx] = int(value) & 0xFFFF
        meta = {
            "mode": "default",
            "family": family,
            "family_label": self.families.get(family, family),
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "spec_generated": self.meta.get("generated"),
            "device_types": [dt.value for dt in FAMILY_DEVICE_TYPES.get(family, [])],
        }
        return {"meta": meta, "tables": self._format_tables(tables)}

    def _format_tables(self, tables: Mapping[str, Mapping[int, int]]) -> Dict[str, Dict[str, int]]:
        formatted: Dict[str, Dict[str, int]] = {}
        for table_name, values in tables.items():
            formatted[table_name] = {str(addr): int(val) for addr, val in sorted(values.items())}
        return formatted


# ---------------------------------------------------------------------------
# Snapshot utilities
# ---------------------------------------------------------------------------


def load_snapshot(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    tables: Dict[str, Dict[int, int]] = {}
    for table_name, values in data.get("tables", {}).items():
        tables[table_name] = {int(addr): int(val) for addr, val in values.items()}
    data["tables"] = tables
    return data


def save_snapshot(path: Path, snapshot: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialisable = {
        "meta": snapshot.get("meta", {}),
        "tables": {
            table: {str(addr): int(val) for addr, val in sorted(values.items())}
            for table, values in snapshot.get("tables", {}).items()
        },
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(serialisable, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Modbus reading helpers
# ---------------------------------------------------------------------------


def _compute_ranges(entries: Sequence[RegisterEntry], max_block: int) -> List[tuple[int, int]]:
    addresses: List[int] = []
    for entry in entries:
        for offset in range(entry.length):
            addresses.append(entry.address + offset)
    if not addresses:
        return []
    addresses.sort()
    ranges: List[tuple[int, int]] = []
    start = addresses[0]
    last = start
    for addr in addresses[1:]:
        if addr == last + 1 and (addr - start + 1) <= max_block:
            last = addr
            continue
        ranges.append((start, last - start + 1))
        start = addr
        last = addr
    ranges.append((start, last - start + 1))
    return ranges


async def _read_table(
    network: GrowattNetwork,
    table: str,
    ranges: Sequence[tuple[int, int]],
    *,
    unit: int,
) -> Dict[int, int]:
    result: Dict[int, int] = {}
    for start, count in ranges:
        if table == "holding":
            registers = await network.read_holding_registers(start, count, slave=unit)
        else:
            registers = await network.read_input_registers(start, count, slave=unit)
        result.update(registers)
    return result


async def read_device_tables(
    spec: RegisterSpec,
    *,
    family: str,
    device_type: DeviceTypes,
    host: str,
    port: int,
    unit: int,
    network_type: str,
    frame: str,
    tables: Sequence[str],
    timeout: int = 3,
    retries: int = 3,
) -> Dict[str, Dict[int, int]]:
    registers_info = get_register_information(device_type)
    max_length = registers_info.max_length
    network = GrowattNetwork(network_type, host, port=port, frame=frame, timeout=timeout, retries=retries)
    await network.connect()
    try:
        decoded: Dict[str, Dict[int, int]] = {}
        for table in tables:
            entries = spec.entries_for_family(family, table)
            ranges = _compute_ranges(entries, max_length)
            decoded[table] = await _read_table(network, table, ranges, unit=unit)
        return decoded
    finally:  # pragma: no branch - always execute cleanup
        network.close()


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def _format_raw(raw: Sequence[Optional[int]]) -> str:
    return "[" + ", ".join("--" if value is None else f"0x{value:04X}" for value in raw) + "]"


def print_decoded(decoded: Mapping[str, List[DecodedRegister]]) -> None:
    for table, entries in decoded.items():
        print(f"\n== {table.upper()} REGISTERS ==")
        for item in entries:
            unit = f" {item.entry.unit}" if item.entry.unit else ""
            display = item.decoded.get("display", "--")
            print(f"{item.address_range:>9}  {item.entry.name:<40} {display}{unit}")
            print(f"          raw={_format_raw(item.raw)}")
            if item.entry.description:
                print(f"          {item.entry.description}")
            if item.decoded.get("label") and item.decoded.get("label") != display:
                print(f"          label={item.decoded['label']}")
            if item.decoded.get("flags"):
                flags = ", ".join(
                    f"{name}={'on' if state else 'off'}"
                    for name, state in sorted(item.decoded["flags"].items())
                )
                print(f"          flags={flags}")


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


def _parse_device_type(value: Optional[str], family: Optional[str]) -> DeviceTypes:
    if value:
        try:
            return DeviceTypes(value)
        except ValueError:
            for item in DeviceTypes:
                if item.name.lower() == value.lower():
                    return item
            raise
    if family and family in FAMILY_DEFAULT_DEVICE:
        return FAMILY_DEFAULT_DEVICE[family]
    return DeviceTypes.HYBRID_120_TL_XH


def cmd_list(args, spec: RegisterSpec) -> None:
    print("Known inverter families:")
    for family, label in spec.families.items():
        device_types = ", ".join(dt.value for dt in FAMILY_DEVICE_TYPES.get(family, [])) or "(none mapped)"
        print(f"  {family:<8} {label} -> {device_types}")


def cmd_defaults(args, spec: RegisterSpec) -> None:
    output_dir = Path(args.output_dir or SNAPSHOT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    for family in spec.families:
        snapshot = spec.generate_default_snapshot(family)
        path = output_dir / f"default_{family}.json"
        if path.exists() and not args.overwrite:
            LOG.info("Skipping %s (exists)", path)
            continue
        save_snapshot(path, snapshot)
        print(f"[OK] wrote {path.relative_to(REPO_ROOT)}")


def cmd_show(args, spec: RegisterSpec) -> None:
    family = args.family or (args.device_type and args.device_type.split("_")[0]) or "tlx"
    if family not in spec.families:
        raise SystemExit(f"Unknown family '{family}'. Use the 'list' command to inspect options.")
    device_type = _parse_device_type(args.device_type, family)

    tables = [table for table in (args.tables or ["holding", "input"]) if table in ("holding", "input")]
    if not tables:
        raise SystemExit("No tables selected (expected 'holding' and/or 'input').")

    snapshot_data: Dict[str, Dict[int, int]]
    metadata: Dict[str, Any] = {}

    if args.snapshot:
        data = load_snapshot(Path(args.snapshot))
        snapshot_data = {table: values for table, values in data.get("tables", {}).items() if table in tables}
        metadata = data.get("meta", {})
        family = args.family or metadata.get("family", family)
    else:
        if not args.host:
            raise SystemExit("Either --host or --snapshot must be provided.")
        loop = asyncio.get_event_loop()
        snapshot_data = loop.run_until_complete(
            read_device_tables(
                spec,
                family=family,
                device_type=device_type,
                host=args.host,
                port=args.port,
                unit=args.unit,
                network_type=args.network,
                frame=args.frame,
                tables=tables,
                timeout=args.timeout,
                retries=args.retries,
            )
        )
        metadata = {
            "mode": "live",
            "family": family,
            "family_label": spec.families.get(family, family),
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "device_type": device_type.value,
            "host": args.host,
            "port": args.port,
            "unit": args.unit,
            "spec_generated": spec.meta.get("generated"),
        }
        if args.out:
            save_snapshot(Path(args.out), {"meta": metadata, "tables": snapshot_data})
            LOG.info("Saved snapshot to %s", args.out)

    decoded = spec.decode_tables(snapshot_data, family=family)
    if args.format == "json":
        serialisable = {
            "meta": metadata,
            "decoded": {
                table: [
                    {
                        "address": item.entry.address,
                        "end_address": item.entry.address + item.entry.length - 1,
                        "name": item.entry.name,
                        "unit": item.entry.unit,
                        "display": item.decoded.get("display"),
                        "value": item.decoded.get("value"),
                        "raw": [value for value in item.raw],
                    }
                    for item in items
                ]
                for table, items in decoded.items()
            },
        }
        print(json.dumps(serialisable, indent=2, sort_keys=True))
    else:
        print_decoded(decoded)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser(spec: RegisterSpec) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-level", default="WARNING", help="Logging level (DEBUG, INFO, WARNING, ERROR)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_list = subparsers.add_parser("list", help="List known inverter families and device types")
    parser_list.set_defaults(func=cmd_list)

    parser_defaults = subparsers.add_parser("defaults", help="Generate synthetic default snapshots")
    parser_defaults.add_argument("--output-dir", help="Directory for generated snapshots (default: testing/snapshots)")
    parser_defaults.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser_defaults.set_defaults(func=cmd_defaults)

    parser_show = subparsers.add_parser("show", help="Display registers from a live inverter or snapshot")
    parser_show.add_argument("--family", choices=sorted(spec.families.keys()))
    parser_show.add_argument(
        "--device-type",
        help="Explicit DeviceTypes enum value (e.g. inverter_120, hybrid_120_TL_XH)",
    )
    parser_show.add_argument("--host", help="Host running the Modbus proxy (TCP/UDP)")
    parser_show.add_argument("--port", type=int, default=502, help="Modbus port (default: 502)")
    parser_show.add_argument("--unit", type=int, default=1, help="Modbus unit/slave ID")
    parser_show.add_argument("--network", default="tcp", help="Network transport: tcp or udp")
    parser_show.add_argument("--frame", default="", help="Framer type ('' for socket, 'rtu' for RTU over TCP/UDP)")
    parser_show.add_argument("--tables", nargs="*", default=["holding", "input"], help="Tables to display")
    parser_show.add_argument("--timeout", type=int, default=3, help="Modbus request timeout")
    parser_show.add_argument("--retries", type=int, default=3, help="Retry count for Modbus requests")
    parser_show.add_argument("--snapshot", help="Existing snapshot JSON to decode")
    parser_show.add_argument("--out", help="Optional path to write the captured snapshot")
    parser_show.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser_show.set_defaults(func=cmd_show)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    spec = RegisterSpec.load(SPEC_PATH, DATA_TYPES_PATH)
    parser = build_parser(spec)
    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.WARNING))

    handler = getattr(args, "func", None)
    if not handler:
        parser.print_help()
        return 1
    handler(args, spec)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())

