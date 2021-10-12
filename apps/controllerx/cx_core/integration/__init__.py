import abc
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from cx_const import DefaultActionsMapping
from cx_helper import get_classes

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
    async def listen_changes(self, controller_id: str) -> None:
        raise NotImplementedError


def get_integrations(controller, kwargs) -> List[Integration]:
    integration_classes = get_classes(__file__, __package__, Integration)
    integrations = [cls_(controller, kwargs) for cls_ in integration_classes]
    return integrations
