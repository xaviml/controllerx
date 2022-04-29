import pytest
from cx_core.integration import EventData
from cx_devices.muller_licht import MLI404002LightController


@pytest.mark.parametrize(
    "data, expected_action",
    [
        (
            {"command": "on", "args": []},
            "on",
        ),
        (
            {"command": "off", "args": []},
            "off",
        ),
        (
            {"command": "step", "args": [0, 43, 3]},
            "step_up",
        ),
        (
            {"command": "move", "args": [0, 100]},
            "move_up",
        ),
        (
            {"command": "step", "args": [1, 43, 3]},
            "step_down",
        ),
        (
            {"command": "move", "args": [1, 100]},
            "move_down",
        ),
        (
            {"command": "stop", "args": []},
            "stop",
        ),
        (
            {"command": "recall", "args": [16387, 1]},
            "recall",
        ),
    ],
)
def test_zha_action_MLI404002(data: EventData, expected_action: str) -> None:
    sut = MLI404002LightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action
