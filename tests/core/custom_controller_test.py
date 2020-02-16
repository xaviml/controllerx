import pytest

from core import (
    CallServiceController,
    CustomLightController,
    CustomMediaPlayerController,
    Controller,
)
from tests.utils import hass_mock


@pytest.mark.parametrize(
    "custom_cls, mapping, action_input, mock_function, expected_calls",
    [
        (CustomLightController, {"action1": "on"}, "action1", "on", 1),
        (CustomLightController, {"action1": "toggle"}, "action1", "toggle", 1),
        (CustomLightController, {"action1": "off"}, "action1", "off", 1),
        (
            CustomLightController,
            {"action1": "on_min_brightness"},
            "action1",
            "on_min",
            1,
        ),
        (
            CustomLightController,
            {"action1": "hold_brightness_up"},
            "action1",
            "hold",
            1,
        ),
        (
            CustomLightController,
            {"action1": "hold_brightness_up"},
            "action2",
            "hold",
            0,
        ),
        (
            CustomMediaPlayerController,
            {"action1": "play_pause"},
            "action1",
            "play_pause",
            1,
        ),
        (
            CustomMediaPlayerController,
            {"action1": "hold_volume_up"},
            "action1",
            "hold",
            1,
        ),
        (CustomMediaPlayerController, {"action1": "release"}, "action1", "release", 1),
    ],
)
@pytest.mark.asyncio
async def test_custom_light_controller(
    hass_mock, mocker, custom_cls, mapping, action_input, mock_function, expected_calls
):
    sut = custom_cls()
    sut.args = {
        "controller": "test_controller",
        "integration": "z2m",
        "light": "test_light",
        "media_player": "test_media_player",
        "mapping": mapping,
    }
    mocked = mocker.patch.object(sut, mock_function)
    sut.initialize()
    sut.action_delta = 0
    await sut.handle_action(action_input)

    mocked.call_count == expected_calls


@pytest.mark.parametrize(
    "integration, called_service, data, expected_service_called",
    [
        (
            "z2m",
            "homeassistant/test_service",
            {"attr1": "test", "attr2": "test"},
            "homeassistant/test_service",
        ),
        (
            "deconz",
            "homeassistant.test_service",
            {"attr1": "test", "attr2": "test"},
            "homeassistant/test_service",
        ),
        ("zha", "homeassistant.test_service2", {}, "homeassistant/test_service2",),
        ("z2m", "homeassistant/test_service2", None, "homeassistant/test_service2",),
    ],
)
@pytest.mark.asyncio
async def test_call_service_controller(
    hass_mock, mocker, integration, called_service, data, expected_service_called,
):
    sut = CallServiceController()
    sut.args = {
        "controller": "test_controller",
        "integration": integration,
        "mapping": {"action": {"service": called_service, "data": data}},
    }
    mocked = mocker.patch.object(Controller, "call_service")
    sut.initialize()
    sut.action_delta = 0
    await sut.handle_action("action")

    if data is None:
        mocked.assert_called_with(expected_service_called)
    else:
        mocked.assert_called_with(expected_service_called, **data)
