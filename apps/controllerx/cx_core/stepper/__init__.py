import abc
from typing import Tuple

from cx_const import Number


class MinMax:
    def __init__(self, min: Number, max: Number, margin: float = 0.05) -> None:
        self._min = min
        self._max = max
        self.margin_dist = (max - min) * margin

    @property
    def min(self) -> Number:
        return self._min

    @property
    def max(self) -> Number:
        return self._max

    def is_min(self, value: Number) -> bool:
        return self._min == value

    def is_max(self, value: Number) -> bool:
        return self._max == value

    def is_between(self, value: Number) -> bool:
        return self._min < value < self._max

    def in_min_boundaries(self, value: Number) -> bool:
        return self._min <= value <= (self._min + self.margin_dist)

    def in_max_boundaries(self, value: Number) -> bool:
        return (self._max - self.margin_dist) <= value <= self._max

    def clip(self, value: Number) -> Number:
        return max(self._min, min(value, self._max))

    def __repr__(self) -> str:
        return f"MinMax({self.min}, {self.max})"


class Stepper(abc.ABC):
    UP = "up"
    DOWN = "down"
    TOGGLE_UP = "toggle_up"
    TOGGLE_DOWN = "toggle_down"
    TOGGLE = "toggle"
    sign_mapping = {UP: 1, DOWN: -1, TOGGLE_UP: 1, TOGGLE_DOWN: -1}

    previous_direction: str = TOGGLE_DOWN
    min_max: MinMax
    steps: Number

    def __init__(self, min_max: MinMax, steps: Number) -> None:
        self.min_max = min_max
        self.steps = steps

    def get_direction(self, value: Number, direction: str) -> str:
        if direction == Stepper.TOGGLE:
            direction = (
                Stepper.TOGGLE_UP
                if self.previous_direction == Stepper.TOGGLE_DOWN
                else Stepper.TOGGLE_DOWN
            )
            self.previous_direction = direction
        return direction

    def sign(self, direction: str) -> int:
        return Stepper.sign_mapping[direction]

    @abc.abstractmethod
    def step(self, value: Number, direction: str) -> Tuple[Number, bool]:
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        raise NotImplementedError
