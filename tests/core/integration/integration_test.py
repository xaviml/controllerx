import pytest

from core import integration as integration_module
from core.controller import Controller
from tests.utils import IntegrationMock, fake_controller, hass_mock


def test_get_integrations(fake_controller):
    integrations = integration_module.get_integrations(fake_controller, {})
    integrations.sort(key=lambda integration: integration.name)
    inteagration_names = [i.name for i in integrations]
    assert inteagration_names == sorted(["z2m", "zha", "deconz"])
