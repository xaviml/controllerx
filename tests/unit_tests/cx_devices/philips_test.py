import pytest
from cx_core.integration import EventData
from cx_devices.philips import HueDimmerController


@pytest.mark.parametrize(
    "data, expected_action",
    [
        ({"command": "on_long_release"}, "on_long_release"),
        ({"command": "down_press"}, "down_press"),
        ({"command": "off_hold"}, "off_hold"),
    ],
)
def test_zha_action_HueDimmerController(data: EventData, expected_action: str) -> None:
    sut = HueDimmerController(**{})
    action = sut.get_zha_action(data)
    assert action == expected_action
