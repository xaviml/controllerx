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
            {"service": "homeassistant.test_service2", "data": {},},
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
    hass_mock, monkeypatch, mocker, integration, services, expected_calls,
):
    sut = CallServiceController()
    sut.args = {
        "controller": "test_controller",
        "integration": integration,
        "mapping": {"action": services},
    }
    call_service_stub = mocker.stub()

    async def fake_call_service(self, service, **data):
        call_service_stub(service, **data)

    monkeypatch.setattr(Controller, "call_service", fake_call_service)

    sut.initialize()
    sut.action_delta = 0
    await sut.handle_action("action")

    assert call_service_stub.call_count == len(expected_calls)
    for expected_service, expected_data in expected_calls:
        call_service_stub.assert_any_call(expected_service, **expected_data)
