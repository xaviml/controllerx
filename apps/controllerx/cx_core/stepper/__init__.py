import abc
from typing import Tuple, Union


class MinMax:
    def __init__(self, min_: float, max_: float, margin=0.05) -> None:
        self._min = min_
        self._max = max_
        self.margin_dist = (max_ - min_) * margin

    @property
    def min(self) -> float:
        return self._min

    @property
    def max(self) -> float:
        return self._max

    def is_min(self, value: float) -> bool:
        return self._min == value

    def is_max(self, value: float) -> bool:
        return self._max == value

    def is_between(self, value: float) -> bool:
        return self._min < value < self._max

    def in_min_boundaries(self, value: float) -> bool:
        return self._min <= value <= (self._min + self.margin_dist)

    def in_max_boundaries(self, value: float) -> bool:
        return (self._max - self.margin_dist) <= value <= self._max

    def clip(self, value: float) -> float:
        return max(self._min, min(value, self._max))


class Stepper(abc.ABC):
    UP = "up"
    DOWN = "down"
    TOGGLE_UP = "toggle_up"
    TOGGLE_DOWN = "toggle_down"
    TOGGLE = "toggle"
    sign_mapping = {UP: 1, DOWN: -1, TOGGLE_UP: 1, TOGGLE_DOWN: -1}

    def __init__(self) -> None:
        self.previous_direction = Stepper.TOGGLE_DOWN

    def get_direction(self, value: float, direction: str) -> str:
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
    def step(self, value: float, direction: str) -> Tuple[Union[int, float], bool]:
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        raise NotImplementedError
