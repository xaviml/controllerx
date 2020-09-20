from cx_core import Controller
from cx_core import type as type_module
from tests.test_utils import get_classes


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
    controller_types = get_classes(
        type_module.__file__, type_module.__package__, Controller, instantiate=True
    )
    for controller_type in controller_types:
        mappings = controller_type.get_type_actions_mapping()
        check_mapping(mappings)
