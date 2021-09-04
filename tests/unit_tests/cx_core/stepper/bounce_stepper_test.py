import pytest
from cx_core.stepper import MinMax, Stepper
from cx_core.stepper.bounce_stepper import BounceStepper
from typing_extensions import Literal


@pytest.mark.parametrize(
    "min_max, value, steps, direction, expected_value, expected_direction",
    [
        (MinMax(0, 10), 5, 10, Stepper.DOWN, 4, Stepper.DOWN),
        (MinMax(0, 10), 5, 10, Stepper.UP, 6, Stepper.UP),
        (MinMax(0, 10), 1, 10, Stepper.DOWN, 0, Stepper.UP),
        (MinMax(0, 10), 9, 10, Stepper.UP, 10, Stepper.DOWN),
        (MinMax(0, 10), 0, 10, Stepper.DOWN, 1, Stepper.UP),
        (MinMax(0, 10), 0, 10, Stepper.UP, 1, Stepper.UP),
        (MinMax(0, 10), 10, 10, Stepper.UP, 9, Stepper.DOWN),
        (MinMax(0, 10), 10, 10, Stepper.DOWN, 9, Stepper.DOWN),
        (MinMax(0, 10), -1, 10, Stepper.DOWN, 1, Stepper.UP),
        (MinMax(0, 10), 11, 10, Stepper.UP, 9, Stepper.DOWN),
        (MinMax(0, 10), 6, 5, Stepper.DOWN, 4, Stepper.DOWN),
        (MinMax(0, 10), 4, 5, Stepper.UP, 6, Stepper.UP),
    ],
)
def test_bounce_stepper(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
    expected_direction: Literal["up", "down"],
):
    stepper = BounceStepper(min_max, steps)
    stepper_output = stepper.step(value, direction)
    assert stepper_output.next_value == expected_value
    assert stepper_output.next_direction == expected_direction
    assert not stepper_output.exceeded
