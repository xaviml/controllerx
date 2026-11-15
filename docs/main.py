"""
Extracts the supported devices from the ControllerX code base so they can be
documented. Used by `gen_device_pages.py` to generate:

- One Markdown page per device (docs/controllers/<device>.md)
- The supported controllers catalogue (docs/controllers/index.md)
- A machine-readable catalogue (docs/controllers/devices.json) used by the
  configuration builder and meant for tools and AI assistants.
"""

import re
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
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
from cx_version import __version__

DocsMapping = dict[str | None, dict[str, list[ActionEvent]]]


@dataclass(frozen=True)
class Integration:
    name: str
    title: str
    # Documentation page, relative to docs/docs/
    page: str


INTEGRATIONS = {
    integration.name: integration
    for integration in [
        Integration("z2m", "Zigbee2MQTT", "start/integrations/zigbee2mqtt.md"),
        Integration("deconz", "deCONZ", "start/integrations/deconz.md"),
        Integration("zha", "ZHA", "start/integrations/zha.md"),
        Integration("state", "State", "start/integrations/state.md"),
        Integration(
            "lutron_caseta", "Lutron Caseta", "start/integrations/lutron_caseta.md"
        ),
        Integration("homematic", "Homematic", "start/integrations/homematic.md"),
        Integration("shelly", "Shelly", "start/integrations/shelly.md"),
        Integration(
            "shellyforhass", "ShellyForHass", "start/integrations/shellyforhass.md"
        ),
        Integration("tasmota", "Tasmota", "start/integrations/tasmota.md"),
    ]
}

INTEGRATIONS_TITLES = {name: i.title for name, i in INTEGRATIONS.items()}

# Example configurations shown for each device. The `id` is used by the
# configuration builder and the `title` is used as the tab title
# (tabs with the same title are linked across pages).
INTEGRATIONS_EXAMPLES: list[dict[str, Any]] = [
    {
        "id": "z2m-mqtt",
        "name": "z2m",
        "title": "Zigbee2MQTT (MQTT)",
        "controller": "my_controller",
        "controller_help": "Zigbee2MQTT friendly name of the device",
        "attrs": {"listen_to": "mqtt"},
    },
    {
        "id": "z2m-event",
        "name": "z2m",
        "title": "Zigbee2MQTT (event)",
        "controller": "my_controller_action",
        "controller_help": "Event entity ID without the `event.` prefix",
        "attrs": {"listen_to": "event"},
    },
    {
        "id": "deconz",
        "name": "deconz",
        "title": "deCONZ",
        "controller": "my_controller",
        "controller_help": "deCONZ `id` or `unique_id` of the device",
    },
    {
        "id": "zha",
        "name": "zha",
        "title": "ZHA",
        "controller": "00:11:22:33:44:55:66:77:88",
        "controller_help": "IEEE address of the device",
    },
    {
        "id": "state",
        "name": "state",
        "title": "State",
        "controller": "sensor.my_custom_controller",
        "controller_help": "Entity ID whose state changes with each action",
    },
    {
        "id": "lutron_caseta",
        "name": "lutron_caseta",
        "title": "Lutron Caseta",
        "controller": "87654321",
        "controller_help": "`serial` of the device in `lutron_caseta_button_event`",
    },
    {
        "id": "homematic",
        "name": "homematic",
        "title": "Homematic",
        "controller": "my_controller",
        "controller_help": "Homematic device name",
    },
    {
        "id": "shelly",
        "name": "shelly",
        "title": "Shelly",
        "controller": "shellybutton-ABC123456",
        "controller_help": "Shelly device ID",
    },
    {
        "id": "shellyforhass",
        "name": "shellyforhass",
        "title": "ShellyForHass",
        "controller": "binary_sensor.shelly_button_switch",
        "controller_help": "Binary sensor entity ID",
    },
    {
        "id": "tasmota",
        "name": "tasmota",
        "title": "Tasmota",
        "controller": "stat/tasmota_device/RESULT",
        "controller_help": "MQTT topic where Tasmota publishes the events",
        "attrs": {"component": "MyComponent"},
    },
]

# Python module in cx_devices -> manufacturer name
MANUFACTURERS = {
    "adeo": "ADEO",
    "aqara": "Aqara",
    "aurora": "Aurora",
    "homematic": "Homematic",
    "ikea": "IKEA",
    "legrand": "Legrand",
    "linkind": "Linkind",
    "livarno": "Livarno",
    "lutron": "Lutron",
    "muller_licht": "Müller Licht",
    "namron": "Namron",
    "osram": "OSRAM",
    "philips": "Philips",
    "prolight": "Prolight",
    "rgb_genie": "RGB Genie",
    "robb": "ROBB",
    "sengled": "Sengled",
    "shelly": "Shelly",
    "smartkontakten": "Smartkontakten",
    "smartthings": "SmartThings",
    "sonoff": "SONOFF",
    "tasmota": "Tasmota",
    "terncy": "Terncy",
    "trust": "Trust",
    "tuya": "Tuya",
}

