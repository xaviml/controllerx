from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class BounceStepper(Stepper):
    def step(self, value: Number, direction: str) -> StepperOutput:
        value = self.min_max.clip(value)
        step = self._compute_step()

        new_value = value + Stepper.apply_sign(step, direction)
        if self.min_max.is_between(new_value):
            return StepperOutput(round(new_value, 3), next_direction=direction)
        else:
            new_value = 2 * self.min_max.clip(new_value) - new_value
            return StepperOutput(
                round(new_value, 3), next_direction=Stepper.invert_direction(direction)
            )
