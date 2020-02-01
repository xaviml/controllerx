import pytest

from core import integration as integration_module
from core.controller import Controller
from tests.utils import IntegrationMock, hass_mock


@pytest.fixture
def controller(hass_mock):
    c = Controller()
    c.args = {}
    return c


def test_get_integrations(controller):
    integrations = integration_module.get_integrations(controller)
    integrations.sort(key=lambda integration: integration.name)
    inteagration_names = [i.name for i in integrations]
    assert inteagration_names == sorted(["z2m", "zha", "deconz"])
