from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class LutronIntegration(Integration):
    name = "lutron_caseta"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_lutron_caseta_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        await Hass.listen_event(
            self.controller,
            self.callback,
            "lutron_caseta_button_event",
            serial=controller_id,
        )

    async def callback(self, event_name: str, data: EventData, kwargs: dict) -> None:
        button = data["button_number"]
        action_type = data["action"]
        action = f"button_{button}_{action_type}"
        await self.controller.handle_action(action, extra=data)
