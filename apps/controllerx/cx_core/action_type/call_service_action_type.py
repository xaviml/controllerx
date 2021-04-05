from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from cx_core.action_type.base import ActionType
from cx_core.integration import EventData

if TYPE_CHECKING:
    from cx_core.type_controller import TypeController


class CallServiceActionType(ActionType):
    service: str
    # Priority order for entity_id:
    # - Inside data
    # - In the same level as "service"
    # - From the main config if the domain matches
    entity_id: Optional[str]
    data: Dict[str, Any]

    def initialize(self, **kwargs) -> None:
        self.service = kwargs["service"]
        self.data = kwargs.get("data", {})

        self.entity_id = self.data.get("entity_id") or kwargs.get("entity_id")
        if (
            self.entity_id is None
            and self._check_controller_isinstance_type_controller()
        ):
            type_controller = cast("TypeController", self.controller)
            if self._get_service_domain(self.service) in type_controller.domains:
                self.entity_id = type_controller.entity.name
        if "entity_id" in self.data:
            del self.data["entity_id"]

    def _check_controller_isinstance_type_controller(self):
        # This is checked dynamically without the isinstance to avoid
        # circular dependency
        class_names = [c.__name__ for c in type(self.controller).mro()]
        return "TypeController" in class_names

    def _get_service_domain(self, service: str) -> str:
        return service.replace(".", "/").split("/")[0]

    async def run(self, extra: Optional[EventData] = None) -> None:
        if self.entity_id:
            await self.controller.call_service(
                self.service, entity_id=self.entity_id, **self.data
            )
        else:
            await self.controller.call_service(self.service, **self.data)

    def __str__(self) -> str:
        return f"Service ({self.service})"
