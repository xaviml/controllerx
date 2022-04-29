import pytest
from cx_core.integration import EventData
from cx_devices.legrand import get_zha_action_LegrandWallController


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"endpoint_id": 1, "command": "off", "args": []}, "1_off"),
        ({"endpoint_id": 1, "command": "on", "args": []}, "1_on"),
        ({"command": "off", "args": []}, "1_off"),
        ({"command": "on", "args": []}, "1_on"),
        ({"endpoint_id": 2, "command": "move", "args": [0, 255]}, "2_move_up"),
        ({"endpoint_id": 2, "command": "move", "args": [1, 255]}, "2_move_down"),
        ({"endpoint_id": 1, "command": "stop"}, "1_stop"),
        ({"endpoint_id": 2, "command": "stop"}, "2_stop"),
    ],
)
def test_get_zha_action_LegrandWallController(
    data: EventData, expected_action: str
) -> None:
    action = get_zha_action_LegrandWallController(data)
    assert action == expected_action
