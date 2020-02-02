from core.integration import Integration


class DeCONZIntegration(Integration):
    def __init__(self, controller):
        super().__init__("deconz", controller)

    def get_actions_mapping(self):
        return self.controller.get_deconz_actions_mapping()

    def listen_changes(self, controller_id):
        self.controller.listen_event(self.callback, "deconz_event", id=controller_id)

    async def callback(self, event_name, data, kwargs):
        await self.controller.handle_action(data["event"])
