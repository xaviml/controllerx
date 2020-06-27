import abc
import importlib
import os
import pkgutil
from typing import Any, Dict, List, NewType, Optional, Type, Union

from cx_const import TypeActionsMapping


class Integration(abc.ABC):
    def __init__(self, controller, kwargs: Dict[str, Any]):
        self.name = self.get_name()
        self.controller = controller
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_actions_mapping(self) -> Optional[TypeActionsMapping]:
        raise NotImplementedError

    @abc.abstractmethod
    def listen_changes(self, controller_id: str) -> None:
        raise NotImplementedError


def _import_modules(file_dir: str, package: str) -> None:
    pkg_dir = os.path.dirname(file_dir)
    for (_, name, _) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module("." + name, package)


IntegrationSubType = NewType("IntegrationSubType", Integration)


def _all_integration_subclasses(
    cls_: Type[Union[Integration, IntegrationSubType]]
) -> List[Type[Integration]]:
    subclasses = set(cls_.__subclasses__()).union(
        [s for c in cls_.__subclasses__() for s in _all_integration_subclasses(c)]
    )
    return list(subclasses)


def get_integrations(controller, kwargs) -> List[Integration]:
    _import_modules(__file__, __package__)
    subclasses = _all_integration_subclasses(Integration)
    integrations = [cls_(controller, kwargs) for cls_ in subclasses]
    return integrations
