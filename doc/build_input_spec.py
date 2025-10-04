#!/usr/bin/env python3
"""Rebuild the input register portion of growatt_registers_spec.json.

The canonical data lives in `HA_local_registers.json` and the
home-grown metadata below.  The goal is to provide clean descriptions,
units, and data types for the TL-X/TL-XH telemetry ranges.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Callable, Iterable

DOC_DIR = Path(__file__).resolve().parent
SPEC_PATH = DOC_DIR / "growatt_registers_spec.json"
MAPPING_PATH = DOC_DIR / "HA_local_registers.json"
DATA_TYPES_PATH = DOC_DIR / "growatt_register_data_types.json"

@dataclass(frozen=True)
class RegisterMeta:
    register: int
    register_end: int
    attributes: tuple[str, ...]
    name: str
    description: str
    unit: str | None
    data_type: str
    families: tuple[str, ...]
    access: str = "R"
    note: str | None = None


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def tracker_description(index: int, field: str) -> tuple[str, str, str | None]:
    label = f"PV{index}"
    if field == "voltage":
        return (
            f"{label} DC voltage",
            f"Instantaneous {label} string voltage measured at the inverter input.",
            "V",
        )
    if field == "amperage":
        return (
            f"{label} DC current",
            f"Instantaneous {label} string current flowing into the inverter.",
            "A",
        )
    if field == "power":
        return (
            f"{label} DC power",
            f"Real-time DC power from {label} computed from voltage and current readings.",
            "W",
        )
    if field == "energy_today":
        return (
            f"{label} energy today",
            f"Energy harvested by {label} today. Values use 0.1 kWh resolution.",
            "kWh",
        )
    if field == "energy_total":
        return (
            f"{label} energy total",
            f"Lifetime energy harvested by {label}. Values use 0.1 kWh resolution.",
            "kWh",
        )
    raise KeyError(field)


PHASE_NAMES = {
    1: "phase L1",
    2: "phase L2",
    3: "phase L3",
}


def phase_description(index: int, field: str) -> tuple[str, str, str | None]:
    phase = PHASE_NAMES.get(index, f"phase {index}")
    if field == "voltage":
        return (
            f"AC {phase} voltage",
            f"AC output voltage for {phase}.",
            "V",
        )
    if field == "amperage":
        return (
            f"AC {phase} current",
            f"AC output current for {phase}.",
            "A",
        )
    if field == "power":
        return (
            f"AC {phase} power",
            f"Active power exported on {phase}.",
            "W",
        )
    raise KeyError(field)


def energy_flow_description(flow: str) -> tuple[str, str, str | None]:
    if flow == "power_to_user":
        return (
            "Load supply power",
            "Real-time active power delivered to on-site (self-consumption) loads.",
            "W",
        )
    if flow == "power_to_grid":
        return (
            "Grid export power",
            "Active power exported to the utility grid.",
            "W",
        )
    if flow == "power_user_load":
        return (
            "Home load power",
            "Aggregate instantaneous demand from on-site loads.",
            "W",
        )
    if flow == "energy_to_user_today":
        return (
            "Load energy today",
            "Energy delivered to on-site loads today (0.1 kWh resolution).",
            "kWh",
        )
    if flow == "energy_to_user_total":
        return (
            "Load energy total",
            "Lifetime energy delivered to on-site loads (0.1 kWh resolution).",
            "kWh",
        )
    if flow == "energy_to_grid_today":
        return (
            "Export energy today",
            "Energy exported to the grid today (0.1 kWh resolution).",
            "kWh",
        )
    if flow == "energy_to_grid_total":
        return (
            "Export energy total",
            "Lifetime energy exported to the grid (0.1 kWh resolution).",
            "kWh",
        )
    raise KeyError(flow)


ATTRIBUTE_OVERRIDES: dict[str, tuple[str, str, str | None]] = {
    "status_code": (
        "Inverter status",
        "Operating state reported by the inverter controller (0=waiting, 1=normal, 3=fault, 5=PV charge, 6=AC charge, 7=combined charge, 8=combined charge bypass, 9=PV charge bypass, 10=AC charge bypass, 11=bypass, 12=PV charge + discharge).",
        None,
    ),
    "input_power": (
        "PV input power",
        "Total PV input power summed across all strings (0.1 W resolution).",
        "W",
    ),
    "output_power": (
        "AC output power",
        "Active AC output power delivered by the inverter (0.1 W resolution).",
        "W",
    ),
    "grid_frequency": (
        "Grid frequency",
        "Measured grid frequency with 0.01 Hz resolution.",
        "Hz",
    ),
    "operation_hours": (
        "Run time",
        "Total cumulative run time of the inverter. Raw values are seconds scaled by 1/7200 (0.0001389 hours).",
        "h",
    ),
    "input_energy_total": (
        "PV energy total",
        "Total PV energy generated across all strings (0.1 kWh resolution).",
        "kWh",
    ),
    "output_energy_today": (
        "Output energy today",
        "Energy exported to the AC output today (0.1 kWh resolution).",
        "kWh",
    ),
    "output_energy_total": (
        "Output energy total",
        "Lifetime AC output energy (0.1 kWh resolution).",
        "kWh",
    ),
    "output_reactive_power": (
        "Output reactive power",
        "Instantaneous reactive power on the AC output (positive = inductive, negative = capacitive).",
        "var",
    ),
    "output_reactive_energy_total": (
        "Reactive energy total",
        "Lifetime accumulated reactive energy (0.1 kvarh resolution).",
        "kvarh",
    ),
    "derating_mode": (
        "Derating mode",
        "Active derating reason reported by the inverter controller.",
        None,
    ),
    "inverter_temperature": (
        "Inverter temperature",
        "Main inverter heatsink temperature (0.1 °C resolution).",
        "°C",
    ),
    "ipm_temperature": (
        "IPM temperature",
        "IPM (power module) temperature (0.1 °C resolution).",
        "°C",
    ),
    "boost_temperature": (
        "Boost temperature",
        "Boost inductor temperature (0.1 °C resolution).",
        "°C",
    ),
    "comm_board_temperature": (
        "Communication board temperature",
        "Temperature reported by the communication/control board (0.1 °C resolution).",
        "°C",
    ),
    "p_bus_voltage": (
        "P-bus voltage",
        "Positive DC bus voltage (0.1 V resolution).",
        "V",
    ),
    "n_bus_voltage": (
        "N-bus voltage",
        "Negative DC bus voltage (0.1 V resolution).",
        "V",
    ),
    "real_output_power_percent": (
        "Output power percentage",
        "Instantaneous AC output as a percentage of the inverter's rated power.",
        "%",
    ),
    "fault_code": (
        "Fault code",
        "Current inverter fault code (see protocol documentation).",
        None,
    ),
    "warning_code": (
        "Warning code",
        "Current inverter warning code (vendor-defined bitmask).",
        None,
    ),
    "present_fft_a": (
        "Present FFT value (channel A)",
        "Latest Fast Fourier Transform diagnostic value for channel A.",
        None,
    ),
    "inv_start_delay": (
        "Inverter start delay",
        "Seconds remaining before restart once grid conditions recover.",
        "s",
    ),
    "discharge_energy_today": (
        "Battery discharge today",
        "Energy discharged from the battery into the AC system today (0.1 kWh resolution).",
        "kWh",
    ),
    "discharge_energy_total": (
        "Battery discharge total",
        "Total energy discharged from the battery (0.1 kWh resolution).",
        "kWh",
    ),
    "charge_energy_today": (
        "Battery charge today",
        "Energy charged into the battery today (0.1 kWh resolution).",
        "kWh",
    ),
    "charge_energy_total": (
        "Battery charge total",
        "Total energy charged into the battery (0.1 kWh resolution).",
        "kWh",
    ),
    "bdc_new_flag": (
        "BDC presence flag",
        "Indicates whether a battery DC converter (BDC) has been detected.",
        None,
    ),
    "battery_voltage": (
        "Battery voltage",
        "Pack voltage reported via the inverter-side measurements (0.01 V resolution).",
        "V",
    ),
    "battery_current": (
        "Battery current",
        "Current flowing between battery and inverter (positive = discharge) with 0.1 A resolution.",
        "A",
    ),
    "soc": (
        "Battery SOC",
        "Battery state of charge reported by the inverter.",
        "%",
    ),
    "vbus1_voltage": (
        "VBUS1 voltage",
        "BDC high-side bus voltage (0.1 V resolution).",
        "V",
    ),
    "vbus2_voltage": (
        "VBUS2 voltage",
        "BDC low-side bus voltage (0.1 V resolution).",
        "V",
    ),
    "buck_boost_current": (
        "Buck/boost current",
        "Current through the BDC buck/boost stage (0.1 A resolution).",
        "A",
    ),
    "llc_current": (
        "LLC stage current",
        "Current through the LLC resonant stage (0.1 A resolution).",
        "A",
    ),
    "battery_temperature_a": (
        "Battery temperature A",
        "Battery temperature sensor A (0.1 °C resolution).",
        "°C",
    ),
    "battery_temperature_b": (
        "Battery temperature B",
        "Battery temperature sensor B (0.1 °C resolution).",
        "°C",
    ),
    "discharge_power": (
        "Battery discharge power",
        "Real-time discharge power flowing from the battery (0.1 W resolution).",
        "W",
    ),
    "charge_power": (
        "Battery charge power",
        "Real-time charge power flowing into the battery (0.1 W resolution).",
        "W",
    ),
    "bms_max_volt_cell_no": (
        "BMS max cell index",
        "Cell index reporting the highest voltage in the battery stack (1-based).",
        None,
    ),
    "bms_min_volt_cell_no": (
        "BMS min cell index",
        "Cell index reporting the lowest voltage in the battery stack (1-based).",
        None,
    ),
    "bms_avg_temp_a": (
        "BMS average temperature A",
        "Average temperature reported by sensor group A (0.1 °C resolution).",
        "°C",
    ),
    "bms_max_cell_temp_a": (
        "BMS max cell temperature A",
        "Maximum cell temperature within sensor group A (0.1 °C resolution).",
        "°C",
    ),
    "bms_avg_temp_b": (
        "BMS average temperature B",
        "Average temperature reported by sensor group B (0.1 °C resolution).",
        "°C",
    ),
    "bms_max_cell_temp_b": (
        "BMS max cell temperature B",
        "Maximum cell temperature within sensor group B (0.1 °C resolution).",
        "°C",
    ),
    "bms_avg_temp_c": (
        "BMS average temperature C",
        "Average temperature reported by sensor group C (0.1 °C resolution).",
        "°C",
    ),
    "bms_max_soc": (
        "BMS max SOC",
        "Highest state of charge observed across battery modules.",
        "%",
    ),
    "bms_min_soc": (
        "BMS min SOC",
        "Lowest state of charge observed across battery modules.",
        "%",
    ),
    "parallel_battery_num": (
        "Parallel battery count",
        "Number of battery modules detected in parallel.",
        None,
    ),
    "bms_derate_reason": (
        "BMS derate reason",
        "Reason code reported by the BMS for power derating.",
        None,
    ),
    "bms_gauge_fcc_ah": (
        "BMS full charge capacity",
        "Full charge capacity (FCC) reported by the battery fuel gauge (Ah).",
        "Ah",
    ),
    "bms_gauge_rm_ah": (
        "BMS remaining capacity",
        "Remaining capacity (RM) reported by the battery fuel gauge (Ah).",
        "Ah",
    ),
    "bms_protect1": (
        "BMS protect flags 1",
        "Protection bitmask word 1 from the battery management system.",
        None,
    ),
    "bms_warn1": (
        "BMS warning flags 1",
        "Warning bitmask word 1 from the battery management system.",
        None,
    ),
    "bms_fault1": (
        "BMS fault flags 1",
        "Fault bitmask word 1 from the battery management system.",
        None,
    ),
    "bms_fault2": (
        "BMS fault flags 2",
        "Fault bitmask word 2 from the battery management system.",
        None,
    ),
    "bat_iso_status": (
        "Battery insulation status",
        "Isolation detection status reported by the BMS (0 = not detected, 1 = detected).",
        None,
    ),
    "batt_request_flags": (
        "Battery request flags",
        "Bitmask of requests from the BMS to the inverter (charge/discharge permissions).",
        None,
    ),
    "bms_status": (
        "BMS status",
        "Overall battery management system status code.",
        None,
    ),
    "bms_protect2": (
        "BMS protect flags 2",
        "Protection bitmask word 2 from the battery management system.",
        None,
    ),
    "bms_warn2": (
        "BMS warning flags 2",
        "Warning bitmask word 2 from the battery management system.",
        None,
    ),
    "bms_soc": (
        "BMS SOC",
        "State of charge reported directly by the BMS.",
        "%",
    ),
    "bms_battery_voltage": (
        "BMS battery voltage",
        "Pack voltage reported by the BMS (0.01 V resolution).",
        "V",
    ),
    "bms_battery_current": (
        "BMS battery current",
        "Current reported by the BMS with 0.01 A resolution (positive = discharge).",
        "A",
    ),
    "bms_cell_max_temp": (
        "BMS max cell temperature",
        "Maximum cell temperature observed across the battery pack (0.1 °C resolution).",
        "°C",
    ),
    "bms_max_charge_current": (
        "BMS max charge current",
        "Maximum charge current allowed by the BMS (0.01 A resolution).",
        "A",
    ),
    "bms_max_discharge_current": (
        "BMS max discharge current",
        "Maximum discharge current allowed by the BMS (0.01 A resolution).",
        "A",
    ),
    "bms_cycle_count": (
        "BMS cycle count",
        "Total charge/discharge cycles counted by the BMS.",
        None,
    ),
    "bms_soh": (
        "BMS state of health",
        "Battery state of health reported by the BMS.",
        "%",
    ),
    "bms_charge_volt_limit": (
        "BMS charge voltage limit",
        "Maximum pack voltage permitted during charge (0.01 V resolution).",
        "V",
    ),
    "bms_discharge_volt_limit": (
        "BMS discharge voltage limit",
        "Minimum pack voltage permitted during discharge (0.01 V resolution).",
        "V",
    ),
    "bms_warn3": (
        "BMS warning flags 3",
        "Warning bitmask word 3 from the battery management system.",
        None,
    ),
    "bms_protect3": (
        "BMS protect flags 3",
        "Protection bitmask word 3 from the battery management system.",
        None,
    ),
    "bms_cell_volt_max": (
        "BMS max cell voltage",
        "Highest individual cell voltage (0.001 V resolution).",
        "V",
    ),
    "bms_cell_volt_min": (
        "BMS min cell voltage",
        "Lowest individual cell voltage (0.001 V resolution).",
        "V",
    ),
}


def resolve_attribute(attr: str, register: int) -> tuple[str, str, str | None]:
    if attr in ATTRIBUTE_OVERRIDES:
        return ATTRIBUTE_OVERRIDES[attr]

    if match := re.match(r"input_(\d+)_(voltage|amperage|power|energy_today|energy_total)", attr):
        idx = int(match.group(1))
        field = match.group(2)
        return tracker_description(idx, field)

    if match := re.match(r"output_(\d+)_(voltage|amperage|power)", attr):
        idx = int(match.group(1))
        field = match.group(2)
        return phase_description(idx, field)

    if attr in {
        "power_to_user",
        "power_to_grid",
        "power_user_load",
        "energy_to_user_today",
        "energy_to_user_total",
        "energy_to_grid_today",
        "energy_to_grid_total",
    }:
        return energy_flow_description(attr)

    raise KeyError(f"Missing metadata for attribute {attr} (register {register})")


SIGNED_ATTRIBUTES = {
    "battery_current",
    "bms_battery_current",
    "discharge_power",
    "charge_power",
    "output_reactive_power",
}

ENERGY_ATTRIBUTES = {
    "input_energy_total",
    "output_energy_today",
    "output_energy_total",
    "input_1_energy_today",
    "input_1_energy_total",
    "input_2_energy_today",
    "input_2_energy_total",
    "input_3_energy_today",
    "input_3_energy_total",
    "input_4_energy_today",
    "input_4_energy_total",
    "input_5_energy_today",
    "input_5_energy_total",
    "input_6_energy_today",
    "input_6_energy_total",
    "input_7_energy_today",
    "input_7_energy_total",
    "input_8_energy_today",
    "input_8_energy_total",
    "output_reactive_energy_total",
    "energy_to_user_today",
    "energy_to_user_total",
    "energy_to_grid_today",
    "energy_to_grid_total",
    "discharge_energy_today",
    "discharge_energy_total",
    "charge_energy_today",
    "charge_energy_total",
}


def is_voltage_attr(attr: str) -> bool:
    if attr.endswith("_volt_cell_no"):
        return False
    return (
        "voltage" in attr
        or attr.endswith("_volt")
        or "_volt_" in attr
        or attr.endswith("volt_limit")
        or attr.endswith("volt_max")
        or attr.endswith("volt_min")
    )


def determine_data_type(attr: str, length: int, scale: int, value_type: str) -> str:
    if attr == "status_code":
        return "inverter_status_code"
    if attr in {"fault_code", "warning_code"}:
        return "u16_status_word"
    if attr == "derating_mode":
        return "u16_raw_code"
    if attr == "bdc_new_flag":
        return "u16_flag"
    if attr == "operation_hours":
        return "u32_runtime_hours"
    if attr == "output_reactive_power":
        return "s32_reactive_power_decivar"
    if attr == "output_reactive_energy_total":
        return "u32_energy_kvarh_decitenth"
    if attr.endswith("_ah"):
        return "u16_ampere_hour"
    if length == 2 and attr in ENERGY_ATTRIBUTES:
        return "u32_energy_kwh_decitenth"
    if length == 2:
        if attr in SIGNED_ATTRIBUTES:
            return "s32_power_w_decawatt"
        return "u32_power_w_decawatt"
    if scale == 1000:
        if is_voltage_attr(attr):
            return "u16_voltage_millivolt"
        return "u16_raw"
    if scale == 100:
        if "current" in attr:
            if attr in SIGNED_ATTRIBUTES:
                return "s16_current_centiamp"
            return "u16_current_centiamp"
        if is_voltage_attr(attr):
            return "u16_voltage_centivolt"
        if attr == "grid_frequency":
            return "u16_frequency_centihz"
        return "u16_scaled_100"
    if scale == 7200:
        return "u32_runtime_hours"
    percent_attributes = {
        "soc",
        "bms_soc",
        "bms_max_soc",
        "bms_min_soc",
        "real_output_power_percent",
        "bms_soh",
    }
    if scale == 10:
        if attr in percent_attributes:
            return "u16_percent"
        if is_voltage_attr(attr):
            return "u16_voltage_decivolt"
        if "current" in attr or "amperage" in attr:
            if attr in SIGNED_ATTRIBUTES:
                return "s16_current_deciamp"
            return "u16_current_deciamp"
        if "temperature" in attr or "temp" in attr:
            return "s16_temperature_decic"
        if attr.endswith("power") or "power_" in attr:
            return "u16_power_decawatt"
    if scale == 1:
        if attr in percent_attributes:
            return "u16_percent"
        if attr.endswith("_ah"):
            return "u16_ampere_hour"
    if value_type == "int":
        return "u16_raw"
    return "u16_raw"


SECTION_RULES: list[tuple[str, Callable[[int], bool]]] = [
    ("Common input telemetry (0–124)", lambda reg: 0 <= reg <= 124),
    ("Extended common input telemetry (125–299)", lambda reg: 125 <= reg < 3000),
    ("TL-X/TL-XH PV/AC telemetry (3000–3124)", lambda reg: 3000 <= reg <= 3124),
    ("TL-X/TL-XH battery telemetry (3125–3199)", lambda reg: 3125 <= reg <= 3199),
    ("TL-X/TL-XH BMS diagnostics (3200–3231)", lambda reg: 3200 <= reg <= 3231),
]


def assign_section(register: int) -> str:
    for title, predicate in SECTION_RULES:
        if predicate(register):
            return title
    raise ValueError(f"No section for register {register}")


def build_register_meta() -> list[RegisterMeta]:
    mapping = load_json(MAPPING_PATH)
    register_families: dict[int, set[str]] = {}
    for family, groups in mapping.items():
        for group_name, group_entries in groups.items():
            if not group_name.startswith("input"):
                continue
            for item in group_entries:
                register_families.setdefault(item["register"], set()).add(family)

    entries: list[RegisterMeta] = []
    # combine common and TL-XH groups (deduplicate by register + attribute)
    seen: set[tuple[int, str]] = set()
    combined = mapping["tlx"]["input_common"] + mapping["tlx"]["input_tl_xh"]
    for item in combined:
        attr = item["name"]
        register = item["register"]
        key = (register, attr)
        if key in seen:
            continue
        seen.add(key)
        length = item.get("length", 1)
        register_end = register + length - 1
        value_type = item.get("value_type", "int")
        scale = item.get("scale")
        if scale is None:
            scale = 1 if value_type == "int" else 10
        name, description, unit = resolve_attribute(attr, register)
        data_type = determine_data_type(attr, length, scale, value_type)
        note = None
        if attr == "operation_hours":
            note = "Raw counter counts seconds; divide by 7200 to obtain hours."
        if attr == "bms_battery_current":
            note = "Positive values indicate discharge from the battery; negative values indicate charging."
        families = tuple(sorted(register_families.get(register, {"tlx"})))
        entries.append(
            RegisterMeta(
                register=register,
                register_end=register_end,
                attributes=(attr,),
                name=name,
                description=description,
                unit=unit,
                data_type=data_type,
                families=families,
                note=note,
            )
        )
    entries.sort(key=lambda meta: meta.register)
    return entries


TYPE_DEFINITIONS: dict[str, dict] = {
    "inverter_status_code": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "waiting"},
            "1": {"label": "normal"},
            "3": {"label": "fault"},
            "5": {"label": "pv_charge"},
            "6": {"label": "ac_charge"},
            "7": {"label": "combined_charge"},
            "8": {"label": "combined_charge_bypass"},
            "9": {"label": "pv_charge_bypass"},
            "10": {"label": "ac_charge_bypass"},
            "11": {"label": "bypass"},
            "12": {"label": "pv_charge_discharge"},
        },
        "notes": "Enum derived from Growatt protocol inverter status codes.",
    },
    "u16_voltage_decivolt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "V",
    },
    "u16_voltage_centivolt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 100,
        "unit": "V",
    },
    "u16_voltage_millivolt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 1000,
        "unit": "V",
    },
    "u16_current_deciamp": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "A",
    },
    "s16_current_deciamp": {
        "kind": "scaled_signed",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "A",
    },
    "u16_current_centiamp": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 100,
        "unit": "A",
    },
    "s16_current_centiamp": {
        "kind": "scaled_signed",
        "registers": 1,
        "bits": 16,
        "scale": 100,
        "unit": "A",
    },
    "s16_temperature_decic": {
        "kind": "scaled_signed",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "°C",
    },
    "u16_percent": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 1,
        "unit": "%",
    },
    "u16_ampere_hour": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 1,
        "unit": "Ah",
    },
    "u16_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {"0": {"label": "no"}, "1": {"label": "yes"}},
    },
    "u16_raw": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
    },
    "u16_raw_code": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
        "notes": "Vendor-specific state code.",
    },
    "u16_status_word": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
        "notes": "Vendor-specific fault/warning bitmask.",
    },
    "u32_power_w_decawatt": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "W",
        "notes": "Unsigned 32-bit value stored as high/low words with 0.1 W resolution.",
    },
    "s32_power_w_decawatt": {
        "kind": "scaled_signed",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "W",
        "notes": "Signed 32-bit value stored as high/low words with 0.1 W resolution.",
    },
    "s32_reactive_power_decivar": {
        "kind": "scaled_signed",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "var",
        "notes": "Signed 32-bit reactive power measurement with 0.1 var resolution.",
    },
    "u16_power_decawatt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "W",
    },
    "u32_energy_kwh_decitenth": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "kWh",
        "notes": "Cumulative energy counter with 0.1 kWh resolution (high word first).",
    },
    "u32_energy_kvarh_decitenth": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "kvarh",
        "notes": "Cumulative reactive energy counter with 0.1 kvarh resolution (high word first).",
    },
    "u32_runtime_hours": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 7200,
        "unit": "h",
        "notes": "Divide raw seconds by 7200 to obtain hours.",
    },
    "u16_scaled_100": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 100,
    },
    "u16_frequency_centihz": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 100,
        "unit": "Hz",
        "notes": "Divide by 100 to obtain the grid frequency in hertz.",
    },
}


SECTION_TITLE_ORDER = [title for title, _ in SECTION_RULES]


def rebuild_spec_input(entries: Iterable[RegisterMeta]) -> list[dict]:
    result: list[dict] = []
    current_section: str | None = None
    for meta in entries:
        section = assign_section(meta.register)
        if section != current_section:
            result.append({"type": "section", "title": section})
            current_section = section
        entry: dict = {
            "type": "entry",
            "section": section,
            "register": meta.register,
            "register_start": meta.register,
            "register_end": meta.register_end,
            "name": meta.name,
            "description": meta.description,
            "access": meta.access,
            "unit": meta.unit,
            "data_type": meta.data_type,
        }
        if meta.note:
            entry["note"] = meta.note
        if meta.attributes:
            entry["attributes"] = list(meta.attributes)
        result.append(entry)
    return result


def update_spec_file(entries: list[RegisterMeta]):
    spec = load_json(SPEC_PATH)
    spec["input"] = rebuild_spec_input(entries)
    with SPEC_PATH.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def update_data_types(entries: list[RegisterMeta]):
    data = load_json(DATA_TYPES_PATH)
    types = data.setdefault("types", {})
    for type_name, definition in TYPE_DEFINITIONS.items():
        existing = types.get(type_name)
        if existing:
            continue
        types[type_name] = definition

    register_types: list[dict] = data.setdefault("register_types", [])
    handled_registers = {meta.register for meta in entries}
    # Remove existing entries for the registers we cover in the input table.
    preserved_families: dict[int, set[str]] = {}
    filtered: list[dict] = []
    for item in register_types:
        if (
            item.get("table") == "input"
            and item.get("register") in handled_registers
            and "tlx" in item.get("families", [])
        ):
            preserved_families[item["register"]] = set(item.get("families", []))
            continue
        filtered.append(item)
    register_types = filtered
    for meta in entries:
        families = set(preserved_families.get(meta.register, set())) | set(meta.families)
        item = {
            "table": "input",
            "register": meta.register,
            "register_end": meta.register_end,
            "type": meta.data_type,
            "attributes": list(meta.attributes),
            "families": sorted(families),
        }
        register_types.append(item)
    # Keep register types sorted for determinism.
    register_types.sort(key=lambda item: (item["table"], item["register"]))
    data["register_types"] = register_types
    with DATA_TYPES_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main():
    entries = build_register_meta()
    update_spec_file(entries)
    update_data_types(entries)
    print(f"Updated input register spec for {len(entries)} entries.")


if __name__ == "__main__":
    main()
