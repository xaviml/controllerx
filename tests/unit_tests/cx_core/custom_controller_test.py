from typing import Any, Dict, List, Tuple, Type

import pytest
from _pytest.monkeypatch import MonkeyPatch
from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from cx_const import PredefinedActionsMapping
from cx_core import (
    CallServiceController,
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
)
from cx_core.type_controller import TypeController
from pytest_mock.plugin import MockerFixture

from tests.test_utils import fake_fn


@pytest.mark.parametrize(
    "custom_cls, mapping, action_input, mock_function, expected_calls",
    [
        (LightController, {"action1": "on"}, "action1", "on", 1),
        (LightController, {"action1": "toggle"}, "action1", "toggle", 1),
        (LightController, {"action1": "off"}, "action1", "off", 1),
        (
            LightController,
            {"action1": "on_min_brightness"},
            "action1",
            "on_min",
            1,
        ),
        (
            LightController,
            {"action1": "hold_brightness_up"},
            "action1",
            "hold",
            1,
        ),
        (
            LightController,
            {"action1": "hold_brightness_up"},
            "action2",
            "hold",
            0,
        ),
        (
            MediaPlayerController,
            {"action1": "play_pause"},
            "action1",
            "play_pause",
            1,
        ),
        (
            MediaPlayerController,
            {"action1": "hold_volume_up"},
            "action1",
            "hold",
            1,
        ),
        (MediaPlayerController, {"action1": "release"}, "action1", "release", 1),
        (SwitchController, {"action1": "toggle"}, "action1", "toggle", 1),
        (CoverController, {"action1": "open"}, "action2", "open", 0),
    ],
)
@pytest.mark.asyncio
async def test_custom_controllers(
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    custom_cls: Type[TypeController],
    mapping: PredefinedActionsMapping,
    action_input: str,
    mock_function: str,
    expected_calls: int,
):
    sut = custom_cls()  # type: ignore
    sut.args = {
        "controller": "test_controller",
        "integration": "z2m",
        "light": "light.test_light",
        "media_player": "media_player.test_media_player",
        "switch": "switch.test_switch",
        "cover": "cover.test_cover",
        "mapping": mapping,
    }
    mocked = mocker.patch.object(sut, mock_function)
    monkeypatch.setattr(sut, "get_entity_state", fake_fn(async_=True, to_return="0"))

    # SUT
    await sut.initialize()
    sut.action_delta = 0
    await sut.handle_action(action_input)

    # Check
    assert mocked.call_count == expected_calls


@pytest.mark.parametrize(
    "integration, services, expected_calls",
    [
        (
            "z2m",
            {
                "service": "homeassistant/test_service",
                "data": {"attr1": "test", "attr2": "test"},
            },
            [("homeassistant/test_service", {"attr1": "test", "attr2": "test"})],
        ),
        (
            "deconz",
            {
                "service": "homeassistant.test_service",
                "data": {"attr1": "test", "attr2": "test"},
            },
            [("homeassistant/test_service", {"attr1": "test", "attr2": "test"})],
        ),
        (
            "zha",
            {"service": "homeassistant.test_service2", "data": {}},
            [("homeassistant/test_service2", {})],
        ),
        (
            "z2m",
            {"service": "homeassistant/test_service2"},
            [("homeassistant/test_service2", {})],
        ),
        (
            "deconz",
            [
                {"service": "homeassistant/test_service1"},
                {"service": "homeassistant.test_service2", "data": {"attr1": "test"}},
            ],
            [
                ("homeassistant/test_service1", {}),
                ("homeassistant/test_service2", {"attr1": "test"}),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_call_service_controller(
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    integration: str,
    services: List[Dict[str, Any]],
    expected_calls: List[Tuple[str, Dict[str, Any]]],
):
    sut = CallServiceController()  # type: ignore
    sut.args = {
        "controller": "test_controller",
        "integration": integration,
        "mapping": {"action": services},
    }
    call_service_stub = mocker.patch.object(Hass, "call_service")

    # SUT
    await sut.initialize()
    sut.action_delta = 0
    await sut.handle_action("action")

    # Checks
    assert call_service_stub.call_count == len(expected_calls)
    for expected_service, expected_data in expected_calls:
        call_service_stub.assert_any_call(sut, expected_service, **expected_data)
