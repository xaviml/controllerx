from core.integration import Integration


class ZHAIntegration(Integration):
    def __init__(self, controller, kwargs):
        super().__init__("zha", controller, kwargs)

    def get_actions_mapping(self):
        return self.controller.get_zha_actions_mapping()

    def listen_changes(self, controller_id):
        self.controller.listen_event(
            self.callback, "zha_event", device_ieee=controller_id
        )

    async def callback(self, event_name, data, kwargs):
        action = data["command"]
        args = data["args"]
        if type(args) == dict:
            args = args["args"]
        args = list(map(str, args))
        if not (action == "stop" or action == "release"):
            if len(args) > 0:
                action += "_" + "_".join(args)
        await self.controller.handle_action(action)
