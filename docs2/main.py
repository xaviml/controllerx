from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import appdaemon.plugins.hass.hassapi as hass
import cx_devices as devices_module
import mock
from cx_const import ActionEvent, DefaultActionsMapping
from cx_core import (
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
)
from cx_core.release_hold_controller import ReleaseHoldController
from cx_core.type_controller import TypeController
from cx_helper import get_classes

INTEGRATIONS: Dict[str, Dict[str, str]] = {
    "z2m": {"title": "Zigbee2MQTT", "controller": "sensor.my_controller_action"},
    "deconz": {"title": "deCONZ", "controller": "my_controller"},
    "zha": {"title": "ZHA", "controller": "00:11:22:33:44:55:66:77:88"},
    "state": {"title": "State", "controller": "sensor.my_custom_controller"},
    "lutron": {"title": "Lutron Caseta", "controller": "87654321"},
}


@dataclass
class ControllerDocs:
    order: int
    type: str
    cls: str
    delay: Optional[int]
    mappings: Dict[str, Dict[str, List[ActionEvent]]]
    integrations_list: List[str]

    @property
    def domain(self) -> str:
        return "_".join(self.type.lower().split())

    @property
    def integrations(self) -> Dict[str, Dict[str, str]]:
        return {
            integration: INTEGRATIONS[integration]
            for integration in self.integrations_list
        }

    def _decorate_action_event(self, action_event: ActionEvent) -> str:
        value = str(action_event)
        if value in ("on", "off"):
            value = f'"{value}"'
        return f"`{value}`"

    def make_table(self) -> str:

        table = [
            "|"
            + "|".join(
                [integration["title"] for integration in self.integrations.values()]
            )
            + "| Predefined actions |"
        ]
        table.append(
            "-----".join(["|" for _ in range(len(self.integrations_list) + 2)])
        )
        for predefined_action, integrations in self.mappings.items():
            integration_values = {key: "" for key in self.integrations_list}
            integration_values.update(
                {
                    key: ", ".join(
                        [self._decorate_action_event(value) for value in values]
                    )
                    for key, values in integrations.items()
                }
            )
            row = (
                "|"
                + "|".join(integration_values.values())
                + "|"
                + predefined_action
                + "|"
            )
            table.append(row)
        return "\n".join(table)


def get_device_name(controller: str) -> str:
    return (
        controller.replace("Light", "")
        .replace("MediaPlayer", "")
        .replace("Switch", "")
        .replace("Cover", "")
        .replace("Controller", "")
    )


def get_controller_type(controller: TypeController) -> Tuple[str, int]:
    if isinstance(controller, LightController):
        return "Light", 0
    elif isinstance(controller, MediaPlayerController):
        return "Media Player", 1
    elif isinstance(controller, SwitchController):
        return "Switch", 2
    elif isinstance(controller, CoverController):
        return "Cover", 3
    else:
        raise ValueError(
            f"{controller.__class__.__name__} does not belong to any of the 4 type controllers"
        )


def get_controller_docs(controller: TypeController) -> ControllerDocs:
    controller_type, order = get_controller_type(controller)
    controller_class = controller.__class__.__name__
    delay: Optional[int] = None
    if isinstance(controller, ReleaseHoldController):
        delay = controller.default_delay()
    mappings: Dict[str, Dict[str, List[ActionEvent]]] = defaultdict(
        lambda: defaultdict(list)
    )
    integrations = []

    integration_mappings_funcs: Dict[
        str, Callable[[], Optional[DefaultActionsMapping]]
    ] = {
        "z2m": controller.get_z2m_actions_mapping,
        "deconz": controller.get_deconz_actions_mapping,
        "zha": controller.get_zha_actions_mapping,
        "state": controller.get_state_actions_mapping,
        "lutron": controller.get_lutron_caseta_actions_mapping,
    }
    for integration, integration_mapping_func in integration_mappings_funcs.items():
        mapping = integration_mapping_func()
        if mapping is not None:
            integrations.append(integration)
            for action_event, predefined_action in mapping.items():
                mappings[predefined_action][integration].append(action_event)

    return ControllerDocs(
        order=order,
        type=controller_type,
        cls=controller_class,
        delay=delay,
        mappings=mappings,
        integrations_list=integrations,
    )


def get_controllers() -> List[TypeController]:
    with mock.patch.object(hass.Hass, "__init__", return_value=None):
        controller_instances = get_classes(
            devices_module.__file__,
            devices_module.__package__,
            TypeController,
            instantiate=True,
        )
    return controller_instances


def get_devices() -> Dict[str, List[ControllerDocs]]:
    devices = defaultdict(list)
    for controller in get_controllers():
        device_name = get_device_name(controller.__class__.__name__)
        controller_docs = get_controller_docs(controller)
        devices[device_name].append(controller_docs)
    # Sort the controller types,
    # so they appear in the same order in the documentaiton
    for device in devices:
        devices[device].sort(key=lambda c: c.order)
    return devices


def define_env(env):
    @env.macro
    def devices():
        devices = get_devices()
        return dict(sorted(devices.items(), key=lambda device: device[0]))
