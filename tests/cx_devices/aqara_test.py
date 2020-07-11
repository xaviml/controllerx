import pytest
from cx_devices.aqara import MFKZQ01LMLightController, WXKG01LMLightController


@pytest.mark.parametrize(
    "command, args, expected_action",
    [
        ("shake", {}, "shake"),
        ("knock", {}, "knock"),
        ("slide", {}, "slide"),
        ("flip", {"flip_degrees": 90}, "flip90"),
        ("flip", {"flip_degrees": 180}, "flip180"),
        ("rotate_left", {}, "rotate_left"),
        ("rotate_right", {}, "rotate_right"),
    ],
)
def test_zha_action_MFKZQ01LMLightController(command, args, expected_action):
    sut = MFKZQ01LMLightController()
    action = sut.get_zha_action(command, args)
    assert action == expected_action


@pytest.mark.parametrize(
    "command, args, expected_action",
    [
        ("click", {"click_type": "single"}, "single"),
        ("click", {"click_type": "double"}, "double"),
        ("click", {"click_type": "triple"}, "triple"),
        ("click", {"click_type": "quadruple"}, "quadruple"),
        ("click", {"click_type": "furious"}, "furious"),
    ],
)
def test_zha_action_WXKG01LMLightController(command, args, expected_action):
    sut = WXKG01LMLightController()
    action = sut.get_zha_action(command, args)
    assert action == expected_action
