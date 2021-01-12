import abc
import importlib
import os
import pkgutil
from typing import TYPE_CHECKING, Any, Dict, List, NewType, Optional, Type, Union

from cx_const import DefaultActionsMapping

if TYPE_CHECKING:
    from cx_core.controller import Controller

EventData = Dict[str, Any]


class Integration(abc.ABC):

    name: str
    controller: "Controller"
    kwargs: Dict[str, Any]

    def __init__(self, controller: "Controller", kwargs: Dict[str, Any]):
        self.controller = controller
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
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
    return list(subclasses)  # type: ignore


def get_integrations(controller, kwargs) -> List[Integration]:
    _import_modules(__file__, __package__)
    subclasses = _all_integration_subclasses(Integration)
    integrations = [cls_(controller, kwargs) for cls_ in subclasses]
    return integrations
