import pytest

from core.stepper.minmax_stepper import MinMaxStepper
from core.stepper import Stepper


@pytest.mark.parametrize(
    "minmax, value, direction, previous_direction, expected_direction",
    [
        ((0, 10), 10, Stepper.DOWN, None, Stepper.DOWN),
        ((0, 10), 11, Stepper.DOWN, None, Stepper.DOWN),
        ((0, 10), -1, Stepper.DOWN, None, Stepper.DOWN),
        ((0, 10), 5, Stepper.UP, None, Stepper.UP),
        ((0, 10), 5, Stepper.UP, None, Stepper.UP),
        ((0, 10), 5, Stepper.TOGGLE, Stepper.TOGGLE_DOWN, Stepper.TOGGLE_UP),
        ((0, 10), 5, Stepper.TOGGLE, Stepper.TOGGLE_UP, Stepper.TOGGLE_DOWN),
        ((0, 10), 10, Stepper.TOGGLE, Stepper.TOGGLE_UP, Stepper.TOGGLE_DOWN),
        ((0, 10), 10, Stepper.TOGGLE, Stepper.TOGGLE_DOWN, Stepper.TOGGLE_DOWN),
        ((0, 10), 0, Stepper.TOGGLE, Stepper.TOGGLE_DOWN, Stepper.TOGGLE_UP),
        ((0, 10), 0, Stepper.TOGGLE, Stepper.TOGGLE_UP, Stepper.TOGGLE_UP),
    ],
)
def test_minmax_stepper_get_direction(
    minmax, value, direction, previous_direction, expected_direction
):
    stepper = MinMaxStepper(*minmax, 10)
    stepper.previous_direction = previous_direction

    # SUT
    new_direction = stepper.get_direction(value, direction)

    # Checks
    assert new_direction == expected_direction


@pytest.mark.parametrize(
    "minmax, value, steps, direction, expected_value, expected_exceeded",
    [
        ((0, 10), 5, 10, Stepper.DOWN, 4, False),
        ((0, 10), 5, 10, Stepper.UP, 6, False),
        ((0, 10), 1, 10, Stepper.DOWN, 0, True),
        ((0, 10), 9, 10, Stepper.UP, 10, True),
        ((0, 10), 0, 10, Stepper.DOWN, 0, True),
        ((0, 10), 10, 10, Stepper.UP, 10, True),
        ((0, 10), -1, 10, Stepper.DOWN, 0, True),
        ((0, 10), 11, 10, Stepper.UP, 10, True),
        ((0, 10), 6, 5, Stepper.DOWN, 4, False),
        ((0, 10), 4, 5, Stepper.UP, 6, False),
    ],
)
def test_minmax_stepper_step(
    minmax, value, steps, direction, expected_value, expected_exceeded
):
    stepper = MinMaxStepper(*minmax, steps)

    # SUT
    new_value, exceeded = stepper.step(value, direction)

    # Checks
    assert new_value == expected_value
    assert exceeded == expected_exceeded
