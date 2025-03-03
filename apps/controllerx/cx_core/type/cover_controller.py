from collections.abc import Awaitable
from typing import Any, Callable, Optional

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

    cover_duration: Optional[int]

    is_supposedly_moving: bool = False
    stop_timer_handle: Optional[str] = None

    async def init(self) -> None:
        self.open_position = self.args.get("open_position", 100)
        self.close_position = self.args.get("close_position", 0)
        self.cover_duration = self.args.get("cover_duration")
        if self.open_position < self.close_position:
            raise ValueError("`open_position` must be higher than `close_position`")
        await super().init()

    def _get_entity_type(self) -> type[Entity]:
        return Entity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            Cover.OPEN: self.open,
            Cover.CLOSE: self.close,
            Cover.STOP: self.stop,
            Cover.TOGGLE_OPEN: (self.toggle, (self.open,)),
            Cover.TOGGLE_CLOSE: (self.toggle, (self.close,)),
        }

    async def cover_stopped_cb(self, kwargs: dict[str, Any]) -> None:
        self.is_supposedly_moving = False
        self.stop_timer_handle = None

    async def start_timer(self) -> None:
        if self.cover_duration is None:
            return
        await self.stop_timer()
        self.is_supposedly_moving = True
        self.stop_timer_handle = await self.run_in(
            self.cover_stopped_cb, self.cover_duration
        )

    async def stop_timer(self) -> None:
        if self.stop_timer_handle is not None:
            self.is_supposedly_moving = False
            await self.cancel_timer(self.stop_timer_handle)

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
                f"⚠️ `{self.entity}` does not support SET_COVER_POSITION or OPEN",
                level="WARNING",
                ascii_encode=False,
            )
            return
        await self.start_timer()

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
                f"⚠️ `{self.entity}` does not support SET_COVER_POSITION or CLOSE",
                level="WARNING",
                ascii_encode=False,
            )
            return
        await self.start_timer()

    @action
    async def stop(self) -> None:
        await self.stop_timer()
        await self.call_service("cover/stop_cover", entity_id=self.entity.name)

    @action
    async def toggle(self, action: Callable[[], Awaitable[None]]) -> None:
        cover_state = await self.get_entity_state()
        if (
            cover_state == "opening"
            or cover_state == "closing"
            or self.is_supposedly_moving
        ):
            await self.stop()
        else:
            await action()
