from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class BounceStepper(Stepper):
    def step(self, value: Number, direction: str) -> StepperOutput:
        raise NotImplementedError()
