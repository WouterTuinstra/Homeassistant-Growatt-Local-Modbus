#!/usr/bin/env python3
"""Generate growatt_register_data_types.json from the integration mapping.

The resulting JSON file contains two sections:

``types``
    Canonical reusable type descriptions. Each entry documents how raw
    Modbus register values should be interpreted (scale, encoding, etc.).

``register_types``
    Mapping of specific register ranges to the type identifiers. Entries are
    keyed by Modbus table (``holding``/``input``) so that overlapping register
    numbers in different tables can be described independently.

Some configuration registers are not consumed directly by the integration but
are still documented for completeness. Their definitions live in
``MANUAL_REGISTER_TYPES`` below.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

DOC_DIR = Path(__file__).resolve().parent
MAPPING_PATH = DOC_DIR / "growatt_local_registers.json"
OUTPUT_PATH = DOC_DIR / "growatt_register_data_types.json"


MANUAL_TYPES: dict[str, dict[str, Any]] = {
    "inverter_enable_flags": {
        "kind": "bitfield",
        "registers": 1,
        "bits": 16,
        "flags": [
            {
                "bit": 0,
                "name": "inverter_run_request",
                "description": "1 keeps the inverter enabled; 0 issues a remote stop command.",
            },
            {
                "bit": 1,
                "name": "bdc_enable_request",
                "description": "Enable the BDC (battery DC converter) for battery-ready mode.",
            },
        ],
        "notes": "Write the combined bit mask (0–3). Bits 2–15 are reserved and should remain 0.",
    },
    "safety_function_flags": {
        "kind": "bitfield",
        "registers": 1,
        "bits": 16,
        "flags": [
            {"bit": 0, "name": "spi_enable", "description": "Enable the System Protection Interface (SPI)."},
            {"bit": 1, "name": "auto_test_start", "description": "Allow automatic anti-islanding test routines."},
            {"bit": 2, "name": "lvfrt_enable", "description": "Enable low-voltage fault ride through."},
            {"bit": 3, "name": "frequency_derating_enable", "description": "Apply frequency-based active power derating."},
            {"bit": 4, "name": "soft_start_enable", "description": "Enable soft-start behaviour."},
            {"bit": 5, "name": "drms_enable", "description": "Enable DRMS/DRAS demand response mode."},
            {"bit": 6, "name": "volt_var_enable", "description": "Enable Volt-Var (Power-Volt) function."},
            {"bit": 7, "name": "hvfrt_enable", "description": "Enable high-voltage fault ride through."},
            {"bit": 8, "name": "rocof_enable", "description": "Enable rate-of-change-of-frequency protection."},
            {"bit": 9, "name": "freq_derating_recover", "description": "Allow automatic recovery after frequency derating."},
            {"bit": 10, "name": "split_phase_enable", "description": "Enable split-phase operation."},
        ],
        "notes": "Bits 0–3 relate to CEI 0-21 compliance; bits 4–6 to AS/NZS (SAA) requirements. Bits 11–15 are reserved.",
    },
    "boolean_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "disabled"},
            "1": {"label": "enabled"},
        },
    },
    "pf_command_persistence": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "volatile", "description": "Restore defaults after a restart."},
            "1": {"label": "persist", "description": "Keep power-factor related commands in NVRAM."},
        },
    },
    "active_power_percent_limit": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 1,
        "unit": "%",
        "range": [0, 100],
        "special_values": {
            "255": {"label": "no_limit", "description": "255 disables the active power cap."}
        },
    },
    "reactive_power_percent_limit": {
        "kind": "scaled_signed",
        "registers": 1,
        "bits": 16,
        "scale": 1,
        "unit": "%",
        "range": [-100, 100],
        "special_values": {
            "255": {"label": "no_limit", "description": "255 disables the reactive power cap."}
        },
    },
    "power_factor_x10000": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10000,
        "unit": "pf",
        "notes": "Divide by 10 000 to obtain the power factor. Values <1 lead (capacitive), >1 lag (inductive).",
    },
    "u32_decivolt_ampere": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "VA",
        "notes": "Unsigned 32-bit value stored in 0.1 VA increments (high word first).",
    },
    "u16_decivolt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "V",
    },
    "u16_seconds": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 1,
        "unit": "s",
    },
    "ramp_percent_per_second": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "%/s",
        "range": [1, 1000],
    },
    "export_limit_failure_percent": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "%",
        "range": [0, 100],
        "read_write": True,
        "notes": "Fallback output percentage used when the export-limit controller is unavailable.",
    },
    "dry_contact_enable_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "disabled"},
            "1": {"label": "enabled"},
        },
        "read_write": True,
    },
    "ac_charge_enable_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "disabled"},
            "1": {"label": "enabled"},
        },
        "read_write": True,
        "notes": "0 disables AC-side charging; 1 allows grid charging when configured.",
    },
    "storage_work_mode": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "default"},
            "1": {"label": "system_retrofit"},
            "2": {"label": "multi_parallel"},
        },
        "read_write": True,
        "notes": "Selects the hybrid operating mode for retrofits or parallel stacks.",
    },
    "external_comm_offgrid_enable_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "disabled"},
            "1": {"label": "enabled"},
        },
        "read_write": True,
    },
    "grid_topology_code": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "single_phase"},
            "1": {"label": "three_phase"},
            "2": {"label": "split_phase"},
        },
        "read_write": True,
    },
    "current_dec_ampere": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "A",
        "read_write": True,
    },
    "voltage_centivolt": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 100,
        "unit": "V",
        "read_write": True,
    },
    "temperature_decicelsius_offset": {
        "kind": "scaled",
        "registers": 1,
        "bits": 16,
        "scale": 10,
        "unit": "°C",
        "read_write": True,
        "notes": "Values 0–200 map to 0–20 °C; subtract 1000 from values ≥1000 to obtain negative limits.",
    },
    "grid_first_schedule_control": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
        "read_write": True,
        "notes": "Bits 0–7 start minute, 8–12 start hour, 13–14 priority, bit 15 enable.",
    },
    "grid_first_schedule_end": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
        "read_write": True,
        "notes": "Bits 0–7 end minute, 8–12 end hour; other bits reserved.",
    },
    "u32_deciwatt": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "W",
    },
    "u32_decikwh": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 10,
        "unit": "kWh",
    },
    "u32_work_hours_half_second": {
        "kind": "scaled",
        "registers": 2,
        "bits": 32,
        "scale": 7200,
        "unit": "h",
        "notes": "Value / 7200 gives operating hours with 0.5 s resolution.",
    },
    "bdc_reset_command": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "invalid"},
            "1": {"label": "reset_settings"},
            "2": {"label": "reset_calibration"},
            "3": {"label": "clear_history"},
        },
        "read_write": True,
    },
    "ascii_4": {
        "kind": "ascii",
        "registers": 2,
        "characters": 4,
        "read_write": False,
    },
    "ascii_2": {
        "kind": "ascii",
        "registers": 1,
        "characters": 2,
        "read_write": False,
    },
    "bms_comm_interface_type": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "rs485"},
            "1": {"label": "can"},
        },
    },
    "bdc_protocol_version_word": {
        "kind": "raw",
        "registers": 1,
        "bits": 16,
        "read_write": False,
        "notes": "High byte = major version, low byte = minor version.",
    },
    "bdc_onoff_state_flag": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "off"},
            "1": {"label": "on"},
        },
    },
    "ascii_12": {
        "kind": "ascii",
        "registers": 6,
        "characters": 12,
        "read_write": False,
    },
    "ascii_10": {
        "kind": "ascii",
        "registers": 5,
        "characters": 10,
        "read_write": False,
    },
    "lcd_language_code": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
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
    "baud_rate_selection": {
        "kind": "enum",
        "registers": 1,
        "bits": 16,
        "values": {
            "0": {"label": "9600 bps"},
            "1": {"label": "38400 bps"},
        },
        "notes": "Applies to the RS-485 Modbus RTU interface.",
    },
}


MANUAL_REGISTER_TYPES: tuple[dict[str, Any], ...] = (
    {
        "table": "holding",
        "register": 0,
        "register_end": 0,
        "type": "inverter_enable_flags",
        "attributes": ["inverter_enabled"],
        "families": ["tlx", "tl3", "storage"],
        "description": "Remote enable bits for the inverter (bit 0) and BDC (bit 1).",
    },
    {
        "table": "holding",
        "register": 1,
        "register_end": 1,
        "type": "safety_function_flags",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
        "description": "Safety function enable mask (SPI, LVFRT, DRMS, Volt/Var, etc.).",
    },
    {
        "table": "holding",
        "register": 2,
        "register_end": 2,
        "type": "pf_command_persistence",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 3,
        "register_end": 3,
        "type": "active_power_percent_limit",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 4,
        "register_end": 4,
        "type": "reactive_power_percent_limit",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 5,
        "register_end": 5,
        "type": "power_factor_x10000",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 6,
        "register_end": 7,
        "type": "u32_decivolt_ampere",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 8,
        "register_end": 8,
        "type": "u16_decivolt",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 9,
        "register_end": 14,
        "type": "ascii_12",
        "attributes": ["firmware"],
        "families": ["tlx", "tl3", "storage"],
        "description": "Concatenated DSP/control firmware identification string (ASCII).",
    },
    {
        "table": "holding",
        "register": 15,
        "register_end": 15,
        "type": "lcd_language_code",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 16,
        "register_end": 16,
        "type": "boolean_flag",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
        "description": "Indicates whether a country/regional profile has been selected.",
    },
    {
        "table": "holding",
        "register": 17,
        "register_end": 17,
        "type": "u16_decivolt",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 18,
        "register_end": 18,
        "type": "u16_seconds",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 19,
        "register_end": 19,
        "type": "u16_seconds",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 20,
        "register_end": 20,
        "type": "ramp_percent_per_second",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 21,
        "register_end": 21,
        "type": "ramp_percent_per_second",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 22,
        "register_end": 22,
        "type": "baud_rate_selection",
        "attributes": [],
        "families": ["tlx", "tl3", "storage"],
    },
    {
        "table": "holding",
        "register": 23,
        "register_end": 27,
        "type": "ascii_10",
        "attributes": ["serial number"],
        "families": ["tlx", "tl3", "storage"],
        "description": "Inverter serial number stored as a 10-character ASCII string.",
    },
    {
        "table": "holding",
        "register": 3000,
        "register_end": 3000,
        "type": "export_limit_failure_percent",
        "families": ["storage"],
        "description": "Fallback output percentage when export limiting fails.",
    },
    {
        "table": "holding",
        "register": 3016,
        "register_end": 3016,
        "type": "dry_contact_enable_flag",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3018,
        "register_end": 3018,
        "type": "storage_work_mode",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3021,
        "register_end": 3021,
        "type": "external_comm_offgrid_enable_flag",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3023,
        "register_end": 3023,
        "type": "grid_topology_code",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3024,
        "register_end": 3024,
        "type": "current_dec_ampere",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3028,
        "register_end": 3030,
        "type": "voltage_centivolt",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3031,
        "register_end": 3034,
        "type": "temperature_decicelsius_offset",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3038,
        "register_end": 3038,
        "type": "grid_first_schedule_control",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3039,
        "register_end": 3039,
        "type": "grid_first_schedule_end",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3041,
        "register_end": 3042,
        "type": "u32_deciwatt",
        "attributes": ["power_to_user"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3043,
        "register_end": 3044,
        "type": "u32_deciwatt",
        "attributes": ["power_to_grid"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3045,
        "register_end": 3046,
        "type": "u32_deciwatt",
        "attributes": ["power_user_load"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3047,
        "register_end": 3048,
        "type": "u32_work_hours_half_second",
        "attributes": ["operation_hours"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3049,
        "register_end": 3049,
        "type": "ac_charge_enable_flag",
        "attributes": ["ac_charge_enabled"],
        "families": ["storage"],
        "description": "Remote enable for AC-side charging on TL-XH hybrids.",
    },
    {
        "table": "holding",
        "register": 3051,
        "register_end": 3052,
        "type": "u32_decikwh",
        "attributes": ["output_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3053,
        "register_end": 3054,
        "type": "u32_decikwh",
        "attributes": ["input_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3055,
        "register_end": 3056,
        "type": "u32_decikwh",
        "attributes": ["input_1_energy_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3057,
        "register_end": 3058,
        "type": "u32_decikwh",
        "attributes": ["input_1_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3059,
        "register_end": 3060,
        "type": "u32_decikwh",
        "attributes": ["input_2_energy_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3061,
        "register_end": 3062,
        "type": "u32_decikwh",
        "attributes": ["input_2_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3063,
        "register_end": 3064,
        "type": "u32_decikwh",
        "attributes": ["input_3_energy_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3065,
        "register_end": 3066,
        "type": "u32_decikwh",
        "attributes": ["input_3_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3067,
        "register_end": 3068,
        "type": "u32_decikwh",
        "attributes": ["energy_to_user_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3069,
        "register_end": 3070,
        "type": "u32_decikwh",
        "attributes": ["energy_to_user_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3071,
        "register_end": 3072,
        "type": "u32_decikwh",
        "attributes": ["energy_to_grid_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3073,
        "register_end": 3074,
        "type": "u32_decikwh",
        "attributes": ["energy_to_grid_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3075,
        "register_end": 3076,
        "type": "u32_decikwh",
        "attributes": ["load_energy_today"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3077,
        "register_end": 3078,
        "type": "u32_decikwh",
        "attributes": ["load_energy_total"],
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3079,
        "register_end": 3082,
        "type": "u32_decikwh",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3083,
        "register_end": 3084,
        "type": "u32_decikwh",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3087,
        "register_end": 3094,
        "type": "ascii_16",
        "families": ["storage"],
        "description": "Battery rack serial number string from the BMS.",
    },
    {
        "table": "holding",
        "register": 3095,
        "register_end": 3095,
        "type": "bdc_reset_command",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3096,
        "register_end": 3097,
        "type": "ascii_4",
        "families": ["storage"],
        "description": "BDC monitoring firmware code.",
    },
    {
        "table": "holding",
        "register": 3099,
        "register_end": 3100,
        "type": "ascii_4",
        "families": ["storage"],
        "description": "DSP firmware code identifier.",
    },
    {
        "table": "holding",
        "register": 3101,
        "register_end": 3101,
        "type": "ascii_2",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3103,
        "register_end": 3106,
        "type": "ascii_2",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3107,
        "register_end": 3107,
        "type": "bms_comm_interface_type",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3108,
        "register_end": 3111,
        "type": "ascii_2",
        "families": ["storage"],
        "description": "BDC module identification tokens.",
    },
    {
        "table": "holding",
        "register": 3113,
        "register_end": 3113,
        "type": "bdc_protocol_version_word",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3118,
        "register_end": 3118,
        "type": "bdc_onoff_state_flag",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3121,
        "register_end": 3122,
        "type": "u32_deciwatt",
        "families": ["storage"],
    },
    {
        "table": "holding",
        "register": 3123,
        "register_end": 3124,
        "type": "u32_decikwh",
        "families": ["storage"],
    },
)


def load_mapping() -> dict:
    with MAPPING_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def table_from_group(group_name: str) -> str:
    return "holding" if "holding" in group_name else "input"


def type_id(length: int, scale: float | int, read_write: bool, value_type: str) -> str:
    if value_type == "str":
        return f"ascii_{length * 2}"
    if value_type == "custom_function":
        return f"raw_u{length * 16}"
    bits = length * 16
    if scale == 1 or scale == 1.0:
        scale_part = "scale1"
    elif isinstance(scale, float) and scale != int(scale):
        scale_part = f"scale{scale}".replace(".", "p")
    else:
        scale_part = f"scale{int(scale)}"
    suffix = "_rw" if read_write else ""
    return f"u{bits}_{scale_part}{suffix}"


def ensure_type(
    types: dict[str, dict[str, Any]],
    tid: str,
    length: int,
    scale: float | int,
    read_write: bool,
    value_type: str,
) -> None:
    if tid in types:
        return
    if value_type == "str":
        types[tid] = {
            "kind": "ascii",
            "registers": length,
            "characters": length * 2,
            "read_write": bool(read_write),
        }
    elif value_type == "custom_function":
        types[tid] = {
            "kind": "raw",
            "registers": length,
            "bits": length * 16,
            "read_write": bool(read_write),
        }
    else:
        types[tid] = {
            "kind": "scaled",
            "registers": length,
            "bits": length * 16,
            "scale": scale,
            "read_write": bool(read_write),
        }


def merge_manual_registers(
    register_types: list[dict[str, Any]],
    manual_entries: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    base_map = {
        (entry["table"], entry["register"]): entry
        for entry in register_types
    }

    for manual in manual_entries:
        key = (manual["table"], manual["register"])
        base_map.pop(key, None)
        base_map[key] = manual

    merged = list(base_map.values())
    merged.sort(key=lambda item: (item["table"], item["register"]))
    return merged


def main() -> None:
    mapping = load_mapping()
    types: dict[str, dict[str, Any]] = {}
    reg_map: dict[tuple[str, int], dict[str, Any]] = {}

    for family, groups in mapping.items():
        for group_name, entries in groups.items():
            table = table_from_group(group_name)
            for entry in entries:
                length = entry.get("length", 1)
                scale = entry.get("scale", 10)
                read_write = entry.get("read_write", False)
                value_type = entry.get("value_type", "int")
                register = entry["register"]
                register_end = register + length - 1
                tid = type_id(length, scale, read_write, value_type)

                ensure_type(types, tid, length, scale, read_write, value_type)

                info = reg_map.setdefault(
                    (table, register),
                    {
                        "table": table,
                        "register": register,
                        "register_end": register_end,
                        "type": tid,
                        "attributes": set(),
                        "families": set(),
                    },
                )

                if info["type"] != tid:
                    # retain the first discovered type and surface conflicts later if needed
                    info.setdefault("type_conflicts", set()).add(tid)
                info["register_end"] = max(info["register_end"], register_end)
                info["attributes"].add(entry["name"])
                info["families"].add(family)

    # serialise sets
    register_types = []
    for (_, _), info in sorted(reg_map.items(), key=lambda item: (item[0][0], item[0][1])):
        entry = {
            "table": info["table"],
            "register": info["register"],
            "register_end": info["register_end"],
            "type": info["type"],
            "attributes": sorted(info["attributes"]),
            "families": sorted(info["families"]),
        }
        if conflicts := info.get("type_conflicts"):
            entry["type_conflicts"] = sorted(conflicts)
        register_types.append(entry)

    # merge manual definitions and extend the type catalogue with manual types
    for name, definition in MANUAL_TYPES.items():
        # Allow overriding automatically generated placeholders with manual
        # descriptions by replacing the entry entirely.
        types[name] = definition

    register_types = merge_manual_registers(register_types, MANUAL_REGISTER_TYPES)

    data = {
        "types": dict(sorted(types.items())),
        "register_types": register_types,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"Wrote {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
