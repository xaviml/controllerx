from typing import Any, Dict, Optional

from cx_core.action_type.base import ActionType
from cx_core.integration import EventData


class CallServiceActionType(ActionType):
    service: str
    entity_id: Optional[str]
    data: Dict[str, Any]

    def initialize(self, **kwargs) -> None:
        self.service = kwargs["service"]
        self.entity_id = kwargs.get("entity_id")
        self.data = kwargs.get("data", {})

    async def run(self, extra: Optional[EventData] = None) -> None:
        if self.entity_id:
            if "entity_id" in self.data:
                del self.data["entity_id"]
            await self.controller.call_service(
                self.service, entity_id=self.entity_id, **self.data
            )
        else:
            await self.controller.call_service(self.service, **self.data)

    def __str__(self) -> str:
        return f"Service ({self.service})"
