import pytest
from tests.test_utils import get_classes, get_controller

import cx_devices as devices_module
from cx_core import Controller
from cx_core.controller import ReleaseHoldController


def check_mapping(mapping, all_possible_actions, device):
    device_name = device.__class__.__name__
    if mapping is None:
        return
    if issubclass(device.__class__, ReleaseHoldController):
        delay = device.default_delay()
        if delay < 0:
            raise ValueError(
                f"`default_delay` should be a positive integer and the value is `{delay}`. "
                f"Device class: {device_name}"
            )
    for k, v in mapping.items():
        if not isinstance(v, str):
            raise ValueError(
                "The value from the mapping should be a string, matching "
                "one of the actions from the controller. "
                f"The possible actions are: {all_possible_actions}. "
                f"Device class: {device_name}"
            )

        if v not in all_possible_actions:
            raise ValueError(
                f"{device_name}: `{v}` not found in the list of possible action from the controller. "
                + f"The possible actions are: {all_possible_actions}"
            )


devices_classes = get_classes(
    devices_module.__file__, devices_module.__package__, Controller
)


@pytest.mark.parametrize("device_class", devices_classes)
def test_devices(hass_mock, device_class):
    device = device_class()

    # We first check that all devices are importable from controllerx module
    device_from_controllerx = get_controller("controllerx", device_class.__name__)
    assert device_from_controllerx is not None

    type_actions_mapping = device.get_type_actions_mapping()
    if type_actions_mapping is None:
        return
    possible_actions = list(type_actions_mapping.keys())
    integration_mappings_funcs = [
        device.get_z2m_actions_mapping,
        device.get_deconz_actions_mapping,
        device.get_zha_actions_mapping,
    ]
    for func in integration_mappings_funcs:
        mappings = func()
        check_mapping(mappings, possible_actions, device)
