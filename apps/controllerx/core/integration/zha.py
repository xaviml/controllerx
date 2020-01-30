from core.integration import Integration


class ZHAIntegration(Integration):
    def __init__(self, controller):
        super().__init__("zha", controller)

    def get_actions_mapping(self):
        return None

    def listen_changes(self, controller_id):
        pass

    async def callback(self, event_name, data, kwargs):
        await self.controller.handle_action(data["event"])