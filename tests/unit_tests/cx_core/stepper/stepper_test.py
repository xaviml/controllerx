import pytest
from cx_const import Number
from cx_core.stepper import MinMax, Stepper, StepperOutput


class FakeStepper(Stepper):
    def __init__(self) -> None:
        super().__init__(MinMax(0, 1), 1)

    def step(self, value: Number, direction: str) -> StepperOutput:
        return StepperOutput(next_value=0, next_direction=None)


@pytest.mark.parametrize(
    "direction_input, previous_direction, expected_direction",
    [
        (Stepper.UP, Stepper.UP, Stepper.UP),
        (Stepper.DOWN, Stepper.DOWN, Stepper.DOWN),
        (Stepper.UP, Stepper.DOWN, Stepper.UP),
        (Stepper.DOWN, Stepper.UP, Stepper.DOWN),
        (Stepper.TOGGLE, Stepper.UP, Stepper.DOWN),
        (Stepper.TOGGLE, Stepper.DOWN, Stepper.UP),
    ],
)
def test_get_direction(
    direction_input: str, previous_direction: str, expected_direction: str
):
    stepper = FakeStepper()
    stepper.previous_direction = previous_direction

    direction_output = stepper.get_direction(0, direction_input)

    assert direction_output == expected_direction


@pytest.mark.parametrize(
    "direction_input, expected_sign",
    [
        (Stepper.UP, 1),
        (Stepper.DOWN, -1),
        (Stepper.UP, 1),
        (Stepper.DOWN, -1),
    ],
)
def test_sign(direction_input: str, expected_sign: int):
    stepper = FakeStepper()
    sign_output = stepper.sign(direction_input)
    assert sign_output == expected_sign
