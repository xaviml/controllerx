from typing import Callable
from const import Cover, TypeActionsMapping
from core.controller import TypeController, action


class CoverController(TypeController):
    """
    This is the main class that controls the coveres for different devices.
    Type of actions:
        - Open
        - Close
    Parameters taken:
        - controller (required): Inherited from Controller
        - cover (required): cover entity name
        - delay (optional): Inherited from ReleaseHoldController
    """

    async def initialize(self) -> None:
        self.cover = self.args["cover"]
        await self.check_domain(self.cover)
        await super().initialize()

    def get_domain(self) -> str:
        return "cover"

    def get_type_actions_mapping(self) -> TypeActionsMapping:
        return {
            Cover.OPEN: self.open,
            Cover.CLOSE: self.close,
            Cover.STOP: self.stop,
            Cover.TOGGLE_OPEN: (self.toggle, self.open),
            Cover.TOGGLE_CLOSE: (self.toggle, self.close),
        }

    @action
    async def open(self) -> None:
        await self.call_service("cover/open_cover", entity_id=self.cover)

    @action
    async def close(self) -> None:
        await self.call_service("cover/close_cover", entity_id=self.cover)

    @action
    async def stop(self) -> None:
        await self.call_service("cover/stop_cover", entity_id=self.cover)

    @action
    async def toggle(self, action: Callable) -> None:
        cover_state = await self.get_entity_state(self.cover)
        if cover_state == "opening" or cover_state == "closing":
            await self.stop()
        else:
            await action()
