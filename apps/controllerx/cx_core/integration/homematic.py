from typing import TYPE_CHECKING, Any, Optional

from appdaemon.plugins.hass.hassapi import Hass
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration

if TYPE_CHECKING:
    from cx_core.controller import Controller


class HomematicIntegration(Integration):
    name = "homematic"
    _registered_controller_ids: set[str]

    def __init__(self, controller: "Controller", kwargs: dict[str, Any]):
        self._registered_controller_ids = set()
        super().__init__(controller, kwargs)

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_homematic_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        self._registered_controller_ids.add(controller_id)
        await Hass.listen_event(
            self.controller, self.event_callback, "homematic.keypress"
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict[str, Any]
    ) -> None:
        if data["name"] not in self._registered_controller_ids:
            return
        param = data["param"]
        channel = data["channel"]
        action = f"{param}_{channel}"
        await self.controller.handle_action(action, extra=data)
