import pytest

from core import MediaPlayerController, ReleaseHoldController
from tests.utils import hass_mock
from core.stepper import Stepper
from core.stepper.minmax_stepper import MinMaxStepper
from core.stepper.circular_stepper import CircularStepper


@pytest.fixture
def sut(hass_mock):
    c = MediaPlayerController()
    c.args = {}
    c.delay = 0
    return c
