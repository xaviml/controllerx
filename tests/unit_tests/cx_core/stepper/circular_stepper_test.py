from typing import Tuple

import pytest
from cx_core.stepper import Stepper
from cx_core.stepper.circular_stepper import CircularStepper
from typing_extensions import Literal


@pytest.mark.parametrize(
    "minmax, value, steps, direction, expected_value",
    [
        ((0, 10), 5, 10, Stepper.DOWN, 4),
        ((0, 10), 5, 10, Stepper.UP, 6),
        ((0, 10), 1, 10, Stepper.DOWN, 0),
        ((0, 10), 9, 10, Stepper.UP, 10),
        ((0, 10), 0, 10, Stepper.DOWN, 10),
        ((0, 10), 10, 10, Stepper.UP, 0),
        ((0, 10), -1, 10, Stepper.DOWN, 9),
        ((0, 10), 11, 10, Stepper.UP, 1),
        ((0, 10), 6, 5, Stepper.DOWN, 4),
        ((0, 10), 4, 5, Stepper.UP, 6),
    ],
)
def test_minmax_stepper(
    minmax: Tuple[int, int],
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
):
    stepper = CircularStepper(*minmax, steps)
    new_value, _ = stepper.step(value, direction)
    assert new_value == expected_value
