from typing import Dict, Optional

import pytest
from cx_core.controller import Controller
from cx_core.integration.deconz import DeCONZIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, type, expected",
    [
        (
            {"id": 123, "event": 1002},
            None,
            1002,
        ),
        (
            {"id": 123, "gesture": 2},
            "gesture",
            2,
        ),
    ],
)
@pytest.mark.asyncio
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict,
    type: Optional[str],
    expected: str,
):
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    kwargs = {}
    if type is not None:
        kwargs["type"] = type
    deconz_integration = DeCONZIntegration(fake_controller, kwargs)
    await deconz_integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)
