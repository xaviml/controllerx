from typing import Any, Dict, List, Tuple, Type

import pytest
from appdaemon.adapi import ADAPI
from cx_const import PredefinedActionsMapping
from cx_core import (
    Controller,
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
)
from cx_core.type_controller import Entity, TypeController
from pytest import MonkeyPatch
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
async def test_custom_controllers(
    mocker: MockerFixture,
    custom_cls: Type[TypeController[Entity]],
    mapping: PredefinedActionsMapping,
    action_input: str,
    mock_function: str,
    expected_calls: int,
) -> None:
    sut = custom_cls(**{})
    sut.args = {
        "controller": "test_controller",
        "integration": "z2m",
        "light": "light.test_light",
        "media_player": "media_player.test_media_player",
        "switch": "switch.test_switch",
        "cover": "cover.test_cover",
        "mapping": mapping,
        "action_delta": 0,
    }
    mocked = mocker.stub()

    async def mocked_fn() -> None:
        mocked()

    mocker.patch.object(sut, mock_function, mocked_fn)
    mocker.patch.object(sut, "get_state", fake_fn(None, async_=True))
    mocker.patch.object(sut, "get_entity_state", fake_fn(async_=True, to_return="0"))

    # SUT
    await sut.initialize()
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
            "lutron_caseta",
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
async def test_call_service_controller(
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    integration: str,
    services: List[Dict[str, Any]],
    expected_calls: List[Tuple[str, Dict[str, Any]]],
) -> None:
    sut = Controller(**{})
    sut.args = {
        "controller": "test_controller",
        "integration": integration,
        "mapping": {"action": services},
        "action_delta": 0,
    }
    call_service_stub = mocker.patch.object(ADAPI, "call_service")

    # SUT
    await sut.initialize()
    await sut.handle_action("action")

    # Checks
    assert call_service_stub.call_count == len(expected_calls)
    for expected_service, expected_data in expected_calls:
        call_service_stub.assert_any_call(sut, expected_service, **expected_data)
