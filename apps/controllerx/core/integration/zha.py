from core.integration import Integration


class ZHAIntegration(Integration):
    def __init__(self, controller):
        super().__init__("zha", controller)

    def get_actions_mapping(self):
        return self.controller.get_zha_actions_mapping()

    def listen_changes(self, controller_id):
        self.controller.listen_event(
            self.callback, "zha_event", device_ieee=controller_id
        )

    async def callback(self, event_name, data, kwargs):
        await self.controller.handle_action(data["command"])
