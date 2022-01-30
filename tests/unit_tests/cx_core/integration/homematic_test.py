from typing import Dict

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.homematic import HomematicIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {"name": "MyController", "param": "PRESS_SHORT", "channel": 1},
            "PRESS_SHORT_1",
        ),
        (
            {"name": "MyController", "param": "PRESS_LONG", "channel": 2},
            "PRESS_LONG_2",
        ),
    ],
)
@pytest.mark.asyncio
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict,
    expected: str,
):
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    integration = HomematicIntegration(fake_controller, {})
    await integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)


@pytest.mark.asyncio
async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
):
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    integration = HomematicIntegration(fake_controller, {})

    await integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        integration.event_callback,
        "homematic.keypress",
        name=controller_id,
    )
