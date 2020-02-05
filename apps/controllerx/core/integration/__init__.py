import abc
import os
import pkgutil
import importlib


def _import_modules(file_dir, package):
    pkg_dir = os.path.dirname(file_dir)
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module("." + name, package)


def get_integrations(controller):
    _import_modules(__file__, __package__)
    subclasses = [c for c in Integration.__subclasses__()]
    integrations = [
        cls_(controller) for cls_ in subclasses if len(cls_.__subclasses__()) == 0
    ]
    return integrations


class Integration(abc.ABC):
    def __init__(self, name, controller):
        self.name = name
        self.controller = controller

    @abc.abstractmethod
    def get_actions_mapping(self, controller_id):
        pass

    @abc.abstractmethod
    def listen_changes(self):
        pass
