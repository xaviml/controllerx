import abc
import os
import pkgutil
import importlib


def _import_modules(file_dir, package):
    pkg_dir = os.path.dirname(file_dir)
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module("." + name, package)


def _all_subclasses(cls):
    return list(
        set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
        )
    )


def get_integrations(controller, kwargs):
    _import_modules(__file__, __package__)
    subclasses = _all_subclasses(Integration)
    integrations = [cls_(controller, kwargs) for cls_ in subclasses]
    return integrations


class Integration(abc.ABC):
    def __init__(self, controller, kwargs):
        self.name = self.get_name()
        self.controller = controller
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_actions_mapping(self, controller_id):
        pass

    @abc.abstractmethod
    def listen_changes(self):
        pass
