import cx_devices as devices_module
from cx_core import Controller
from cx_core.controller import ReleaseHoldController
from tests.test_utils import get_instances


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


def test_devices(hass_mock):
    devices = get_instances(
        devices_module.__file__, devices_module.__package__, Controller
    )
    for device in devices:
        type_actions_mapping = device.get_type_actions_mapping()
        if type_actions_mapping is None:
            continue
        possible_actions = list(type_actions_mapping.keys())
        mappings = device.get_z2m_actions_mapping()
        check_mapping(mappings, possible_actions, device)
        mappings = device.get_deconz_actions_mapping()
        check_mapping(mappings, possible_actions, device)
        mappings = device.get_zha_actions_mapping()
        check_mapping(mappings, possible_actions, device)
