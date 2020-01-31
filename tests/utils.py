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
    monkeypatch.setattr(hass.Hass, "__init__", lambda self: None)
    monkeypatch.setattr(hass.Hass, "listen_event", lambda self, callback, entity: None)
    monkeypatch.setattr(hass.Hass, "listen_state", lambda self, callback, entity: None)
    monkeypatch.setattr(hass.Hass, "log", lambda self, message, level: None)

    c = Controller()
    c.args = {}
    return
