"""Regression tests for the HA-5 live defects."""

from types import SimpleNamespace

from custom_components.growatt_local.API.device_type.base import (
    ATTR_AC_CHARGE_ENABLED,
    ATTR_BMS_BATTERY_CURRENT,
    ATTR_INVERTER_ENABLED,
    GrowattDeviceInfo,
    GrowattDeviceRegisters,
)
from custom_components.growatt_local.API.growatt import select_device_info
from custom_components.growatt_local.API.utils import process_registers
from custom_components.growatt_local.const import CONF_INVERTER_POWER_CONTROL
from custom_components.growatt_local.switch import get_switch_descriptions
import pytest


def make_config_entry(
    *, data_enabled: bool, option_enabled: bool | None = None
) -> SimpleNamespace:
    """Build the small config-entry surface used by the switch selector."""

    options = {}
    if option_enabled is not None:
        options[CONF_INVERTER_POWER_CONTROL] = option_enabled
    return SimpleNamespace(
        data={CONF_INVERTER_POWER_CONTROL: data_enabled}, options=options
    )


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [(0xFEB6, -3.30), (330, 3.30), (0, 0.0)],
)
def test_signed_bms_current_processing(raw_value: int, expected: float) -> None:
    """BMS current register 3217 is a signed int16 scaled by 100."""

    register = GrowattDeviceRegisters(
        name=ATTR_BMS_BATTERY_CURRENT,
        register=3217,
        value_type=float,
        scale=100,
        signed=True,
    )

    assert process_registers({3217: register}, {3217: raw_value}) == {
        ATTR_BMS_BATTERY_CURRENT: expected
    }


def test_tlxh_power_control_switch_is_gated() -> None:
    """AC Charge remains available while power control follows its option."""

    supported = {ATTR_AC_CHARGE_ENABLED, ATTR_INVERTER_ENABLED}

    disabled = get_switch_descriptions(
        make_config_entry(data_enabled=False), supported
    )
    assert [description.key for description in disabled] == [ATTR_AC_CHARGE_ENABLED]

    enabled = get_switch_descriptions(
        make_config_entry(data_enabled=True), supported
    )
    assert [description.key for description in enabled] == [
        ATTR_AC_CHARGE_ENABLED,
        ATTR_INVERTER_ENABLED,
    ]

    overridden = get_switch_descriptions(
        make_config_entry(data_enabled=True, option_enabled=False), supported
    )
    assert [description.key for description in overridden] == [ATTR_AC_CHARGE_ENABLED]


def make_device_info(device_type_code: int) -> GrowattDeviceInfo:
    """Build device information for protocol-family selection tests."""

    return GrowattDeviceInfo(
        serial_number="serial",
        model="model",
        firmware="firmware",
        mppt_trackers=2,
        grid_phases=1,
        modbus_version=3.05,
        device_type="device",
        device_type_code=device_type_code,
    )


def test_device_info_selection_uses_device_type_family() -> None:
    """MIN TL-XH code 5100 selects the v1.20 register layout."""

    v120 = make_device_info(5100)
    v315 = make_device_info(5100)

    assert select_device_info(v120, v315) is v120
    assert v120.device_family.value == "hybrid_120_TL_XH"


def test_device_info_selection_preserves_offgrid_family() -> None:
    """The known SPF device family still selects the v3.15 layout."""

    v120 = make_device_info(0xD00)
    v315 = make_device_info(0xD00)

    assert select_device_info(v120, v315) is v315
    assert v315.device_family.value == "offgrid_SPF"


def test_device_info_selection_does_not_guess_unknown_family() -> None:
    """Unknown device codes require explicit family selection."""

    assert select_device_info(make_device_info(0x1200), make_device_info(0x1200)) is None
