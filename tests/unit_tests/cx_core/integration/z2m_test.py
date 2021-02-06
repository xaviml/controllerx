from typing import Any, Dict, Optional

import pytest
from cx_core.controller import Controller
from cx_core.integration.z2m import Z2MIntegration
from pytest_mock import MockerFixture


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
@pytest.mark.asyncio
async def test_event_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict,
    action_key: str,
    action_group: Optional[int],
    handle_action_called: bool,
    expected_called_with: str,
):
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    kwargs: Dict[str, Any] = {}
    if action_key is not None:
        kwargs["action_key"] = action_key
    if action_group is not None:
        kwargs["action_group"] = action_group
    z2m_integration = Z2MIntegration(fake_controller, kwargs)
    await z2m_integration.event_callback("test", data, {})

    if handle_action_called:
        handle_action_patch.assert_called_once_with(expected_called_with)
    else:
        handle_action_patch.assert_not_called()
