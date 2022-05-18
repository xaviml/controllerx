from typing import Any, Dict

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.shellyforhass import ShellyForHASSIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "entity_id": "binary_sensor.shelly_shbtn_1_xxxxxx_switch",
                "click_type": "single",
            },
            "single",
        ),
        (
            {
                "entity_id": "binary_sensor.shelly_shbtn_1_xxxxxx_switch",
                "click_type": "double",
            },
            "double",
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
    shellyforhass_integration = ShellyForHASSIntegration(fake_controller, {})
    await shellyforhass_integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)


async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    shellyforhass_integration = ShellyForHASSIntegration(fake_controller, {})

    await shellyforhass_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        shellyforhass_integration.event_callback,
        "shellyforhass.click",
        entity_id=controller_id,
    )
