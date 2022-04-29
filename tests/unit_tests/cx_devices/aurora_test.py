import pytest
from cx_core.integration import EventData
from cx_devices.aurora import AUA1ZBR2GWLightController


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "on"}, "1_toggle"),
        ({"command": "on", "endpoint_id": 2}, "2_toggle"),
        ({"command": "off"}, "1_toggle"),
        ({"command": "step", "args": [0]}, "1_step_up"),
        ({"command": "step", "args": [3]}, "1_step_up"),
        ({"command": "step_color_temp", "args": [1]}, "1_step_color_temp_down"),
    ],
)
def test_zha_action_WXKG01LMLightController(
    data: EventData, expected_action: str
) -> None:
    sut = AUA1ZBR2GWLightController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action
