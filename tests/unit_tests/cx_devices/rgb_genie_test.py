import pytest
from cx_core.integration import EventData
from cx_devices.rgb_genie import ZB5122LightController


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "on"}, "on"),
        ({"command": "off"}, "off"),
        ({"command": "stop"}, "stop"),
        ({"command": "move_to_color"}, "move_to_color"),
        ({"command": "move_with_on_off", "args": [0, 50]}, "hold_brightness_up"),
        ({"command": "move_with_on_off", "args": [1, 50]}, "hold_brightness_down"),
        ({"command": "move_hue", "args": [0, 0]}, "stop_move_hue"),
        ({"command": "move_hue", "args": [1, 2]}, "move_hue"),
    ],
)
def test_zha_action_MFKZQ01LMLightController(
    data: EventData, expected_action: str
) -> None:
    sut = ZB5122LightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action
