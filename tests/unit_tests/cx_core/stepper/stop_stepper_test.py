from typing import Literal

import pytest
from cx_const import StepperDir
from cx_core.stepper import MinMax
from cx_core.stepper.stop_stepper import StopStepper


@pytest.mark.parametrize(
    "min_max, value, direction, previous_direction, expected_direction, expected_new_previous_direction",
    [
        (MinMax(0, 10), 10, StepperDir.DOWN, None, StepperDir.DOWN, None),
        (MinMax(0, 10), 11, StepperDir.DOWN, None, StepperDir.DOWN, None),
        (MinMax(0, 10), -1, StepperDir.DOWN, None, StepperDir.DOWN, None),
        (MinMax(0, 10), 5, StepperDir.UP, None, StepperDir.UP, None),
        (MinMax(0, 10), 5, StepperDir.UP, None, StepperDir.UP, None),
        (
            MinMax(0, 10),
            5,
            StepperDir.TOGGLE,
            StepperDir.DOWN,
            StepperDir.UP,
            StepperDir.UP,
        ),
        (
            MinMax(0, 10),
            5,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(0, 10),
            10,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(0, 10),
            10,
            StepperDir.TOGGLE,
            StepperDir.DOWN,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(0, 10),
            0,
            StepperDir.TOGGLE,
            StepperDir.DOWN,
            StepperDir.UP,
            StepperDir.UP,
        ),
        (
            MinMax(0, 10),
            0,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.UP,
            StepperDir.UP,
        ),
        (
            MinMax(1, 255),
            255,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(1, 255),
            254,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(1, 255),
            253,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.DOWN,
            StepperDir.DOWN,
        ),
        (
            MinMax(1, 255),
            1,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.UP,
            StepperDir.UP,
        ),
        (
            MinMax(1, 255),
            5,
            StepperDir.TOGGLE,
            StepperDir.UP,
            StepperDir.UP,
            StepperDir.UP,
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
) -> None:
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
        (MinMax(0, 10), 5, 10, StepperDir.DOWN, 4, False),
        (MinMax(0, 10), 5, 10, StepperDir.UP, 6, False),
        (MinMax(0, 10), 1, 10, StepperDir.DOWN, 0, True),
        (MinMax(0, 10), 9, 10, StepperDir.UP, 10, True),
        (MinMax(0, 10), 0, 10, StepperDir.DOWN, 0, True),
        (MinMax(0, 10), 10, 10, StepperDir.UP, 10, True),
        (MinMax(0, 10), -1, 10, StepperDir.DOWN, 0, True),
        (MinMax(0, 10), 11, 10, StepperDir.UP, 10, True),
        (MinMax(0, 10), 6, 5, StepperDir.DOWN, 4, False),
        (MinMax(0, 10), 4, 5, StepperDir.UP, 6, False),
    ],
)
def test_stop_stepper_step(
    min_max: MinMax,
    value: int,
    steps: int,
    direction: Literal["up", "down"],
    expected_value: int,
    expected_exceeded: bool,
) -> None:
    stepper = StopStepper(min_max, steps)

    stepper_output = stepper.step(value, direction)

    assert stepper_output.next_value == expected_value
    assert stepper_output.exceeded == expected_exceeded
