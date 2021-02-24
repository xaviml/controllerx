from typing import Dict

import pytest
from cx_core.controller import Controller
from cx_core.integration.mqtt import MQTTIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {"payload": "click"},
            "click",
        ),
        (
            {},
            None,
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
    mqtt_integration = MQTTIntegration(fake_controller, {})
    await mqtt_integration.event_callback("test", data, {})

    if expected is not None:
        handle_action_patch.assert_called_once_with(expected)
    else:
        handle_action_patch.assert_not_called()
