from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest import mock

import appdaemon.plugins.hass.hassapi as hass
import cx_devices as devices_module
import yaml
from cx_const import ActionEvent, DefaultActionsMapping
from cx_core import (
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
    Z2MLightController,
)
from cx_core.release_hold_controller import ReleaseHoldController
from cx_core.type_controller import Entity, TypeController
from cx_helper import get_instances
from mkdocs_macros.plugin import MacrosPlugin

DocsMapping = Dict[Optional[str], Dict[str, List[ActionEvent]]]

INTEGRATIONS_TITLES = {
    "z2m": "Zigbee2MQTT",
    "deconz": "deCONZ",
    "zha": "ZHA",
    "state": "State",
    "lutron": "Lutron Caseta",
    "homematic": "Homematic",
    "shelly": "Shelly",
    "shellyforhass": "ShellyForHass",
    "tasmota": "Tasmota",
}

INTEGRATIONS_EXAMPLES: List[Dict[str, Any]] = [
    {
        "name": "z2m",
        "title": "Zigbee2MQTT (HA entity)",
        "controller": "sensor.my_controller_action",
    },
    {
        "name": "z2m",
        "title": "Zigbee2MQTT (mqtt)",
        "controller": "my_controller",
        "attrs": {"listen_to": "mqtt"},
    },
    {"name": "deconz", "title": "deCONZ", "controller": "my_controller"},
    {"name": "zha", "title": "ZHA", "controller": "00:11:22:33:44:55:66:77:88"},
    {
        "name": "state",
        "title": "State",
        "controller": "sensor.my_custom_controller",
    },
    {"name": "lutron", "title": "Lutron Caseta", "controller": "87654321"},
    {"name": "homematic", "title": "Homematic", "controller": "my_controller"},
    {"name": "shelly", "title": "Shelly", "controller": "shellybutton-ABC123456"},
    {
        "name": "shellyforhass",
        "title": "ShellyForHass",
        "controller": "binary_sensor.shelly_button_switch",
    },
    {
        "name": "tasmota",
        "title": "Tasmota",
        "controller": "stat/tasmota_device/RESULT",
        "attrs": {"component": "MyComponent"},
    },
]

DEPRECATED_CONTROLLERS = ["W2049"]

with open(Path(__file__).parent / "notes.yaml") as f:
    NOTES: Dict[str, str] = yaml.full_load(f)


@dataclass
class ControllerTypeDocs:
    order: int
    type: str
    entity_arg: str
    domain: Optional[str]
    cls: str
    delay: Optional[int]
    mappings: DocsMapping
    integrations_list: List[str]

    @property
    def entity_name(self) -> str:
        entity_name = "my_entity_id"
        return entity_name if self.domain is None else f"{self.domain}.{entity_name}"

    @property
    def section(self) -> str:
        return "-".join(self.type.lower().split())

    @property
    def integrations_examples(self) -> List[Dict[str, Any]]:
        return [
            integration
            for integration in INTEGRATIONS_EXAMPLES
            if integration["name"] in self.integrations_list
        ]

    @property
    def integrations_titles(self) -> List[str]:
        return [
            INTEGRATIONS_TITLES[integration] for integration in self.integrations_list
        ]

    def _decorate_action_event(self, action_event: ActionEvent) -> str:
        value = str(action_event)
        if value in ("on", "off"):
            value = f'"{value}"'
        return f"`{value}`"

    def make_table(self) -> str:
        table = [
            "|"
            + "|".join(
                [
                    INTEGRATIONS_TITLES[integration]
                    for integration in self.integrations_list
                ]
            )
            + '| <span style="color:#02a6f2">[Predefined actions]'
            f"(/controllerx/advanced/predefined-actions#{self.section})</span> |"
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
                + (
                    predefined_action
                    if predefined_action is not None
                    else "`No action`"
                )
                + "|"
            )
            table.append(row)
        return "\n".join(table)


