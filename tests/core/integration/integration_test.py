from cx_core import integration as integration_module


def test_get_integrations(fake_controller):
    integrations = integration_module.get_integrations(fake_controller, {})
    inteagration_names = {i.name for i in integrations}
    assert inteagration_names == {"z2m", "zha", "deconz", "state", "mqtt"}
