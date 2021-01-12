from typing import Type

from cx_const import MediaPlayer, PredefinedActionsMapping
from cx_core.controller import action
from cx_core.feature_support.media_player import MediaPlayerSupport
from cx_core.release_hold_controller import ReleaseHoldController
from cx_core.stepper import Stepper
from cx_core.stepper.circular_stepper import CircularStepper
from cx_core.stepper.minmax_stepper import MinMaxStepper
from cx_core.type_controller import Entity, TypeController

DEFAULT_VOLUME_STEPS = 10


class MediaPlayerController(TypeController[Entity], ReleaseHoldController):

    domains = ["media_player"]
    entity_arg = "media_player"

    async def init(self) -> None:
        volume_steps = self.args.get("volume_steps", DEFAULT_VOLUME_STEPS)
        self.volume_stepper = MinMaxStepper(0, 1, volume_steps)
        self.volume_level = 0.0
        await super().init()

    def _get_entity_type(self) -> Type[Entity]:
        return Entity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            MediaPlayer.HOLD_VOLUME_DOWN: (self.hold, (Stepper.DOWN,)),
            MediaPlayer.HOLD_VOLUME_UP: (self.hold, (Stepper.UP,)),
            MediaPlayer.CLICK_VOLUME_DOWN: self.volume_down,
            MediaPlayer.CLICK_VOLUME_UP: self.volume_up,
            MediaPlayer.RELEASE: self.release,
            MediaPlayer.PLAY: self.play,
            MediaPlayer.PAUSE: self.pause,
            MediaPlayer.PLAY_PAUSE: self.play_pause,
            MediaPlayer.NEXT_TRACK: self.next_track,
            MediaPlayer.PREVIOUS_TRACK: self.previous_track,
            MediaPlayer.NEXT_SOURCE: (self.change_source_list, (Stepper.UP,)),
            MediaPlayer.PREVIOUS_SOURCE: (self.change_source_list, (Stepper.DOWN,)),
        }

    @action
    async def change_source_list(self, direction: str) -> None:
        entity_states = await self.get_entity_state(self.entity.name, attribute="all")
        entity_attributes = entity_states["attributes"]
        source_list = entity_attributes.get("source_list")
        if len(source_list) == 0 or source_list is None:
            self.log(
                f"⚠️ There is no `source_list` parameter in `{self.entity.name}`",
                level="WARNING",
                ascii_encode=False,
            )
            return
        source = entity_attributes.get("source")
        if source is None:
            new_index_source = 0
        else:
            index_source = source_list.index(source)
            source_stepper = CircularStepper(0, len(source_list) - 1, len(source_list))
            new_index_source, _ = source_stepper.step(index_source, direction)
        await self.call_service(
            "media_player/select_source",
            entity_id=self.entity.name,
            source=source_list[new_index_source],
        )

    @action
    async def play(self) -> None:
        await self.call_service("media_player/media_play", entity_id=self.entity.name)

    @action
    async def pause(self) -> None:
        await self.call_service("media_player/media_pause", entity_id=self.entity.name)

    @action
    async def play_pause(self) -> None:
        await self.call_service(
            "media_player/media_play_pause", entity_id=self.entity.name
        )

    @action
    async def previous_track(self) -> None:
        await self.call_service(
            "media_player/media_previous_track", entity_id=self.entity.name
        )

    @action
    async def next_track(self) -> None:
        await self.call_service(
            "media_player/media_next_track", entity_id=self.entity.name
        )

    @action
    async def volume_up(self) -> None:
        await self.prepare_volume_change()
        await self.volume_change(Stepper.UP)

    @action
    async def volume_down(self) -> None:
        await self.prepare_volume_change()
        await self.volume_change(Stepper.DOWN)

    @action
    async def hold(self, direction: str) -> None:
        await self.prepare_volume_change()
        await super().hold(direction)

    async def prepare_volume_change(self) -> None:
        volume_level = await self.get_entity_state(
            self.entity.name, attribute="volume_level"
        )
        if volume_level is not None:
            self.volume_level = volume_level

    async def volume_change(self, direction: str) -> bool:
        if await self.feature_support.is_supported(MediaPlayerSupport.VOLUME_SET):
            self.volume_level, exceeded = self.volume_stepper.step(
                self.volume_level, direction
            )
            await self.call_service(
                "media_player/volume_set",
                entity_id=self.entity.name,
                volume_level=self.volume_level,
            )
            return exceeded
        else:
            if direction == Stepper.UP:
                await self.call_service(
                    "media_player/volume_up", entity_id=self.entity.name
                )
            else:
                await self.call_service(
                    "media_player/volume_down", entity_id=self.entity.name
                )
            return False

    async def hold_loop(self, direction: str) -> bool:  # type: ignore
        return await self.volume_change(direction)

    def default_delay(self) -> int:
        return 500
