from typing import Callable, KeysView, List, Optional, Type

import cx_devices as devices_module
import pytest
from cx_const import ActionEvent, TypeActionsMapping
from cx_core import Controller
from cx_core.controller import ReleaseHoldController

from tests.test_utils import get_classes, get_controller


def check_mapping(
    mapping: Optional[TypeActionsMapping],
    all_possible_actions: KeysView[ActionEvent],
    device: Controller,
) -> None:
    device_name = device.__class__.__name__
    if mapping is None:
        return
    if isinstance(device, ReleaseHoldController):
        delay = device.default_delay()
        if delay < 0:
            raise ValueError(
                f"`default_delay` should be a positive integer and the value is `{delay}`. "
                f"Device class: {device_name}"
            )
    for v in mapping.values():
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
                + f"The possible actions are: {list(all_possible_actions)}"
            )


devices_classes = get_classes(
    devices_module.__file__, devices_module.__package__, Controller
)


@pytest.mark.parametrize("device_class", devices_classes)
def test_devices(device_class: Type[Controller]):
    device = device_class()  # type: ignore

    # We first check that all devices are importable from controllerx module
    device_from_controllerx = get_controller("controllerx", device_class.__name__)
    assert (
        device_from_controllerx is not None
    ), f"'{device_class.__name__}' not importable from controllerx.py"

    type_actions_mapping = device.get_type_actions_mapping()
    possible_actions = type_actions_mapping.keys()
    integration_mappings_funcs: List[Callable[[], Optional[TypeActionsMapping]]] = [
        device.get_z2m_actions_mapping,
        device.get_deconz_actions_mapping,
        device.get_zha_actions_mapping,
    ]
    for func in integration_mappings_funcs:
        mappings = func()
        check_mapping(mappings, possible_actions, device)
