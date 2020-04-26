from tests.test_utils import hass_mock, get_instances
import devices as devices_module
from core import Controller


def check_mapping(mapping, all_possible_actions, device_name):
    if mapping is None:
        return
    for k, v in mapping.items():
        if type(v) != str:
            raise ValueError(
                "The value from the mapping should be a string, matching "
                + "one of the actions from the controller. "
                + f"The possible actions are: {all_possible_actions}. "
                + f"Device class: {device_name}"
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
        device_name = device.__class__.__name__
        type_actions_mapping = device.get_type_actions_mapping()
        if type_actions_mapping is None:
            continue
        possible_actions = list(type_actions_mapping.keys())
        mappings = device.get_z2m_actions_mapping()
        check_mapping(mappings, possible_actions, device_name)
        mappings = device.get_deconz_actions_mapping()
        check_mapping(mappings, possible_actions, device_name)
        mappings = device.get_zha_actions_mapping()
        check_mapping(mappings, possible_actions, device_name)
