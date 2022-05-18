from typing import Any, Dict

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.shelly import ShellyIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "device_id": "e09c64a22553484d804353ef97f6fcd6",
                "device": "shellybutton1-A4C12A45174",
                "channel": 1,
                "click_type": "single",
                "generation": 1,
            },
            "single_1",
        ),
        (
            {
                "device_id": "e09d64a22553384d8043532f97f6fcd6",
                "device": "shellybutton1-A4C13B45274",
                "channel": 3,
                "click_type": "btn_down",
                "generation": 1,
            },
            "btn_down_3",
        ),
    ],
)
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict[str, Any],
    expected: str,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    shelly_integration = ShellyIntegration(fake_controller, {})
    await shelly_integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)


async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    shelly_integration = ShellyIntegration(fake_controller, {})

    await shelly_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        shelly_integration.event_callback,
        "shelly.click",
        device=controller_id,
    )
