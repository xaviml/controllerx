import pytest
from cx_core.stepper import Stepper
from cx_core.stepper.index_loop_stepper import IndexLoopStepper
from typing_extensions import Literal


@pytest.mark.parametrize(
    "size, value, direction, expected_value",
    [
        (10, 5, Stepper.DOWN, 4),
        (10, 5, Stepper.UP, 6),
        (10, 1, Stepper.DOWN, 0),
        (10, 9, Stepper.UP, 0),
        (10, 0, Stepper.DOWN, 9),
        (10, 10, Stepper.UP, 0),
        (10, -1, Stepper.DOWN, 9),
    ],
)
def test_index_loop_stepper(
    size: int,
    value: int,
    direction: Literal["up", "down"],
    expected_value: int,
):
    stepper = IndexLoopStepper(size)
    stepper_output = stepper.step(value, direction)
    assert stepper_output.next_value == expected_value
    assert not stepper_output.exceeded
