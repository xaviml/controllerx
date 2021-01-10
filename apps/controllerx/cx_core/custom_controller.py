from cx_core.controller import Controller
from cx_core.type.cover_controller import CoverController
from cx_core.type.light_controller import LightController
from cx_core.type.media_player_controller import MediaPlayerController
from cx_core.type.switch_controller import SwitchController


class CustomLightController(LightController):
    async def init(self) -> None:
        self.log(
            "⚠️ `CustomLightController` is deprecated and will be removed. Use `LightController` instead",
            level="WARNING",
            ascii_encode=False,
        )
        await super().init()


class CustomMediaPlayerController(MediaPlayerController):
    async def init(self) -> None:
        self.log(
            "⚠️ `CustomMediaPlayerController` is deprecated and will be removed. Use `MediaPlayerController` instead",
            level="WARNING",
            ascii_encode=False,
        )
        await super().init()


class CustomSwitchController(SwitchController):
    async def init(self) -> None:
        self.log(
            "⚠️ `CustomSwitchController` is deprecated and will be removed. Use `SwitchController` instead",
            level="WARNING",
            ascii_encode=False,
        )
        await super().init()


class CustomCoverController(CoverController):
    async def init(self) -> None:
        self.log(
            "⚠️ `CustomCoverController` is deprecated and will be removed. Use `CoverController` instead",
            level="WARNING",
            ascii_encode=False,
        )
        await super().init()


class CallServiceController(Controller):
    async def init(self) -> None:
        self.log(
            "⚠️ `CallServiceController` is deprecated and will be removed. Use `Controller` instead",
            level="WARNING",
            ascii_encode=False,
        )
        await super().init()
