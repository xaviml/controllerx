from typing import Literal

import pytest
from cx_const import StepperDir
from cx_core.stepper import MinMax
from cx_core.stepper.loop_stepper import LoopStepper


@pytest.mark.parametrize(
    "min_max, value, steps, direction, expected_value",
    [
        (MinMax(0, 10), 5, 10, StepperDir.DOWN, 4),
        (MinMax(0, 10), 5, 10, StepperDir.UP, 6),
        (MinMax(0, 10), 1, 10, StepperDir.DOWN, 0),
        (MinMax(0, 10), 9, 10, StepperDir.UP, 0),
        (MinMax(0, 10), 0, 10, StepperDir.DOWN, 9),
        (MinMax(0, 10), 10, 10, StepperDir.UP, 1),
        (MinMax(0, 10), -1, 10, StepperDir.DOWN, 9),
        (MinMax(0, 10), 11, 10, StepperDir.UP, 1),
        (MinMax(0, 10), 6, 5, StepperDir.DOWN, 4),
        (MinMax(0, 10), 4, 5, StepperDir.UP, 6),
        (MinMax(0, 1), 0.2, 10, StepperDir.UP, 0.3),
        (MinMax(0, 1), 0.1, 5, StepperDir.DOWN, 0.9),
        (MinMax(153, 500), 160, 10, StepperDir.DOWN, 472.3),
        (MinMax(153, 500), 490, 5, StepperDir.UP, 212.4),
    ],
)
def test_loop_stepper(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
) -> None:
    stepper = LoopStepper(min_max, steps)
    stepper_output = stepper.step(value, direction)
    assert stepper_output.next_value == expected_value
    assert not stepper_output.exceeded
