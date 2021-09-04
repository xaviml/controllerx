from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class LoopStepper(Stepper):
    def step(self, value: Number, direction: str) -> StepperOutput:
        sign = self.sign(direction)
        # We add +1 to include `max`
        max_ = self.min_max.max + 1
        min_ = self.min_max.min
        step = (max_ - min_) // self.steps
        new_value = (value + step * sign) % (max_ - min_) + min_
        return StepperOutput(new_value, next_direction=direction)
