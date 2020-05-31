from typing import Tuple

from core.stepper import MinMax, Stepper


class MinMaxStepper(Stepper):
    def __init__(self, min_: int, max_: int, steps: int) -> None:
        super().__init__()
        self.minmax = MinMax(min_, max_)
        self.steps = steps

    def get_direction(self, value: float, direction: str) -> str:
        value = self.minmax.clip(value)
        if self.minmax.is_between(value):
            return super().get_direction(value, direction)

        if direction == Stepper.TOGGLE:
            if self.minmax.is_min(value):
                return Stepper.TOGGLE_UP
            elif self.minmax.is_max(value):  # Then is the max value
                return Stepper.TOGGLE_DOWN

        return direction

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
