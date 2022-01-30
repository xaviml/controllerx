from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class HomematicIntegration(Integration):
    name = "homematic"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_homematic_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        await Hass.listen_event(
            self.controller,
            self.event_callback,
            "homematic.keypress",
            name=controller_id,
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict
    ) -> None:
        param = data["param"]
        channel = data["channel"]
        action = f"{param}_{channel}"
        await self.controller.handle_action(action, extra=data)
