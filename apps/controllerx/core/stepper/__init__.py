import abc
from collections import namedtuple

MinMax = namedtuple("MinMax", "min max")


class Stepper(abc.ABC):
    UP = "up"
    DOWN = "down"
    TOGGLE_UP = "toggle_up"
    TOGGLE_DOWN = "toggle_down"
    TOGGLE = "toggle"
    sign_mapping = {UP: 1, DOWN: -1, TOGGLE_UP: 1, TOGGLE_DOWN: -1}

    def __init__(self):
        self.previous_direction = Stepper.TOGGLE_DOWN

    def get_direction(self, direction):
        if direction == Stepper.TOGGLE:
            direction = (
                Stepper.TOGGLE_UP
                if self.previous_direction == Stepper.TOGGLE_DOWN
                else Stepper.TOGGLE_DOWN
            )
            self.previous_direction = direction
        return direction

    def sign(self, direction):
        return Stepper.sign_mapping[direction]

    @abc.abstractmethod
    def step(self, value, direction):
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        pass
