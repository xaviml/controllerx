from core.stepper import Stepper, MinMax


class CircularStepper(Stepper):
    def __init__(self, min_, max_, steps):
        super().__init__()
        # We add +1 to make the max be included
        self.minmax = MinMax(min_, max_ + 1)
        self.steps = steps

    def step(self, value, direction):
        sign = self.sign(direction)
        max_ = self.minmax.max
        min_ = self.minmax.min
        step = (max_ - min_) // self.steps
        return (value + step * sign) % (max_ - min_) + min_, False