@dataclass
class ControllerDocs:
    name: str
    controller_type_docs: List[ControllerTypeDocs]
    notes: Optional[str]


def get_device_name(controller: str) -> str:
    return (
        controller.replace("Z2MLightController", "")
        .replace("LightController", "")
        .replace("MediaPlayerController", "")
        .replace("SwitchController", "")
        .replace("CoverController", "")
        .replace("Controller", "")
    )


def get_controller_type(controller: TypeController[Entity]) -> Tuple[str, int]:
    if isinstance(controller, LightController):
        return "Light", 0
    elif isinstance(controller, Z2MLightController):
        return "Zigbee2MQTT Light", 1
    elif isinstance(controller, MediaPlayerController):
        return "Media Player", 2
    elif isinstance(controller, SwitchController):
        return "Switch", 3
    elif isinstance(controller, CoverController):
        return "Cover", 4
    else:
        raise ValueError(
            f"{controller.__class__.__name__} does not belong to any of the 4 type controllers"
        )


def get_controller_docs(controller: TypeController[Entity]) -> ControllerTypeDocs:
    controller_type, order = get_controller_type(controller)
    controller_class = controller.__class__.__name__
    delay: Optional[int] = None
    if isinstance(controller, ReleaseHoldController):
        delay = controller.default_delay()
    mappings: DocsMapping = defaultdict(lambda: defaultdict(list))
    integrations = []

    integration_mappings_funcs: Dict[
        str, Callable[[], Optional[DefaultActionsMapping]]
    ] = {
        "z2m": controller.get_z2m_actions_mapping,
        "deconz": controller.get_deconz_actions_mapping,
        "zha": controller.get_zha_actions_mapping,
        "state": controller.get_state_actions_mapping,
        "lutron": controller.get_lutron_caseta_actions_mapping,
        "homematic": controller.get_homematic_actions_mapping,
        "shelly": controller.get_shelly_actions_mapping,
        "shellyforhass": controller.get_shellyforhass_actions_mapping,
        "tasmota": controller.get_tasmota_actions_mapping,
    }
    for integration, integration_mapping_func in integration_mappings_funcs.items():
        mapping = integration_mapping_func()
        if mapping is not None:
            integrations.append(integration)
            for action_event, predefined_action in mapping.items():
                mappings[predefined_action][integration].append(action_event)

    return ControllerTypeDocs(
        order=order,
        type=controller_type,
        entity_arg=controller.entity_arg,
        domain=controller.domains[0] if len(controller.domains) > 0 else None,
        cls=controller_class,
        delay=delay,
        mappings=mappings,
        integrations_list=integrations,
    )


def get_controllers() -> List[TypeController[Entity]]:
    with mock.patch.object(hass.Hass, "__init__", return_value=None):
        controller_instances = get_instances(
            devices_module.__file__,
            devices_module.__package__,
            TypeController,
        )
    return controller_instances


def get_devices() -> Dict[str, ControllerDocs]:
    devices = defaultdict(list)
    for controller in get_controllers():
        device_name = get_device_name(controller.__class__.__name__)
        if device_name in DEPRECATED_CONTROLLERS:
            continue
        controller_docs = get_controller_docs(controller)
        devices[device_name].append(controller_docs)

    devices_docs: Dict[str, ControllerDocs] = {}
    for device_name, docs in devices.items():
        # Sort the controller types,
        # so they appear in the same order in the documentaiton
        docs = sorted(docs, key=lambda c: c.order)
        devices_docs[device_name] = ControllerDocs(
            name=device_name, controller_type_docs=docs, notes=NOTES.get(device_name)
        )

    return devices_docs


def define_env(env: MacrosPlugin) -> None:
    @env.macro  # type: ignore[misc]
    def devices() -> Dict[str, ControllerDocs]:
        devices = get_devices()
        return dict(sorted(devices.items(), key=lambda device: device[0]))
