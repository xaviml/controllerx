import pytest
import sys

sys.path.append("apps/controllerx")

from core.stepper import Stepper, MinMax


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
def test_stepper(minmax, value, steps, direction, expected_value, expected_exceeded):
    stepper = Stepper({"test_attribute": MinMax(*minmax)}, steps)

    # SUT
    new_value, exceeded = stepper.step(value, "test_attribute", direction)

    # Checks
    assert new_value == expected_value
    assert exceeded == expected_exceeded
