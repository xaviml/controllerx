import abc
from typing import TYPE_CHECKING, Any, Optional

from cx_const import DefaultActionsMapping
from cx_helper import get_classes

if TYPE_CHECKING:
    from cx_core.controller import Controller

EventData = dict[str, Any]


class Integration(abc.ABC):
    name: str
    controller: "Controller"
    kwargs: dict[str, Any]

    def __init__(self, controller: "Controller", kwargs: dict[str, Any]):
        self.controller = controller
        self.kwargs = kwargs

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return None

    @abc.abstractmethod
    async def listen_changes(self, controller_id: str) -> None:
        raise NotImplementedError


def get_integrations(
    controller: "Controller", kwargs: dict[str, Any]
) -> list[Integration]:
    integration_classes = get_classes(__file__, __package__, Integration)
    integrations = [cls_(controller, kwargs) for cls_ in integration_classes]
    return integrations
