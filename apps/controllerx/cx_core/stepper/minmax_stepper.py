from typing import Tuple

from cx_core.stepper import MinMax, Stepper


class MinMaxStepper(Stepper):
    def __init__(self, min_: int, max_: int, steps: int) -> None:
        super().__init__()
        self.minmax = MinMax(min_, max_)
        self.steps = steps

    def get_direction(self, value: float, direction: str) -> str:
        value = self.minmax.clip(value)
        if direction == Stepper.TOGGLE and self.minmax.in_min_boundaries(value):
            self.previous_direction = Stepper.TOGGLE_UP
            return self.previous_direction
        if direction == Stepper.TOGGLE and self.minmax.in_max_boundaries(value):
            self.previous_direction = Stepper.TOGGLE_DOWN
            return self.previous_direction
        return super().get_direction(value, direction)

    def step(self, value: float, direction: str) -> Tuple[float, bool]:
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        sign = self.sign(direction)
        max_ = self.minmax.max
        min_ = self.minmax.min
        step = (max_ - min_) / self.steps

        new_value = value + sign * step

        if min_ < new_value < max_:
            return new_value, False
        else:
            new_value = self.minmax.clip(new_value)
            return new_value, True
