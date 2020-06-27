from cx_const import Switch, TypeActionsMapping
from cx_core.controller import TypeController, action


class SwitchController(TypeController):
    """
    This is the main class that controls the switches for different devices.
    Type of actions:
        - On/Off/Toggle
    Parameters taken:
        - sensor (required): Inherited from Controller
        - switch (required): Switch entity name
    """

    async def initialize(self) -> None:
        self.switch = self.args["switch"]
        await self.check_domain(self.switch)
        await super().initialize()

    def get_domain(self) -> str:
        return "switch"

    def get_type_actions_mapping(self) -> TypeActionsMapping:
        return {
            Switch.ON: self.on,
            Switch.OFF: self.off,
            Switch.TOGGLE: self.toggle,
        }

    @action
    async def on(self) -> None:
        await self.call_service("switch/turn_on", entity_id=self.switch)

    @action
    async def off(self) -> None:
        await self.call_service("switch/turn_off", entity_id=self.switch)

    @action
    async def toggle(self) -> None:
        await self.call_service("switch/toggle", entity_id=self.switch)
