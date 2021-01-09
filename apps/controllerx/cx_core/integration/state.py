from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from cx_const import DefaultActionsMapping
from cx_core.integration import Integration


class StateIntegration(Integration):
    name = "state"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_z2m_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        attribute = self.kwargs.get("attribute", None)
        Hass.listen_state(
            self.controller, self.state_callback, controller_id, attribute=attribute
        )

    async def state_callback(
        self, entity: Optional[str], attribute: Optional[str], old, new, kwargs
    ) -> None:
        await self.controller.handle_action(new)
