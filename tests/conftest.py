import appdaemon.plugins.hass.hassapi as hass
import pytest

from cx_core.controller import Controller
from tests.test_utils import fake_async_function


@pytest.fixture(autouse=True)
def hass_mock(monkeypatch, mocker):
    """
    Fixture for set up the tests, mocking appdaemon functions
    """

    def fake_fn(*args, **kwargs):
        return None

    monkeypatch.setattr(hass.Hass, "__init__", fake_fn)
    monkeypatch.setattr(hass.Hass, "listen_event", fake_fn)
    monkeypatch.setattr(hass.Hass, "listen_state", fake_fn)
    monkeypatch.setattr(hass.Hass, "log", fake_fn)
    monkeypatch.setattr(hass.Hass, "call_service", fake_async_function())


@pytest.fixture(autouse=True)
def fake_controller(hass_mock):
    c = Controller()
    c.args = {}
    return c
