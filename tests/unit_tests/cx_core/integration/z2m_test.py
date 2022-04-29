import json
from typing import Any, Dict, Optional

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_core.controller import Controller
from cx_core.integration import EventData
from cx_core.integration.z2m import Z2MIntegration
from pytest_mock import MockerFixture

from tests.test_utils import wrap_execution


@pytest.mark.parametrize(
    "data, action_key, action_group, handle_action_called, expected_called_with",
    [
        ({"payload": '{"event_1": "action_1"}'}, "event_1", None, True, "action_1"),
        ({}, None, None, False, Any),
        ({"payload": '{"action": "action_1"}'}, None, None, True, "action_1"),
        (
            {"payload": '{"action": "action_1", "action_group": 123}'},
            None,
            123,
            True,
            "action_1",
        ),
        (
            {"payload": '{"action": "action_1", "action_group": 123}'},
            None,
            321,
            False,
            "any",
        ),
        ({"payload": '{"event_1": "action_1"}'}, "event_2", None, False, "Any"),
        ({"payload": '{"action_rate": 195}'}, "action", None, False, "Any"),
    ],
)
async def test_event_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: EventData,
    action_key: str,
    action_group: Optional[int],
    handle_action_called: bool,
    expected_called_with: str,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    kwargs: Dict[str, Any] = {}
    if action_key is not None:
        kwargs["action_key"] = action_key
    if action_group is not None:
        kwargs["action_group"] = action_group
    z2m_integration = Z2MIntegration(fake_controller, kwargs)
    await z2m_integration.event_callback("test", data, {})

    if handle_action_called:
        handle_action_patch.assert_called_once_with(
            expected_called_with, extra=json.loads(data["payload"])
        )
    else:
        handle_action_patch.assert_not_called()


@pytest.mark.parametrize(
    "listen_to, topic_prefix, expected_id",
    [
        ("ha", None, "ha"),
        (None, None, "ha"),
        ("mqtt", None, "mqtt"),
        ("mqtt", "my_prefix", "mqtt"),
        ("fake", None, None),
    ],
)
async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
    listen_to: Optional[str],
    topic_prefix: Optional[str],
    expected_id: Optional[str],
) -> None:
    kwargs = {}
    if listen_to is not None:
        kwargs["listen_to"] = listen_to
    if topic_prefix is not None:
        kwargs["topic_prefix"] = topic_prefix

    hass_listen_state_mock = mocker.patch.object(Hass, "listen_state")
    mqtt_listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    z2m_integration = Z2MIntegration(fake_controller, kwargs)

    with wrap_execution(error_expected=expected_id is None, exception=ValueError):
        await z2m_integration.listen_changes("controller_id")

    if expected_id is None:
        return

    if expected_id == "ha":
        hass_listen_state_mock.assert_called_once_with(
            fake_controller,
            z2m_integration.state_callback,
            "controller_id",
        )
    elif expected_id == "mqtt":
        mqtt_listen_event_mock.assert_called_once_with(
            fake_controller,
            z2m_integration.event_callback,
            topic=f"{topic_prefix or 'zigbee2mqtt'}/controller_id",
            namespace="mqtt",
        )
    else:
        assert False, "expected_id cannot be other than 'ha' or 'mqtt'"
