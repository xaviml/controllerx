from typing import Any, Dict, Optional

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration import EventData
from cx_core.integration.event import EventIntegration
from pytest_mock.plugin import MockerFixture

from tests.test_utils import wrap_execution


@pytest.mark.parametrize(
    "action_template, data, expected_action",
    [
        # Positive cases
        (
            "{type}_{subtype}",
            {
                "type": "press_long",
                "subtype": 1,
                "device_id": "d6ae82a0e7a3caa694cbad346a7aa7bca",
                "name": "Button Interface HM-PBI-4-FM",
            },
            "press_long_1",
        ),
        (
            "{type}_action_{data[event][subtype]}",
            {
                "type": "type1",
                "data": {"event": {"subtype": 1.3}},
            },
            "type1_action_1.3",
        ),
        # Negative cases
        ("action_{a}", {}, None),
        ("action_{a?}", {"a": 1}, None),
        ("action_{a[b]}", {"a": 1}, None),
        ("action_{a[1]}", {"a": 1}, None),
        ("action_{b}", {"a": 1}, None),
        ("action_{print(1)}", {"a": 1}, None),
        ("action_{1+0}", {"a": 1}, None),
    ],
)
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    action_template: str,
    data: EventData,
    expected_action: Optional[str],
) -> None:
    logger_patch = mocker.patch.object(fake_controller, "log")
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    event_integration = EventIntegration(
        fake_controller, {"action_template": action_template}
    )
    await event_integration.event_callback("test", data, {})

    if expected_action is not None:
        handle_action_patch.assert_called_once_with(expected_action)
        logger_patch.assert_not_called()
    else:
        handle_action_patch.assert_not_called()
        logger_patch.assert_called_once_with(
            f"Template `{action_template}` could not be rendered with data={data}",
            level="WARNING",
        )


@pytest.mark.parametrize(
    "kwargs, error_expected",
    [
        ({"event_type": "homematic.keypress", "controller_key": "device_id"}, False),
        ({"controller_key": "device_id"}, True),
        ({"event_type": "homematic.keypress"}, True),
        ({}, True),
    ],
)
async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
    kwargs: Dict[str, Any],
    error_expected: bool,
) -> None:
    controller_id = "controller_id"
    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    event_integration = EventIntegration(fake_controller, kwargs)

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await event_integration.listen_changes(controller_id)

        listen_event_mock.assert_called_once_with(
            fake_controller,
            event_integration.event_callback,
            kwargs["event_type"],
            **{kwargs["controller_key"]: controller_id},
        )
