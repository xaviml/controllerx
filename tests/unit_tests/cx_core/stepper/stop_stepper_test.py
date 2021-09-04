import pytest
from cx_core.stepper import MinMax, Stepper
from cx_core.stepper.stop_stepper import StopStepper
from typing_extensions import Literal


@pytest.mark.parametrize(
    "min_max, value, direction, previous_direction, expected_direction, expected_new_previous_direction",
    [
        (MinMax(0, 10), 10, Stepper.DOWN, None, Stepper.DOWN, None),
        (MinMax(0, 10), 11, Stepper.DOWN, None, Stepper.DOWN, None),
        (MinMax(0, 10), -1, Stepper.DOWN, None, Stepper.DOWN, None),
        (MinMax(0, 10), 5, Stepper.UP, None, Stepper.UP, None),
        (MinMax(0, 10), 5, Stepper.UP, None, Stepper.UP, None),
        (
            MinMax(0, 10),
            5,
            Stepper.TOGGLE,
            Stepper.DOWN,
            Stepper.UP,
            Stepper.UP,
        ),
        (
            MinMax(0, 10),
            5,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(0, 10),
            10,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(0, 10),
            10,
            Stepper.TOGGLE,
            Stepper.DOWN,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(0, 10),
            0,
            Stepper.TOGGLE,
            Stepper.DOWN,
            Stepper.UP,
            Stepper.UP,
        ),
        (
            MinMax(0, 10),
            0,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.UP,
            Stepper.UP,
        ),
        (
            MinMax(1, 255),
            255,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(1, 255),
            254,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(1, 255),
            253,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.DOWN,
            Stepper.DOWN,
        ),
        (
            MinMax(1, 255),
            1,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.UP,
            Stepper.UP,
        ),
        (
            MinMax(1, 255),
            5,
            Stepper.TOGGLE,
            Stepper.UP,
            Stepper.UP,
            Stepper.UP,
        ),
    ],
)
def test_stop_stepper_get_direction(
    min_max: MinMax,
    value: int,
    direction: str,
    previous_direction: str,
    expected_direction: str,
    expected_new_previous_direction: str,
):
    stepper = StopStepper(min_max, 10)
    stepper.previous_direction = previous_direction

    # SUT
    new_direction = stepper.get_direction(value, direction)

    # Checks
    assert new_direction == expected_direction
    assert stepper.previous_direction == expected_new_previous_direction


@pytest.mark.parametrize(
    "min_max, value, steps, direction, expected_value, expected_exceeded",
    [
        (MinMax(0, 10), 5, 10, Stepper.DOWN, 4, False),
        (MinMax(0, 10), 5, 10, Stepper.UP, 6, False),
        (MinMax(0, 10), 1, 10, Stepper.DOWN, 0, True),
        (MinMax(0, 10), 9, 10, Stepper.UP, 10, True),
        (MinMax(0, 10), 0, 10, Stepper.DOWN, 0, True),
        (MinMax(0, 10), 10, 10, Stepper.UP, 10, True),
        (MinMax(0, 10), -1, 10, Stepper.DOWN, 0, True),
        (MinMax(0, 10), 11, 10, Stepper.UP, 10, True),
        (MinMax(0, 10), 6, 5, Stepper.DOWN, 4, False),
        (MinMax(0, 10), 4, 5, Stepper.UP, 6, False),
    ],
)
def test_stop_stepper_step(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
    expected_exceeded: bool,
):
    stepper = StopStepper(min_max, steps)

    stepper_output = stepper.step(value, direction)

    assert stepper_output.next_value == expected_value
    assert stepper_output.exceeded == expected_exceeded
