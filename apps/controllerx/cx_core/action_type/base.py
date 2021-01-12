from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

from cx_core.integration import EventData

if TYPE_CHECKING:
    from cx_core import Controller


class ActionType(ABC):
    controller: "Controller"

    def __init__(self, controller: "Controller", action: Dict[str, Any]) -> None:
        self.controller = controller
        self.initialize(**action)

    def initialize(self, **kwargs) -> None:
        pass

    @abstractmethod
    async def run(self, extra: Optional[EventData] = None) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
