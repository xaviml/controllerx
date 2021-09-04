from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class BounceStepper(Stepper):
    def step(self, value: Number, direction: str) -> StepperOutput:
        value = self.min_max.clip(value)
        sign = Stepper.sign(direction)
        max_ = self.min_max.max
        min_ = self.min_max.min
        step = (max_ - min_) / self.steps

        new_value = value + sign * step
        if self.min_max.is_between(new_value):
            return StepperOutput(round(new_value, 3), next_direction=direction)
        else:
            new_value = 2 * self.min_max.clip(new_value) - new_value
            return StepperOutput(
                round(new_value, 3), next_direction=Stepper.invert_direction(direction)
            )
