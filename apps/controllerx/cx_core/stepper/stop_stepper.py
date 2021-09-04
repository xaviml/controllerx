from cx_const import Number
from cx_core.stepper import Stepper, StepperOutput


class StopStepper(Stepper):
    def get_direction(self, value: Number, direction: str) -> str:
        value = self.min_max.clip(value)
        if direction == Stepper.TOGGLE and self.min_max.in_min_boundaries(value):
            self.previous_direction = Stepper.UP
            return self.previous_direction
        if direction == Stepper.TOGGLE and self.min_max.in_max_boundaries(value):
            self.previous_direction = Stepper.DOWN
            return self.previous_direction
        return super().get_direction(value, direction)

    def step(self, value: Number, direction: str) -> StepperOutput:
        value = self.min_max.clip(value)
        sign = Stepper.sign(direction)
        max_ = self.min_max.max
        min_ = self.min_max.min
        step = (max_ - min_) / self.steps

        new_value = value + sign * step
        new_value = round(new_value, 3)
        if self.min_max.is_between(new_value):
            return StepperOutput(new_value, next_direction=direction)
        else:
            new_value = self.min_max.clip(new_value)
            return StepperOutput(new_value, next_direction=None)
