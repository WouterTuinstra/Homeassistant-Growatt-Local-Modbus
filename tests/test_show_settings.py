"""Tests for the show_settings CLI utilities."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts import show_settings

SPEC = show_settings.RegisterSpec.load(show_settings.SPEC_PATH, show_settings.DATA_TYPES_PATH)
SNAPSHOT_DIR = Path(show_settings.SNAPSHOT_DIR)


def _load_snapshot(family: str):
    path = SNAPSHOT_DIR / f"default_{family}.json"
    assert path.exists(), f"missing snapshot: {path}"  # sanity guard
    return show_settings.load_snapshot(path)


def _decode_family(family: str):
    snapshot = _load_snapshot(family)
    return SPEC.decode_tables(snapshot["tables"], family=family)


def test_default_snapshots_match_generator():
    """Saved default snapshots should match freshly generated data."""
    for family in SPEC.families:
        saved = _load_snapshot(family)
        generated = SPEC.generate_default_snapshot(family)
        assert saved["meta"]["family"] == family
        # compare tables as int->int maps
        assert saved["tables"] == {
            table: {int(addr): int(val) for addr, val in values.items()}
            for table, values in generated["tables"].items()
        }
        expected_devices = {dt.value for dt in show_settings.FAMILY_DEVICE_TYPES.get(family, [])}
        assert set(saved["meta"].get("device_types", [])) == expected_devices


def _find(decoded, table: str, name: str):
    for entry in decoded[table]:
        if entry.entry.name == name:
            return entry
    raise AssertionError(f"entry {name!r} not found in {table}")


def test_decode_default_tlx_snapshot():
    """Ensure decoding of the TL-X defaults yields meaningful values."""
    decoded = _decode_family("tlx")

    remote = _find(decoded, "holding", "Remote enable")
    assert remote.decoded["value"] == 1
    assert remote.decoded.get("label") == "Enabled"

    safety = _find(decoded, "holding", "Grid safety function enables")
    assert set(safety.decoded.get("set", [])) == {"spi_interface", "lvfrt", "freq_derating"}

    firmware = _find(decoded, "holding", "Firmware revisions")
    assert firmware.decoded["value"]["inverter"] == "INV2.5"
    assert firmware.decoded["value"]["control"] == "COM1.7"

    serial = _find(decoded, "holding", "Serial number")
    assert serial.decoded["value"] == "TLX42A0010"

    device_type = _find(decoded, "holding", "Device type")
    assert device_type.decoded["display"].startswith("2 tracker")

    phases = _find(decoded, "holding", "Trackers / phases")
    assert tuple(phases.decoded["value"]) == (2, 1)

    baud = _find(decoded, "holding", "Modbus baud rate")
    assert baud.decoded["display"] == "38400 bit/s"

    pv_current = _find(decoded, "input", "PV1 buck current")
    assert pytest.approx(pv_current.decoded["value"], rel=1e-3) == 8.2

    battery_voltage = _find(decoded, "input", "Battery voltage")
    assert pytest.approx(battery_voltage.decoded["value"], rel=1e-3) == 51.4

    battery_current = _find(decoded, "input", "Battery current")
    assert pytest.approx(battery_current.decoded["value"], rel=1e-3) == 12.5

    bms_soc = _find(decoded, "input", "BMS SOC")
    assert bms_soc.decoded["value"] == 42

    energy_total = _find(decoded, "input", "Energy To User (Total)")
    assert pytest.approx(energy_total.decoded["value"], rel=1e-3) == 3.8


def test_decode_default_tl3_snapshot():
    """Three-phase defaults should populate identity and power metrics."""

    decoded = _decode_family("tl3")

    serial = _find(decoded, "holding", "Serial number")
    assert serial.decoded["value"] == "TL342C0032"

    device_type = _find(decoded, "holding", "Device type")
    assert "3phase" in device_type.decoded["display"].lower()

    trackers = _find(decoded, "holding", "Trackers / phases")
    assert trackers.decoded["value"] == (2, 3)

    manufacturer = _find(decoded, "holding", "Manufacturer string")
    assert manufacturer.decoded["value"].strip() == "Growatt Power"

    output_voltage = _find(decoded, "input", "Output voltage")
    assert pytest.approx(output_voltage.decoded["value"], rel=1e-3) == 230

    status = _find(decoded, "input", "Status code")
    assert status.decoded["value"] == 42


def test_decode_default_storage_snapshot():
    """Storage defaults should expose serial, device type, and energy stats."""

    decoded = _decode_family("storage")

    serial = _find(decoded, "holding", "Serial number")
    assert serial.decoded["value"].strip() == "STO42B0021"

    device_type = _find(decoded, "holding", "Device type")
    assert "storage" in device_type.decoded["display"].lower()

    trackers = _find(decoded, "holding", "Trackers / phases")
    assert trackers.decoded["value"] == (2, 1)

    discharge = _find(decoded, "input", "Battery discharge power")
    assert pytest.approx(discharge.decoded["value"], rel=1e-3) == 1800

    energy_grid_total = _find(decoded, "input", "Energy To Grid (Total)")
    assert pytest.approx(energy_grid_total.decoded["value"], rel=1e-3) == 3.8


def test_decode_default_offgrid_snapshot():
    """Off-grid defaults should still decode manufacturer and AC metrics."""

    decoded = _decode_family("offgrid")

    manufacturer = _find(decoded, "holding", "Manufacturer string")
    assert manufacturer.decoded["value"].strip() == "Growatt Power"

    status = _find(decoded, "input", "Status code")
    assert status.decoded["value"] == 42

    output_freq = _find(
        decoded,
        "input",
        "Input 6 Voltage, Output 3 Amperage, Output Frequency",
    )
    assert pytest.approx(output_freq.decoded["value"], rel=1e-3) == 50

    output_voltage = _find(
        decoded,
        "input",
        "Output 1 Voltage, Output 3 Voltage",
    )
    assert pytest.approx(output_voltage.decoded["value"], rel=1e-3) == 230


@pytest.mark.parametrize("family", sorted(SPEC.families.keys()))
def test_generate_default_snapshot_roundtrip(family: str):
    """A fresh default snapshot should round-trip through decoding."""
    generated = SPEC.generate_default_snapshot(family)
    tables = {
        table: {int(addr): int(val) for addr, val in values.items()}
        for table, values in generated["tables"].items()
    }
    decoded = SPEC.decode_tables(tables, family=family)
    # ensure at least one register per table produced a value
    for table, entries in decoded.items():
        assert entries, f"no entries decoded for {table} ({family})"
        assert any(entry.decoded.get("value") is not None for entry in entries)

