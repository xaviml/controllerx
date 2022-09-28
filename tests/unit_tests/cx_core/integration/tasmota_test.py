from typing import Optional

import pytest
from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_core.controller import Controller
from cx_core.integration import EventData
from cx_core.integration.tasmota import TasmotaIntegration
from pytest_mock.plugin import MockerFixture

from tests.test_utils import wrap_execution


@pytest.mark.parametrize(
    "data, component_key, payload_key, expected, error_expected",
    [
        (
            {"payload": '{"Component": {"Action": "TOGGLE"}}'},
            "Component",
            "Action",
            "TOGGLE",
            False,
        ),
        (
            {"payload": '{"Component": {"Action": "TOGGLE"}}'},
            "Component2",
            "Action",
            None,
            False,
        ),
        (
            {"payload": '{"Component": {"Action": "TOGGLE"}}'},
            "Component",
            "Action2",
            None,
            True,
        ),
        (
            {},
            None,
            None,
            None,
            False,
        ),
        (
            {"payload": "Component"},
            "Component",
            "Action",
            None,
            True,
        ),
    ],
)
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: EventData,
    component_key: Optional[str],
    payload_key: Optional[str],
    expected: Optional[str],
    error_expected: bool,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    mqtt_integration = TasmotaIntegration(
        fake_controller, {"key": payload_key, "component": component_key}
    )

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await mqtt_integration.event_callback("test", data, {})

    if expected is not None:
        handle_action_patch.assert_called_once_with(expected)
    else:
        handle_action_patch.assert_not_called()


async def test_listen_changes_success(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    kwargs = {"component": "my_component"}
    listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    mqtt_integration = TasmotaIntegration(fake_controller, kwargs)

    await mqtt_integration.listen_changes(controller_id)

    listen_event_mock.assert_called_once_with(
        fake_controller,
        mqtt_integration.event_callback,
        topic=controller_id,
        namespace="mqtt",
    )


async def test_listen_changes_fail(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    mqtt_integration = TasmotaIntegration(fake_controller, {})

    with wrap_execution(exception=ValueError):
        await mqtt_integration.listen_changes(controller_id)

    listen_event_mock.assert_not_called()
