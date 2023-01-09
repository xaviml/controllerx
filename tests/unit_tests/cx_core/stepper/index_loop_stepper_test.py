from typing import Literal

import pytest
from cx_const import StepperDir
from cx_core.stepper.index_loop_stepper import IndexLoopStepper


@pytest.mark.parametrize(
    "size, value, direction, expected_value",
    [
        (10, 5, StepperDir.DOWN, 4),
        (10, 5, StepperDir.UP, 6),
        (10, 1, StepperDir.DOWN, 0),
        (10, 9, StepperDir.UP, 0),
        (10, 0, StepperDir.DOWN, 9),
        (10, 10, StepperDir.UP, 0),
        (10, -1, StepperDir.DOWN, 9),
    ],
)
def test_index_loop_stepper(
    size: int,
    value: int,
    direction: Literal["up", "down"],
    expected_value: int,
) -> None:
    stepper = IndexLoopStepper(size)
    stepper_output = stepper.step(value, direction)
    assert stepper_output.next_value == expected_value
    assert not stepper_output.exceeded
