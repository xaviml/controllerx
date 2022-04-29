from typing import Dict, Optional

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.deconz import DeCONZIntegration
from pytest_mock.plugin import MockerFixture

from tests.test_utils import wrap_execution


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
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict[str, int],
    type: Optional[str],
    expected: str,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    kwargs = {}
    if type is not None:
        kwargs["type"] = type
    deconz_integration = DeCONZIntegration(fake_controller, kwargs)
    await deconz_integration.event_callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)


@pytest.mark.parametrize(
    "listen_to, expected_id",
    [
        ("id", "id"),
        ("unique_id", "unique_id"),
        (None, "id"),
        ("fake", None),
    ],
)
async def test_listen_changes(
    fake_controller: Controller,
    mocker: MockerFixture,
    listen_to: Optional[str],
    expected_id: Optional[str],
) -> None:
    kwargs = {}
    if listen_to is not None:
        kwargs["listen_to"] = listen_to

    listen_event_mock = mocker.patch.object(Hass, "listen_event")
    deconz_integration = DeCONZIntegration(fake_controller, kwargs)

    with wrap_execution(error_expected=expected_id is None, exception=ValueError):
        await deconz_integration.listen_changes("controller_id")

    if expected_id is not None:
        listen_event_mock.assert_called_once_with(
            fake_controller,
            deconz_integration.event_callback,
            "deconz_event",
            **{expected_id: "controller_id"}
        )
