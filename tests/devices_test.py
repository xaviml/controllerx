import importlib
import os
import pkgutil

from tests.utils import hass_mock
import devices as devices_module
from core import Controller


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


def get_devices():
    _import_modules(devices_module.__file__, devices_module.__package__)
    subclasses = _all_subclasses(Controller)
    devices = [cls_() for cls_ in subclasses if len(cls_.__subclasses__()) == 0]
    return devices


def check_mapping(mapping):
    if mapping is None:
        return
    for k, v in mapping.items():
        if not (callable(v) or type(v) == tuple):
            raise ValueError("The value mapping should be a callable or a tuple")
        if type(v) == "tuple":
            if len(v) == 0:
                raise ValueError(
                    "The tuple should contain at least 1 element, the function"
                )
            fn, *args = v
            if not callable(fn):
                raise ValueError("The first element of the tuple should be a callable")


def test_devices(hass_mock):
    devices = get_devices()
    for device in devices:
        mappings = device.get_z2m_actions_mapping()
        check_mapping(mappings)
        mappings = device.get_deconz_actions_mapping()
        check_mapping(mappings)
        mappings = device.get_zha_actions_mapping()
        check_mapping(mappings)
