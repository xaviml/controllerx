from typing import Optional

from const import TypeActionsMapping
from core.integration import Integration


class ZHAIntegration(Integration):
    def get_name(self):
        return "zha"

    def get_actions_mapping(self) -> Optional[TypeActionsMapping]:
        return self.controller.get_zha_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        self.controller.listen_event(
            self.callback, "zha_event", device_ieee=controller_id
        )

    async def callback(self, event_name: str, data: dict, kwargs: dict) -> None:
        action = data["command"]
        args = data["args"]
        if type(args) == dict:
            args = args["args"]
        args = list(map(str, args))
        if not (action == "stop" or action == "release"):
            if len(args) > 0:
                action += "_" + "_".join(args)
        await self.controller.handle_action(action)
