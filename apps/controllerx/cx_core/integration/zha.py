from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class ZHAIntegration(Integration):
    name = "zha"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_zha_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        Hass.listen_event(
            self.controller, self.callback, "zha_event", device_ieee=controller_id
        )

    def get_action(self, data: EventData) -> str:
        command = data["command"]
        args = data["args"]
        if isinstance(args, dict):
            args = args["args"]
        args = list(map(str, args))
        action = command
        if not (command == "stop" or command == "release"):
            if len(args) > 0:
                action += "_" + "_".join(args)
        return action

    async def callback(self, event_name: str, data: EventData, kwargs: dict) -> None:
        action = self.controller.get_zha_action(data)
        if action is None:
            # If there is no action extracted from the controller then
            # we extract with the standard function
            action = self.get_action(data)
        await self.controller.handle_action(action)
