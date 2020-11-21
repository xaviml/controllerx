from cx_core import integration as integration_module
from cx_core.controller import Controller


def test_get_integrations(fake_controller: Controller):
    integrations = integration_module.get_integrations(fake_controller, {})
    inteagration_names = {i.name for i in integrations}
    assert inteagration_names == {"z2m", "zha", "deconz", "state", "mqtt"}
