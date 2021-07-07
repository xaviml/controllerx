from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass
from cx_const import DefaultActionsMapping  # type:ignore
from cx_core.integration import EventData, Integration

LISTENS_TO_ID = "id"
LISTENS_TO_UNIQUE_ID = "unique_id"


class DeCONZIntegration(Integration):
    name = "deconz"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_deconz_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        listens_to = self.kwargs.get("listen_to", LISTENS_TO_ID)
        if listens_to not in (LISTENS_TO_ID, LISTENS_TO_UNIQUE_ID):
            raise ValueError(
                "`listens_to` for deCONZ integration should either be `id` or `unique_id`"
            )
        await Hass.listen_event(
            self.controller,
            self.event_callback,
            "deconz_event",
            **{listens_to: controller_id}
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict
    ) -> None:
        type_ = self.kwargs.get("type", "event")
        await self.controller.handle_action(data[type_], extra=data)
