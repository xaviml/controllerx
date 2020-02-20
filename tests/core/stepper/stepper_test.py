import pytest

from core.stepper import Stepper


class FakeStepper(Stepper):
    def step(self, value, direction):
        pass


@pytest.mark.parametrize(
    "direction_input, previous_direction, expected_direction",
    [
        (Stepper.UP, Stepper.UP, Stepper.UP),
        (Stepper.DOWN, Stepper.DOWN, Stepper.DOWN),
        (Stepper.UP, Stepper.DOWN, Stepper.UP),
        (Stepper.DOWN, Stepper.UP, Stepper.DOWN),
        (Stepper.TOGGLE, Stepper.TOGGLE_UP, Stepper.TOGGLE_DOWN),
        (Stepper.TOGGLE, Stepper.TOGGLE_DOWN, Stepper.TOGGLE_UP),
    ],
)
def test_get_direction(direction_input, previous_direction, expected_direction):
    stepper = FakeStepper()
    stepper.previous_direction = previous_direction

    # SUT
    direction_output = stepper.get_direction(direction_input)

    # Checks
    assert direction_output == expected_direction


@pytest.mark.parametrize(
    "direction_input, expected_sign",
    [
        (Stepper.UP, 1),
        (Stepper.DOWN, -1),
        (Stepper.TOGGLE_UP, 1),
        (Stepper.TOGGLE_DOWN, -1),
    ],
)
def test_sign(direction_input, expected_sign):
    stepper = FakeStepper()

    # SUT
    sign_output = stepper.sign(direction_input)

    # Checks
    assert sign_output == expected_sign
