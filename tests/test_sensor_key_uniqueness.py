import pytest

from custom_components.growatt_local.sensor_types.inverter import INVERTER_SENSOR_TYPES
from custom_components.growatt_local.sensor_types.storage import STORAGE_SENSOR_TYPES


def _assert_unique(descriptions):
    keys = [desc.key for desc in descriptions]
    assert len(keys) == len(set(keys))


def test_inverter_sensor_keys_unique():
    _assert_unique(INVERTER_SENSOR_TYPES)


def test_storage_sensor_keys_unique():
    _assert_unique(STORAGE_SENSOR_TYPES)


def test_no_overlap_between_inverter_and_storage():
    inverter_keys = {desc.key for desc in INVERTER_SENSOR_TYPES}
    storage_keys = {desc.key for desc in STORAGE_SENSOR_TYPES}
    assert inverter_keys.isdisjoint(storage_keys)
