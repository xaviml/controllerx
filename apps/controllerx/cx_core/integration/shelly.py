from typing import Any

from appdaemon.plugins.hass.hassapi import Hass
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class ShellyIntegration(Integration):
    name = "shelly"

    def get_default_actions_mapping(self) -> DefaultActionsMapping | None:
        return self.controller.get_shelly_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        await Hass.listen_event(
            self.controller, self.event_callback, "shelly.click", device=controller_id
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict[str, Any]
    ) -> None:
        click_type = data["click_type"]
        channel = data["channel"]
        action = f"{click_type}_{channel}"
        await self.controller.handle_action(action, extra=data)
