from typing import Any, Dict

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.lutron_caseta import LutronIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "serial": 28786608,
                "type": "FourGroupRemote",
                "button_number": 4,
                "device_name": "Shade Remote",
                "area_name": "Upstairs Hall",
                "action": "press",
            },
            "button_4_press",
        ),
        (
            {
                "serial": 28786608,
                "type": "FourGroupRemote",
                "button_number": 0,
                "device_name": "Shade Remote",
                "area_name": "Upstairs Hall",
                "action": "hold",
            },
            "button_0_hold",
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
    lutron_integration = LutronIntegration(fake_controller, {})
    await lutron_integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)


async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    lutron_integration = LutronIntegration(fake_controller, {})

    await lutron_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        lutron_integration.event_callback,
        "lutron_caseta_button_event",
        serial=controller_id,
    )
