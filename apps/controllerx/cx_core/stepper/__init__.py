import abc
from typing import Optional

from attr import dataclass
from cx_const import Number, StepperDir


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


@dataclass
class StepperOutput:
    next_value: Number
    next_direction: Optional[str]

    @property
    def exceeded(self) -> bool:
        return self.next_direction is None


class Stepper(abc.ABC):
    sign_mapping = {StepperDir.UP: 1, StepperDir.DOWN: -1}

    previous_direction: str = StepperDir.DOWN
    min_max: MinMax
    steps: Number

    @staticmethod
    def invert_direction(direction: str) -> str:
        return StepperDir.UP if direction == StepperDir.DOWN else StepperDir.DOWN

    @staticmethod
    def sign(direction: str) -> int:
        return Stepper.sign_mapping[direction]

    def __init__(self, min_max: MinMax, steps: Number) -> None:
        self.min_max = min_max
        self.steps = steps

    def get_direction(self, value: Number, direction: str) -> str:
        if direction == StepperDir.TOGGLE:
            direction = Stepper.invert_direction(self.previous_direction)
            self.previous_direction = direction
        return direction

    @abc.abstractmethod
    def step(self, value: Number, direction: str) -> StepperOutput:
        """
        This function updates the value according to the steps
        that needs to take and returns the new value together with
        the new direction it will need to go. If next_direction is
        None, the loop will stop executing.
        """
        raise NotImplementedError
