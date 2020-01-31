from collections import namedtuple

MinMax = namedtuple("MinMax", "min max")


class Stepper:

    UP = "up"
    DOWN = "down"

    sign_mapping = {UP: 1, DOWN: -1}

    def __init__(self, minmax_dict, steps):
        self.minmax_dict = minmax_dict
        self.steps = steps

    @staticmethod
    def sign(direction):
        return Stepper.sign_mapping[direction]

    def step(self, value, attribute, direction):
        """
        This function updates the value according to the steps
        that needs to take and returns the new value and True
        if the step exceeds the boundaries.
        """
        sign = Stepper.sign(direction)
        max_ = self.minmax_dict[attribute].max
        min_ = self.minmax_dict[attribute].min
        step = (max_ - min_) // self.steps

        new_value = value + sign * step

        if min_ < new_value < max_:
            return new_value, False
        else:
            new_value = max(min_, min(new_value, max_))
            return new_value, True
