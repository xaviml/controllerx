import sys

sys.path.append("apps/controllerx")
from core.controller import Controller
import appdaemon.plugins.hass.hassapi as hass

import pytest


class IntegrationMock:
    def __init__(self, name, controller, mocker):
        self.name = name
        self.controller = controller
        self.get_actions_mapping = mocker.stub(name="get_actions_mapping")
        self.listen_changes = mocker.stub(name="listen_changes")
        super().__init__()


@pytest.fixture
def hass_mock(monkeypatch, mocker):
    """
    Fixture for set up the tests, mocking appdaemon functions
    """
    fake_fn = lambda *args, **kwargs: None
    monkeypatch.setattr(hass.Hass, "__init__", fake_fn)
    monkeypatch.setattr(hass.Hass, "listen_event", fake_fn)
    monkeypatch.setattr(hass.Hass, "listen_state", fake_fn)
    monkeypatch.setattr(hass.Hass, "log", fake_fn)
    monkeypatch.setattr(hass.Hass, "call_service", fake_fn)

    c = Controller()
    c.args = {}
    return
