from tests.utils import hass_mock, get_instances
import devices as devices_module
from core import Controller
from core import type as type_module


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


def check_mapping(mapping, all_possible_actions, device):
    if mapping is None:
        return
    for k, v in mapping.items():
        if type(v) != str:
            raise ValueError(
                "The value from the mapping should be a string, matching "
                + "one of the actions from the controller. "
                + f"The possible actions are: {all_possible_actions}. "
                + f"Device class: {device.__class__.__name__}"
            )

        if v not in all_possible_actions:
            raise ValueError(
                f"{v} not found in the list of possible action from the controller. "
                + f"The possible actions are: {all_possible_actions}"
            )


def test_devices(hass_mock):
    devices = get_instances(
        devices_module.__file__, devices_module.__package__, Controller
    )
    for device in devices:
        type_actions_mapping = device.get_type_actions_mapping()
        if type_actions_mapping is None:
            continue
        possible_actions = list(type_actions_mapping.keys())
        mappings = device.get_z2m_actions_mapping()
        check_mapping(mappings, possible_actions, device)
        mappings = device.get_deconz_actions_mapping()
        check_mapping(mappings, possible_actions, device)
        mappings = device.get_zha_actions_mapping()
        check_mapping(mappings, possible_actions, device)
