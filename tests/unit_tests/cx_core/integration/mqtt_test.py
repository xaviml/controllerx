from typing import Optional

import pytest
from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_core.controller import Controller
from cx_core.integration import EventData
from cx_core.integration.mqtt import MQTTIntegration
from pytest_mock.plugin import MockerFixture

from tests.test_utils import wrap_execution


@pytest.mark.parametrize(
    "data, payload_key, expected, error_expected",
    [
        (
            {"payload": "click"},
            None,
            "click",
            False,
        ),
        (
            {
                "payload": '{"battery":99,"illuminance":0,"illuminance_lux":0,"linkquality":255,"occupancy":true,"temperature":27,"voltage":2985}'
            },
            "occupancy",
            "true",
            False,
        ),
        (
            {},
            None,
            None,
            False,
        ),
        (
            {"payload": "fail_payload"},
            "fake_key",
            None,
            True,
        ),
        (
            {
                "payload": '{"battery":99,"illuminance":0,"illuminance_lux":0,"linkquality":255,"occupancy":true,"temperature":27,"voltage":2985}'
            },
            "action",
            None,
            True,
        ),
    ],
)
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: EventData,
    payload_key: Optional[str],
    expected: Optional[str],
    error_expected: bool,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    mqtt_integration = MQTTIntegration(fake_controller, {"key": payload_key})

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await mqtt_integration.event_callback("test", data, {})

    if expected is not None:
        handle_action_patch.assert_called_once_with(expected)
    else:
        handle_action_patch.assert_not_called()


async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    mqtt_integration = MQTTIntegration(fake_controller, {})

    await mqtt_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        mqtt_integration.event_callback,
        topic=controller_id,
        namespace="mqtt",
    )
