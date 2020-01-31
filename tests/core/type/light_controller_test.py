import pytest
import sys

sys.path.append("apps/controllerx")

from core import LightController, ReleaseHoldController
from ...utils import hass_mock


@pytest.fixture
def sut(hass_mock):
    c = LightController()
    c.args = {}
    c.delay = 0
    return c


@pytest.mark.parametrize(
    "light_input, light_output",
    [
        ("light.kitchen", {"name": "light.kitchen", "color_mode": "auto"}),
        (
            {"name": "light.kitchen", "color_mode": "auto"},
            {"name": "light.kitchen", "color_mode": "auto"},
        ),
        ({"name": "light.kitchen"}, {"name": "light.kitchen", "color_mode": "auto"}),
        (
            {"name": "light.kitchen", "color_mode": "color_temp"},
            {"name": "light.kitchen", "color_mode": "color_temp"},
        ),
    ],
)
def test_initialize(sut, mocker, light_input, light_output):
    super_initialize_stub = mocker.patch.object(ReleaseHoldController, "initialize")

    sut.args["light"] = light_input
    sut.initialize()

    super_initialize_stub.assert_called_once()
    assert sut.light == light_output
