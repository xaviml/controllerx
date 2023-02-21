import pytest
from cx_core import MediaPlayerController
from cx_core.integration import EventData
from cx_devices.aqara import (
    MFKZQ01LMLightController,
    WXCJKG13LMMediaPlayerController,
    WXKG01LMLightController,
    WXKG11LMRemoteLightController,
    WXKG11LMSensorSwitchLightController,
)


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "shake"}, "shake"),
        ({"command": "knock"}, "knock"),
        ({"command": "slide"}, "slide"),
        ({"command": "flip", "args": {"flip_degrees": 90}}, "flip90"),
        ({"command": "flip", "args": {"flip_degrees": 180}}, "flip180"),
        ({"command": "rotate_left"}, "rotate_left"),
        ({"command": "rotate_right"}, "rotate_right"),
    ],
)
def test_zha_action_MFKZQ01LMLightController(
    data: EventData, expected_action: str
) -> None:
    sut = MFKZQ01LMLightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "click", "args": {"click_type": "single"}}, "single"),
        ({"command": "click", "args": {"click_type": "double"}}, "double"),
        ({"command": "click", "args": {"click_type": "triple"}}, "triple"),
        ({"command": "click", "args": {"click_type": "quadruple"}}, "quadruple"),
        ({"command": "click", "args": {"click_type": "furious"}}, "furious"),
        (
            {"command": "attribute_updated", "args": {"value": True}},
            "attribute_updated",
        ),
    ],
)
def test_zha_action_WXKG01LMLightController(
    data: EventData, expected_action: str
) -> None:
    sut = WXKG01LMLightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "single"}, "single"),
        ({"command": "double"}, "double"),
        ({"command": "hold"}, "hold"),
        ({"command": "release"}, "release"),
    ],
)
def test_zha_action_WXKG11LMRemoteLightController(
    data: EventData, expected_action: str
) -> None:
    sut = WXKG11LMRemoteLightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"args": {"value": 0}}, ""),
        ({"args": {"value": 1}}, "single"),
        ({"args": {"value": 2}}, "double"),
        ({"args": {"value": 3}}, "triple"),
        ({"args": {"value": 4}}, "quadruple"),
    ],
)
def test_zha_action_WXKG11LMSensorSwitchLightController(
    data: EventData, expected_action: str
) -> None:
    sut = WXKG11LMSensorSwitchLightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action


def test_type_WXCJKG13LMMediaPlayerController() -> None:
    sut = WXCJKG13LMMediaPlayerController()

    assert isinstance(sut, MediaPlayerController)
