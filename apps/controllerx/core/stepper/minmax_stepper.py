from core.stepper import Stepper, MinMax


class MinMaxStepper(Stepper):
    def __init__(self, min_, max_, steps):
        super().__init__()
        self.minmax = MinMax(min_, max_)
        self.steps = steps

    def step(self, value, direction):
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
            new_value = max(min_, min(new_value, max_))
            return new_value, True
