from typing import Literal

import pytest
from cx_const import StepperDir
from cx_core.stepper import MinMax
from cx_core.stepper.bounce_stepper import BounceStepper


@pytest.mark.parametrize(
    "min_max, value, steps, direction, expected_value, expected_direction",
    [
        (MinMax(0, 10), 5, 10, StepperDir.DOWN, 4, StepperDir.DOWN),
        (MinMax(0, 10), 5, 10, StepperDir.UP, 6, StepperDir.UP),
        (MinMax(0, 10), 1, 10, StepperDir.DOWN, 0, StepperDir.UP),
        (MinMax(0, 10), 9, 10, StepperDir.UP, 10, StepperDir.DOWN),
        (MinMax(0, 10), 0, 10, StepperDir.DOWN, 1, StepperDir.UP),
        (MinMax(0, 10), 0, 10, StepperDir.UP, 1, StepperDir.UP),
        (MinMax(0, 10), 10, 10, StepperDir.UP, 9, StepperDir.DOWN),
        (MinMax(0, 10), 10, 10, StepperDir.DOWN, 9, StepperDir.DOWN),
        (MinMax(0, 10), -1, 10, StepperDir.DOWN, 1, StepperDir.UP),
        (MinMax(0, 10), 11, 10, StepperDir.UP, 9, StepperDir.DOWN),
        (MinMax(0, 10), 6, 5, StepperDir.DOWN, 4, StepperDir.DOWN),
        (MinMax(0, 10), 4, 5, StepperDir.UP, 6, StepperDir.UP),
    ],
)
def test_bounce_stepper(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
    expected_direction: Literal["up", "down"],
) -> None:
    stepper = BounceStepper(min_max, steps)
    stepper_output = stepper.step(value, direction)
    assert stepper_output.next_value == expected_value
    assert stepper_output.next_direction == expected_direction
    assert not stepper_output.exceeded
