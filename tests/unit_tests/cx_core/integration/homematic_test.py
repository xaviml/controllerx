from typing import Optional, Set

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration import EventData
from cx_core.integration.homematic import HomematicIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, registered_controllers, expected",
    [
        (
            {"name": "MyController", "param": "PRESS_SHORT", "channel": 1},
            {"MyController"},
            "PRESS_SHORT_1",
        ),
        (
            {"name": "MyController", "param": "PRESS_LONG", "channel": 2},
            {"MyController"},
            "PRESS_LONG_2",
        ),
        (
            {"name": "MyController", "param": "PRESS_LONG", "channel": 2},
            {"MyController2"},
            None,
        ),
    ],
)
@pytest.mark.asyncio
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: EventData,
    registered_controllers: Set[str],
    expected: Optional[str],
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    integration = HomematicIntegration(fake_controller, {})
    integration._registered_controller_ids = registered_controllers

    await integration.event_callback("test", data, {})

    if expected is None:
        handle_action_patch.assert_not_called()
    else:
        handle_action_patch.assert_called_once_with(expected, extra=data)


@pytest.mark.asyncio
async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    integration = HomematicIntegration(fake_controller, {})
    assert integration._registered_controller_ids == set()

    await integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller, integration.event_callback, "homematic.keypress"
    )
    assert integration._registered_controller_ids == {controller_id}
