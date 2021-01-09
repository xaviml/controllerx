from typing import Callable, Type

from cx_const import Cover, PredefinedActionsMapping
from cx_core.controller import action
from cx_core.feature_support.cover import CoverSupport
from cx_core.type_controller import Entity, TypeController


class CoverController(TypeController[Entity]):
    """
    This is the main class that controls the coveres for different devices.
    Type of actions:
        - Open
        - Close
    Parameters taken:
        - controller (required): Inherited from Controller
        - cover (required): cover entity name
        - open_position (optional): The open position. Default is 100
        - close_position (optional): The close position. Default is 0
    """

    domains = ["cover"]
    entity_arg = "cover"

    open_position: int
    close_position: int

    async def init(self) -> None:
        self.open_position = self.args.get("open_position", 100)
        self.close_position = self.args.get("close_position", 0)
        if self.open_position < self.close_position:
            raise ValueError("`open_position` must be higher than `close_position`")
        await super().init()

    def _get_entity_type(self) -> Type[Entity]:
        return Entity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            Cover.OPEN: self.open,
            Cover.CLOSE: self.close,
            Cover.STOP: self.stop,
            Cover.TOGGLE_OPEN: (self.toggle, (self.open,)),
            Cover.TOGGLE_CLOSE: (self.toggle, (self.close,)),
        }

    @action
    async def open(self) -> None:
        if await self.feature_support.is_supported(CoverSupport.SET_COVER_POSITION):
            await self.call_service(
                "cover/set_cover_position",
                entity_id=self.entity.name,
                position=self.open_position,
            )
        elif await self.feature_support.is_supported(CoverSupport.OPEN):
            await self.call_service("cover/open_cover", entity_id=self.entity.name)
        else:
            self.log(
                f"⚠️ `{self.entity.name}` does not support SET_COVER_POSITION or OPEN",
                level="WARNING",
                ascii_encode=False,
            )

    @action
    async def close(self) -> None:
        if await self.feature_support.is_supported(CoverSupport.SET_COVER_POSITION):
            await self.call_service(
                "cover/set_cover_position",
                entity_id=self.entity.name,
                position=self.close_position,
            )
        elif await self.feature_support.is_supported(CoverSupport.CLOSE):
            await self.call_service("cover/close_cover", entity_id=self.entity.name)
        else:
            self.log(
                f"⚠️ `{self.entity.name}` does not support SET_COVER_POSITION or CLOSE",
                level="WARNING",
                ascii_encode=False,
            )

    @action
    async def stop(self) -> None:
        await self.call_service("cover/stop_cover", entity_id=self.entity.name)

    @action
    async def toggle(self, action: Callable) -> None:
        cover_state = await self.get_entity_state(self.entity.name)
        if cover_state == "opening" or cover_state == "closing":
            await self.stop()
        else:
            await action()
