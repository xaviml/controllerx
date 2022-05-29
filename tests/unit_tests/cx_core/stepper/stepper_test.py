import pytest
from cx_const import Number, StepperDir
from cx_core.stepper import MinMax, Stepper, StepperOutput


class FakeStepper(Stepper):
    def __init__(self) -> None:
        super().__init__(MinMax(0, 1), 1)

    def step(self, value: Number, direction: str) -> StepperOutput:
        return StepperOutput(next_value=0, next_direction=None)


@pytest.mark.parametrize(
    "direction_input, previous_direction, expected_direction",
    [
        (StepperDir.UP, StepperDir.UP, StepperDir.UP),
        (StepperDir.DOWN, StepperDir.DOWN, StepperDir.DOWN),
        (StepperDir.UP, StepperDir.DOWN, StepperDir.UP),
        (StepperDir.DOWN, StepperDir.UP, StepperDir.DOWN),
        (StepperDir.TOGGLE, StepperDir.UP, StepperDir.DOWN),
        (StepperDir.TOGGLE, StepperDir.DOWN, StepperDir.UP),
    ],
)
def test_get_direction(
    direction_input: str, previous_direction: str, expected_direction: str
) -> None:
    stepper = FakeStepper()
    stepper.previous_direction = previous_direction

    direction_output = stepper.get_direction(0, direction_input)

    assert direction_output == expected_direction


@pytest.mark.parametrize(
    "direction_input, expected_sign",
    [
        (StepperDir.UP, 1),
        (StepperDir.DOWN, -1),
        (StepperDir.UP, 1),
        (StepperDir.DOWN, -1),
    ],
)
def test_sign(direction_input: str, expected_sign: int) -> None:
    stepper = FakeStepper()
    sign_output = stepper.sign(direction_input)
    assert sign_output == expected_sign


@pytest.mark.parametrize(
    "value, direction_input, expected_value",
    [
        (10, StepperDir.UP, 10),
        (0, StepperDir.DOWN, 0),
        (0, StepperDir.UP, 0),
        (2, StepperDir.DOWN, -2),
    ],
)
def test_apply_sign(
    value: Number, direction_input: str, expected_value: Number
) -> None:
    stepper = FakeStepper()
    value_output = stepper.apply_sign(value, direction_input)
    assert value_output == expected_value
