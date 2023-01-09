from cx_const import Number, StepperDir
from cx_core.stepper import MinMax, Stepper, StepperOutput


class IndexLoopStepper(Stepper):
    def __init__(
        self,
        size: int,
        previous_direction: str = StepperDir.DOWN,
        relative_steps: bool = True,
    ) -> None:
        super().__init__(
            MinMax(0, size - 1),
            size,
            previous_direction,
            relative_steps,
        )

    def step(self, value: Number, direction: str) -> StepperOutput:
        value = self.min_max.clip(value)
        sign = self.sign(direction)
        # We add +1 to make the max be included
        max_ = int(self.min_max.max) + 1
        min_ = int(self.min_max.min)
        if self.relative_steps:
            step = (max_ - min_) // self.steps
        else:
            step = self.steps

        new_value = (int(value) + step * sign) % (max_ - min_) + min_
        return StepperOutput(new_value, next_direction=direction)
