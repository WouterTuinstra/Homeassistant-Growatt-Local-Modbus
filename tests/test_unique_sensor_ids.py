"""Test that all sensor unique IDs are unique for each supported inverter type."""

import pytest
from custom_components.growatt_local.sensor_types.inverter import INVERTER_SENSOR_TYPES
from custom_components.growatt_local.sensor_types.storage import STORAGE_SENSOR_TYPES
from custom_components.growatt_local.sensor_types.offgrid import OFFGRID_SENSOR_TYPES
from custom_components.growatt_local.sensor import GrowattDeviceEntity


@pytest.mark.parametrize(
    ("device_type", "sensor_types"),
    [
        ("INVERTER", INVERTER_SENSOR_TYPES),
        ("INVERTER_315", INVERTER_SENSOR_TYPES),
        ("INVERTER_120", INVERTER_SENSOR_TYPES),
        ("HYBRID_120", INVERTER_SENSOR_TYPES + STORAGE_SENSOR_TYPES),
        ("HYBRID_120_TL_XH", INVERTER_SENSOR_TYPES + STORAGE_SENSOR_TYPES),
        ("STORAGE_120", STORAGE_SENSOR_TYPES),
        ("OFFGRID_SPF", OFFGRID_SENSOR_TYPES),
    ],
)
def test_unique_sensor_ids(device_type, sensor_types):
    """Ensure all sensor unique_ids are unique for the given inverter type."""
    # Minimal config entry mock
    config_entry = type("ConfigEntry", (), {})()
    config_entry.data = {
        "serial_number": "TESTSERIAL",
        "type": device_type,
        "model": "TestModel",
        "firmware": "1.0",
    }
    config_entry.options = {
        "name": "TestDevice",
        "ac_phases": 1,
        "dc_string": 1,
        "power_scan_enabled": False,
    }

    # Dummy coordinator
    class DummyCoordinator:
        data = {}

    coordinator = DummyCoordinator()
    # Generate all unique_ids
    unique_ids = set()
    for desc in sensor_types:
        entity = GrowattDeviceEntity(coordinator, desc, config_entry)
        uid = entity.unique_id
        assert uid not in unique_ids, (
            f"Duplicate unique_id: {uid} for type {device_type}"
        )
        unique_ids.add(uid)
