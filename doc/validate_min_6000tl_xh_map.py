#!/usr/bin/env python3
"""Validate the focused MIN 6000TL-XH map and its captured read-only evidence."""

from __future__ import annotations

import json
from pathlib import Path


DOC_DIR = Path(__file__).resolve().parent
MAP_PATH = DOC_DIR / "min_6000tl_xh_register_map.json"
VALIDATION_PATH = DOC_DIR / "min_6000tl_xh_live_validation.json"


def u32(words: list[int], offset: int) -> int:
    return (words[offset] << 16) | words[offset + 1]


def assert_close(actual: float, expected: float, label: str) -> None:
    assert abs(actual - expected) < 0.001, f"{label}: {actual} != {expected}"


def validate_pv_sample(sample: dict[str, object]) -> None:
    raw = sample["fc04_3000_count11_registers"]
    decoded = sample["decoded"]
    assert isinstance(raw, list)
    assert isinstance(decoded, dict)
    total = u32(raw, 1) / 10
    pv1 = u32(raw, 5) / 10
    pv2 = u32(raw, 9) / 10
    assert_close(decoded["pv_power_w"], total, "total PV power")
    assert_close(decoded["pv1_power_w"], pv1, "PV1 power")
    assert_close(decoded["pv2_power_w"], pv2, "PV2 power")
    assert_close(decoded["pv1_power_w"] + decoded["pv2_power_w"], total, "PV sum")


def validate_ac_sample(sample: dict[str, object]) -> None:
    raw = sample.get("fc04_3021_count13_registers")
    if raw is None:
        return
    decoded = sample["decoded"]
    assert isinstance(raw, list)
    assert isinstance(decoded, dict)
    assert_close(decoded["ac_output_power_w"], u32(raw, 2) / 10, "AC output power")


def validate_flow_sample(sample: dict[str, object]) -> None:
    decoded = sample["decoded"]
    assert isinstance(decoded, dict)
    if "fc04_3043_count4_registers" in sample:
        raw = sample["fc04_3043_count4_registers"]
        assert isinstance(raw, list)
        assert_close(decoded["load_w"], u32(raw, 2) / 10, "load power")
    if "fc04_3041_count6_registers" in sample:
        raw = sample["fc04_3041_count6_registers"]
        assert isinstance(raw, list)
        assert_close(decoded["load_w"], u32(raw, 4) / 10, "load power")


def validate_battery_sample(sample: dict[str, object]) -> None:
    decoded = sample["decoded"]
    assert isinstance(decoded, dict)
    if "fc04_3164_count18_registers" in sample:
        raw = sample["fc04_3164_count18_registers"]
        assert isinstance(raw, list)
        voltage = raw[5] / 100
        soc = raw[7]
        discharge = u32(raw, 14) / 10
        charge = u32(raw, 16) / 10
    else:
        raw = sample["fc04_3169_count13_registers"]
        assert isinstance(raw, list)
        voltage = raw[0] / 100
        soc = raw[2]
        discharge = u32(raw, 9) / 10
        charge = u32(raw, 11) / 10
    assert_close(decoded["battery_voltage_v"], voltage, "battery voltage")
    assert decoded["battery_soc_pct"] == soc
    assert_close(decoded["battery_discharge_w"], discharge, "battery discharge power")
    assert_close(decoded["battery_charge_w"], charge, "battery charge power")


def main() -> None:
    register_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))

    holding = {entry["register"]: entry for entry in register_map["holding"]}
    input_registers = {entry["register"]: entry for entry in register_map["input"]}

    assert {0, 23, 43, 44, 88, 3036, 3037, 3047, 3048, 3049, 3081, 3082} <= holding.keys()
    assert {3000, 3001, 3041, 3043, 3045, 3047, 3049, 3081, 3169, 3171, 3178, 3180, 3215} <= input_registers.keys()
    assert holding[3081]["name"] == "UPS/EPS frequency selection"
    assert input_registers[3081]["name"] == "PV4 energy total"
    assert validation["meta"]["access"] == "FC03/FC04 only; no writes issued"
    assert validation["identity"]["fc03_43_count2_registers"] == [5100, 513]
    assert validation["holding_ems"]["fc03_3081_count2_registers"] == [0, 0]
    for sample in validation["telemetry_samples"]:
        if "fc04_3000_count11_registers" in sample:
            validate_pv_sample(sample)
        if "fc04_3021_count13_registers" in sample:
            validate_ac_sample(sample)
        if "fc04_3043_count4_registers" in sample or "fc04_3041_count6_registers" in sample:
            validate_flow_sample(sample)
        if "fc04_3164_count18_registers" in sample or "fc04_3169_count13_registers" in sample:
            validate_battery_sample(sample)

    print(
        f"validated {len(holding)} holding and {len(input_registers)} input entries; "
        "table-specific 3081 conflict is resolved"
    )


if __name__ == "__main__":
    main()
