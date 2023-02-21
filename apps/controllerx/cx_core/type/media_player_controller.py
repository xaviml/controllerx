from typing import Any, Dict, List, Optional, Type

from cx_const import MediaPlayer, Number, PredefinedActionsMapping, StepperDir
from cx_core.controller import action
from cx_core.feature_support.media_player import MediaPlayerSupport
from cx_core.integration import EventData
from cx_core.integration.z2m import Z2MIntegration
from cx_core.release_hold_controller import ReleaseHoldController
from cx_core.stepper import MinMax
from cx_core.stepper.index_loop_stepper import IndexLoopStepper
from cx_core.stepper.stop_stepper import StopStepper
from cx_core.type_controller import Entity, TypeController

DEFAULT_VOLUME_STEPS = 10


class MediaPlayerController(TypeController[Entity], ReleaseHoldController):
    domains = ["media_player"]
    entity_arg = "media_player"
    volume_level: float

    async def init(self) -> None:
        volume_steps = self.args.get("volume_steps", DEFAULT_VOLUME_STEPS)
        self.volume_stepper = StopStepper(MinMax(0, 1), volume_steps)
        self.volume_level = 0.0
        await super().init()

    def _get_entity_type(self) -> Type[Entity]:
        return Entity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            MediaPlayer.HOLD_VOLUME_DOWN: (self.hold, (StepperDir.DOWN,)),
            MediaPlayer.HOLD_VOLUME_UP: (self.hold, (StepperDir.UP,)),
            MediaPlayer.CLICK_VOLUME_DOWN: self.volume_down,
            MediaPlayer.CLICK_VOLUME_UP: self.volume_up,
            MediaPlayer.VOLUME_SET: self.volume_set,
            MediaPlayer.RELEASE: self.release,
            MediaPlayer.PLAY: self.play,
            MediaPlayer.PAUSE: self.pause,
            MediaPlayer.PLAY_PAUSE: self.play_pause,
            MediaPlayer.NEXT_TRACK: self.next_track,
            MediaPlayer.PREVIOUS_TRACK: self.previous_track,
            MediaPlayer.NEXT_SOURCE: (self.change_source_list, (StepperDir.UP,)),
            MediaPlayer.PREVIOUS_SOURCE: (self.change_source_list, (StepperDir.DOWN,)),
            MediaPlayer.MUTE: self.volume_mute,
            MediaPlayer.TTS: self.tts,
            MediaPlayer.VOLUME_FROM_CONTROLLER_ANGLE: self.volume_from_controller_angle,
        }

    @action
    async def change_source_list(self, direction: str) -> None:
        entity_states = await self.get_entity_state(attribute="all")
        entity_attributes = entity_states["attributes"]
        source_list: Optional[List[str]] = entity_attributes.get("source_list")
        if source_list is None or len(source_list) == 0:
            self.log(
                f"⚠️ There is no `source_list` parameter in `{self.entity}`",
                level="WARNING",
                ascii_encode=False,
            )
            return
        source = entity_attributes.get("source")
        new_index_source: Number
        if source is None:
            new_index_source = 0
        else:
            index_source = source_list.index(source)
            source_stepper = IndexLoopStepper(len(source_list))
            stepper_output = source_stepper.step(index_source, direction)
            new_index_source = stepper_output.next_value
        await self.call_service(
            "media_player/select_source",
            entity_id=self.entity.name,
            source=source_list[int(new_index_source)],
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
    async def volume_set(self, volume_level: float) -> None:
        await self.call_service(
            "media_player/volume_set",
            entity_id=self.entity.name,
            volume_level=volume_level,
        )

    @action
    async def volume_up(self) -> None:
        await self.prepare_volume_change()
        await self.volume_change(StepperDir.UP)

    @action
    async def volume_down(self) -> None:
        await self.prepare_volume_change()
        await self.volume_change(StepperDir.DOWN)

    @action
    async def volume_mute(self) -> None:
        await self.call_service("media_player/volume_mute", entity_id=self.entity.name)

    @action
    async def tts(
        self,
        message: str,
        service: str = "google_translate_say",
        cache: Optional[bool] = None,
        language: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        args: Dict[str, Any] = {"entity_id": self.entity.name, "message": message}
        if cache is not None:
            args["cache"] = cache
        if language is not None:
            args["language"] = language
        if options is not None:
            args["options"] = options
        await self.call_service(f"tts.{service}", **args)

    @action
    async def volume_from_controller_angle(
        self, extra: Optional[EventData] = None
    ) -> None:
        if extra is None:
            self.log("No event data present", level="WARNING")
            return
        if isinstance(self.integration, Z2MIntegration):
            if "action_rotation_angle" not in extra:
                self.log(
                    "`action_rotation_angle` is not present in the MQTT payload",
                    level="WARNING",
                )
                return
            angle = extra["action_rotation_angle"]
            direction = StepperDir.UP if angle > 0 else StepperDir.DOWN
            await self._hold(direction)

    @action
    async def hold(self, direction: str) -> None:  # type: ignore[override]
        await self._hold(direction)

    async def _hold(self, direction: str) -> None:
        await self.prepare_volume_change()
        await super().hold(direction)

    async def prepare_volume_change(self) -> None:
        volume_level = await self.get_entity_state(attribute="volume_level")
        if volume_level is not None:
            self.volume_level = volume_level

    async def volume_change(self, direction: str) -> bool:
        if await self.feature_support.is_supported(MediaPlayerSupport.VOLUME_SET):
            stepper_output = self.volume_stepper.step(self.volume_level, direction)
            self.volume_level = stepper_output.next_value
            await self.volume_set(self.volume_level)
            return stepper_output.exceeded
        else:
            if direction == StepperDir.UP:
                await self.call_service(
                    "media_player/volume_up", entity_id=self.entity.name
                )
            else:
                await self.call_service(
                    "media_player/volume_down", entity_id=self.entity.name
                )
            return False

    async def hold_loop(self, direction: str) -> bool:  # type: ignore[override]
        return await self.volume_change(direction)

    def default_delay(self) -> int:
        return 500