DEPRECATED_CONTROLLERS = ["W2049"]

with open(Path(__file__).parent / "notes.yaml") as f:
    NOTES: dict[str, str] = yaml.safe_load(f)


def _yaml_scalar(value: Any) -> str:
    """Render a value as it would be written by hand in apps.yaml."""
    text = str(value)
    if text in ("on", "off", "yes", "no", "true", "false") or ": " in text:
        return f'"{text}"'
    return text


@dataclass
class ControllerTypeDocs:
    order: int
    type: str
    entity_arg: str
    domain: str | None
    cls: str
    delay: int | None
    mappings: DocsMapping
    integrations_list: list[str]

    @property
    def entity_name(self) -> str:
        entity_name = "my_entity_id"
        return entity_name if self.domain is None else f"{self.domain}.{entity_name}"

    @property
    def section(self) -> str:
        """Anchor of this controller type in pages (e.g. `media-player`)."""
        return "-".join(self.type.lower().split())

    @property
    def integrations_examples(self) -> list[dict[str, Any]]:
        return [
            integration
            for integration in INTEGRATIONS_EXAMPLES
            if integration["name"] in self.integrations_list
        ]

    @property
    def integrations_titles(self) -> list[str]:
        return [
            INTEGRATIONS_TITLES[integration] for integration in self.integrations_list
        ]

    def mapping_by_integration(self) -> dict[str, dict[str, str | None]]:
        result: dict[str, dict[str, str | None]] = {
            integration: {} for integration in self.integrations_list
        }
        for predefined_action, integrations in self.mappings.items():
            for integration, action_events in integrations.items():
                for action_event in action_events:
                    result[integration][str(action_event)] = predefined_action
        return result

    def _decorate_action_event(self, action_event: ActionEvent) -> str:
        value = str(action_event)
        if value in ("on", "off"):
            value = f'"{value}"'
        return f"`{value}`"

    def make_table(self, predefined_actions_link: str) -> str:
        header = [INTEGRATIONS_TITLES[i] for i in self.integrations_list] + [
            f"[Predefined action]({predefined_actions_link}#{self.section})"
        ]
        table = [
            "| " + " | ".join(header) + " |",
            "|" + "|".join(" --- " for _ in header) + "|",
        ]
        for predefined_action, integrations in self.mappings.items():
            cells = [
                ", ".join(
                    self._decorate_action_event(value)
                    for value in integrations.get(integration, [])
                )
                for integration in self.integrations_list
            ]
            cells.append(
                f"`{predefined_action}`"
                if predefined_action is not None
                else "_No action_"
            )
            table.append("| " + " | ".join(cells) + " |")
        return "\n".join(table)

    def example_yaml(
        self, example: dict[str, Any], app_name: str = "example_app"
    ) -> str:
        lines = [
            f"{app_name}:",
            "  module: controllerx",
            f"  class: {self.cls}",
        ]
        if "attrs" in example:
            lines.append("  integration:")
            lines.append(f"    name: {example['name']}")
            for key, value in example["attrs"].items():
                lines.append(f"    {key}: {_yaml_scalar(value)}")
        else:
            lines.append(f"  integration: {example['name']}")
        lines.append(f"  controller: {_yaml_scalar(example['controller'])}")
        lines.append(f"  {self.entity_arg}: {self.entity_name}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "anchor": self.section,
            "class": self.cls,
            "entity_arg": self.entity_arg,
            "domain": self.domain,
            "default_delay_ms": self.delay,
            "integrations": self.integrations_list,
            "default_mapping": self.mapping_by_integration(),
        }


