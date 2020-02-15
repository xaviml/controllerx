import importlib
import os
import pkgutil
import sys

import appdaemon.plugins.hass.hassapi as hass
import pytest

sys.path.append("apps/controllerx")
from core.controller import Controller


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


@pytest.fixture
def fake_controller(hass_mock):
    c = Controller()
    c.args = {}
    return c


def _import_modules(file_dir, package):
    pkg_dir = os.path.dirname(file_dir)
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        if ispkg:
            _import_modules(pkg_dir + "/" + name + "/__init__.py", package + "." + name)
        else:
            importlib.import_module("." + name, package)


def _all_subclasses(cls):
    return list(
        set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
        )
    )


def get_instances(file_, package_, class_):
    _import_modules(
        file_, package_,
    )
    subclasses = _all_subclasses(class_)
    devices = [cls_() for cls_ in subclasses if len(cls_.__subclasses__()) == 0]
    return devices
