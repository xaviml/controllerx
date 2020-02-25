from core.integration import Integration


class StateIntegration(Integration):
    def get_name(self):
        return "state"

    def get_actions_mapping(self):
        return self.controller.get_z2m_actions_mapping()

    def listen_changes(self, controller_id):
        self.controller.listen_state(self.callback, controller_id)

    async def callback(self, entity, attribute, old, new, kwargs):
        await self.controller.handle_action(new)
