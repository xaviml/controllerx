from const import Switch
from core.controller import TypeController, action


class SwitchController(TypeController):
    """
    This is the main class that controls the switches for different devices.
    Type of actions:
        - On/Off/Toggle
    Parameters taken:
        - sensor (required): Inherited from Controller
        - switch (required): Switch entity name
        - delay (optional): Inherited from ReleaseHoldController
    """

    async def initialize(self):
        self.switch = self.args["switch"]
        await self.check_domain(self.switch)

        await super().initialize()

    def get_domain(self):
        return "switch"

    def get_type_actions_mapping(self):
        return {
            Switch.ON: self.on,
            Switch.OFF: self.off,
            Switch.TOGGLE: self.toggle,
        }

    @action
    async def on(self):
        self.call_service("switch/turn_on", entity_id=self.switch)

    @action
    async def off(self):
        self.call_service("switch/turn_off", entity_id=self.switch)

    @action
    async def toggle(self):
        self.call_service("switch/toggle", entity_id=self.switch)
