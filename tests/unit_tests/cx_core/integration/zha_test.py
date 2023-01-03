from typing import Any, Dict, Optional

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.zha import ZHAIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "command, args, expected_called_with",
    [
        ("test_command", [0, 1, 2], "test_command_0_1_2"),
        ("testcommand", [0, 2], "testcommand_0_2"),
        ("testcommand", [], "testcommand"),
        ("testcommand", ["string"], "testcommand_string"),
        ("release", [1, 2, 3], "release"),
        ("stop", [1, 2, 3], "stop"),
        (
            "hold",
            {"press_type": "hold", "command_id": 0, "args": [3, 0, 0, 0]},
            "hold_3_0_0_0",
        ),
        (
            "button_double",
            {"press_type": "double", "command_id": 0, "args": [2, 0, 0, 0]},
            "button_double_2_0_0_0",
        ),
        (
            "button_single",
            {"press_type": "single", "command_id": 0, "args": [1, 0, 0, 0]},
            "button_single_1_0_0_0",
        ),
        (
            "button_single",
            {"value": 257.0, "activated_face": 2},
            None,
        ),
    ],
)
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    command: str,
    args: Dict[str, Any],
    expected_called_with: Optional[str],
) -> None:
    data = {"command": command, "args": args}
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    zha_integration = ZHAIntegration(fake_controller, {})
    await zha_integration.event_callback("test", data, {})

    if expected_called_with is not None:
        handle_action_patch.assert_called_once_with(expected_called_with, extra=data)
    else:
        handle_action_patch.assert_not_called()


async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    zha_integration = ZHAIntegration(fake_controller, {})

    await zha_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        zha_integration.event_callback,
        "zha_event",
        device_ieee=controller_id,
    )
