import pytest
from cx_core.stepper import MinMax, Stepper
from cx_core.stepper.loop_stepper import LoopStepper
from typing_extensions import Literal


@pytest.mark.parametrize(
    "min_max, value, steps, direction, expected_value",
    [
        (MinMax(0, 10), 5, 10, Stepper.DOWN, 4),
        (MinMax(0, 10), 5, 10, Stepper.UP, 6),
        (MinMax(0, 10), 1, 10, Stepper.DOWN, 0),
        (MinMax(0, 10), 9, 10, Stepper.UP, 10),
        (MinMax(0, 10), 0, 10, Stepper.DOWN, 10),
        (MinMax(0, 10), 10, 10, Stepper.UP, 0),
        (MinMax(0, 10), -1, 10, Stepper.DOWN, 9),
        (MinMax(0, 10), 11, 10, Stepper.UP, 1),
        (MinMax(0, 10), 6, 5, Stepper.DOWN, 4),
        (MinMax(0, 10), 4, 5, Stepper.UP, 6),
    ],
)
def test_loop_stepper(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
):
    stepper = LoopStepper(min_max, steps)
    new_value, _ = stepper.step(value, direction)
    assert new_value == expected_value
