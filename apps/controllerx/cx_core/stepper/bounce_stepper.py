from typing import Tuple

from cx_const import Number
from cx_core.stepper import Stepper


class BounceStepper(Stepper):
    def step(self, value: Number, direction: str) -> Tuple[Number, bool]:
        raise NotImplementedError()
