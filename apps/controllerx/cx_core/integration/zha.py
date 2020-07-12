from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore

from cx_const import TypeActionsMapping
from cx_core.integration import Integration


class ZHAIntegration(Integration):
    def get_name(self):
        return "zha"

    def get_actions_mapping(self) -> Optional[TypeActionsMapping]:
        return self.controller.get_zha_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        Hass.listen_event(
            self.controller, self.callback, "zha_event", device_ieee=controller_id
        )

    def get_action(self, command: str, args):
        if isinstance(args, dict):
            args = args["args"]
        args = list(map(str, args))
        action = command
        if not (command == "stop" or command == "release"):
            if len(args) > 0:
                action += "_" + "_".join(args)
        return action

    async def callback(self, event_name: str, data: dict, kwargs: dict) -> None:
        command = data["command"]
        args = data["args"]
        action = self.controller.get_zha_action(command, args)
        if action is None:
            # If there is no action extracted from the controller then
            # we extract with the standard function
            action = self.get_action(command, args)
        await self.controller.handle_action(action)
