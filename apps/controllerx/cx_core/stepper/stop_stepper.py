from typing import Tuple

from cx_const import Number
from cx_core.stepper import Stepper


class StopStepper(Stepper):
    def get_direction(self, value: Number, direction: str) -> str:
        value = self.min_max.clip(value)
        if direction == Stepper.TOGGLE and self.min_max.in_min_boundaries(value):
            self.previous_direction = Stepper.TOGGLE_UP
            return self.previous_direction
        if direction == Stepper.TOGGLE and self.min_max.in_max_boundaries(value):
            self.previous_direction = Stepper.TOGGLE_DOWN
            return self.previous_direction
        return super().get_direction(value, direction)

    def step(self, value: Number, direction: str) -> Tuple[Number, bool]:
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        sign = self.sign(direction)
        max_ = self.min_max.max
        min_ = self.min_max.min
        step = (max_ - min_) / self.steps

        new_value = value + sign * step

        if min_ < new_value < max_:
            return new_value, False
        else:
            new_value = self.min_max.clip(new_value)
            return new_value, True
