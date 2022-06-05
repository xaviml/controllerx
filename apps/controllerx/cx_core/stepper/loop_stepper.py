from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class LoopStepper(Stepper):
    def step(self, value: Number, direction: str) -> StepperOutput:
        value = self.min_max.clip(value)
        # We add +1 to include `max`
        max_ = self.min_max.max
        min_ = self.min_max.min
        step = (max_ - min_) / self.steps

        new_value = (
            ((value + Stepper.apply_sign(step, direction)) - min_) % (max_ - min_)
        ) + min_
        new_value = round(new_value, 3)
        return StepperOutput(new_value, next_direction=direction)