@dataclass
class ControllerDocs:
    name: str
    manufacturer: str
    controller_type_docs: list[ControllerTypeDocs]
    notes: str | None

    @property
    def model(self) -> str:
        """Device name without the manufacturer prefix (e.g. `Legrand600083`)."""
        prefix = self.manufacturer.replace(" ", "")
        model = re.sub(f"^{re.escape(prefix)}", "", self.name, flags=re.IGNORECASE)
        return model or self.name

    @property
    def title(self) -> str:
        return f"{self.manufacturer} {self.model}"

    @property
    def integrations_list(self) -> list[str]:
        integrations: list[str] = []
        for ct_docs in self.controller_type_docs:
            for integration in ct_docs.integrations_list:
                if integration not in integrations:
                    integrations.append(integration)
        return integrations

    @property
    def integrations_titles(self) -> list[str]:
        return [INTEGRATIONS_TITLES[i] for i in self.integrations_list]

    @property
    def types(self) -> list[str]:
        return [ct_docs.type for ct_docs in self.controller_type_docs]

    @property
    def description(self) -> str:
        return (
            f"ControllerX default button mappings and example configuration for the "
            f"{self.title} ({_join_words(self.types)} controller) "
            f"with {_join_words(self.integrations_titles)}."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.name,
            "title": self.title,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "url": f"controllers/{self.name}/",
            "image": f"assets/controllers/{self.name}.jpeg",
            "integrations": self.integrations_list,
            "notes": self.notes,
            "controller_types": [ct.to_dict() for ct in self.controller_type_docs],
        }


def _join_words(words: list[str]) -> str:
    if len(words) <= 1:
        return "".join(words)
    return ", ".join(words[:-1]) + " and " + words[-1]


def get_device_name(controller: str) -> str:
    return (
        controller.replace("Z2MLightController", "")
        .replace("LightController", "")
        .replace("MediaPlayerController", "")
        .replace("SwitchController", "")
        .replace("CoverController", "")
        .replace("Controller", "")
    )


def get_manufacturer(controller: TypeController[Entity]) -> str:
    module = controller.__class__.__module__.rsplit(".", 1)[-1]
    if module not in MANUFACTURERS:
        raise ValueError(
            f"Add the manufacturer name for the `{module}` module "
            "to MANUFACTURERS in docs/main.py"
        )
    return MANUFACTURERS[module]


def get_controller_type(controller: TypeController[Entity]) -> tuple[str, int]:
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
            f"{controller.__class__.__name__} does not belong to any of the 5 type controllers"
        )


def get_controller_docs(controller: TypeController[Entity]) -> ControllerTypeDocs:
    controller_type, order = get_controller_type(controller)
    controller_class = controller.__class__.__name__
    delay: int | None = None
    if isinstance(controller, ReleaseHoldController):
        delay = controller.default_delay()
    mappings: DocsMapping = defaultdict(lambda: defaultdict(list))
    integrations = []

    integration_mappings_funcs: dict[
        str, Callable[[], DefaultActionsMapping | None]
    ] = {
        "z2m": controller.get_z2m_actions_mapping,
        "deconz": controller.get_deconz_actions_mapping,
        "zha": controller.get_zha_actions_mapping,
        "state": controller.get_state_actions_mapping,
        "lutron_caseta": controller.get_lutron_caseta_actions_mapping,
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


def get_controllers() -> list[TypeController[Entity]]:
    with mock.patch.object(hass.Hass, "__init__", return_value=None):
        controller_instances = get_instances(
            devices_module.__file__,
            devices_module.__package__,
            TypeController,
        )
    return controller_instances


def get_devices() -> dict[str, ControllerDocs]:
    """Supported devices sorted by name (case-insensitive)."""
    devices: dict[str, list[ControllerTypeDocs]] = defaultdict(list)
    manufacturers: dict[str, str] = {}
    for controller in get_controllers():
        device_name = get_device_name(controller.__class__.__name__)
        if device_name in DEPRECATED_CONTROLLERS:
            continue
        devices[device_name].append(get_controller_docs(controller))
        manufacturers[device_name] = get_manufacturer(controller)

    devices_docs: dict[str, ControllerDocs] = {}
    for device_name in sorted(devices, key=str.lower):
        # Sort the controller types,
        # so they appear in the same order in the documentation
        docs = sorted(devices[device_name], key=lambda c: c.order)
        devices_docs[device_name] = ControllerDocs(
            name=device_name,
            manufacturer=manufacturers[device_name],
            controller_type_docs=docs,
            notes=NOTES.get(device_name),
        )

    return devices_docs


def get_catalogue(devices: dict[str, ControllerDocs]) -> dict[str, Any]:
    """Machine-readable catalogue of the supported devices."""
    return {
        "version": __version__,
        "description": (
            "Devices supported by ControllerX with their controller classes, "
            "supported integrations and default button mappings "
            "(integration action event -> predefined action). "
            "URLs are relative to https://xaviml.github.io/controllerx/"
        ),
        "integrations": {
            name: {
                "title": integration.title,
                "url": integration.page.removesuffix(".md") + "/",
            }
            for name, integration in INTEGRATIONS.items()
        },
        "integration_examples": INTEGRATIONS_EXAMPLES,
        "devices": [device.to_dict() for device in devices.values()],
    }
