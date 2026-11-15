"""
Checks that the hand-written documentation stays in sync with the code.
"""

import re
from pathlib import Path

import pytest
from cx_core import (
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
    Z2MLightController,
)
from cx_core.type_controller import Entity, TypeController

DOCS_DIR = Path(__file__).parents[2] / "docs" / "docs"
PREDEFINED_ACTIONS_DOC = DOCS_DIR / "advanced" / "predefined-actions.md"

# Section title in predefined-actions.md -> controller type
SECTIONS: dict[str, type[TypeController[Entity]]] = {
    "Light": LightController,
    "Zigbee2MQTT Light": Z2MLightController,
    "Media Player": MediaPlayerController,
    "Switch": SwitchController,
    "Cover": CoverController,
}


def get_documented_actions(section: str) -> set[str]:
    content = PREDEFINED_ACTIONS_DOC.read_text()
    match = re.search(
        rf"^## {re.escape(section)}\n(.*?)(?=^#{{1,2}} )", content, re.S | re.M
    )
    assert match is not None, f"Section '## {section}' not found"
    actions = set()
    for line in match.group(1).splitlines():
        # Table rows look like: | `toggle` | description | parameters |
        row = re.match(r"^\|\s*`\"?([^`\"]+)\"?`\s*\|", line)
        if row:
            actions.add(row.group(1))
    return actions


@pytest.mark.parametrize("section, controller_type", SECTIONS.items())
def test_predefined_actions_are_documented(
    section: str, controller_type: type[TypeController[Entity]]
) -> None:
    controller = controller_type(**{})
    code_actions = set(controller.get_predefined_actions_mapping().keys())
    documented_actions = get_documented_actions(section)

    missing = sorted(code_actions - documented_actions)
    unknown = sorted(documented_actions - code_actions)
    assert not missing, (
        f"Predefined actions missing in {PREDEFINED_ACTIONS_DOC.name} "
        f"under '## {section}': {missing}"
    )
    assert not unknown, (
        f"{PREDEFINED_ACTIONS_DOC.name} documents actions under '## {section}' "
        f"that do not exist in {controller_type.__name__}: {unknown}"
    )
