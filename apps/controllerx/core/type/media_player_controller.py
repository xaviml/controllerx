from const import MediaPlayer
from core.controller import ReleaseHoldController, action
from core.stepper import Stepper
from core.stepper.minmax_stepper import MinMaxStepper

DEFAULT_VOLUME_STEPS = 10


class MediaPlayerController(ReleaseHoldController):
    def initialize(self):
        super().initialize()
        self.media_player = self.args["media_player"]
        volume_steps = self.args.get("volume_steps", DEFAULT_VOLUME_STEPS)
        self.volume_stepper = MinMaxStepper(0, 1, volume_steps)
        self.volume_level = 0

    def get_type_actions_mapping(self):
        return {
            MediaPlayer.HOLD_DOWN: (self.hold, Stepper.DOWN),
            MediaPlayer.HOLD_UP: (self.hold, Stepper.UP),
            MediaPlayer.VOLUME_DOWN: self.volume_down,
            MediaPlayer.VOLUME_UP: self.volume_up,
            MediaPlayer.RELEASE: self.release,
            MediaPlayer.PLAY_PAUSE: self.play_pause,
            MediaPlayer.NEXT_TRACK: self.next_track,
            MediaPlayer.PREVIOUS_TRACK: self.previous_track,
        }

    @action
    async def play_pause(self):
        self.call_service("media_player/media_play_pause", entity_id=self.media_player)

    @action
    async def previous_track(self):
        self.call_service(
            "media_player/media_previous_track", entity_id=self.media_player
        )

    @action
    async def next_track(self):
        self.call_service("media_player/media_next_track", entity_id=self.media_player)

    @action
    async def volume_up(self):
        await self.prepare_volume_change()
        await self.volume_change(Stepper.UP)

    @action
    async def volume_down(self):
        await self.prepare_volume_change()
        await self.volume_change(Stepper.DOWN)

    @action
    async def hold(self, direction):
        await self.prepare_volume_change()
        await super().hold(direction)

    async def prepare_volume_change(self):
        volume_level = await self.get_entity_state(
            self.media_player, attribute="volume_level"
        )
        if volume_level is not None:
            self.volume_level = volume_level

    async def volume_change(self, direction):
        self.volume_level, exceeded = self.volume_stepper.step(
            self.volume_level, direction
        )
        self.call_service(
            "media_player/volume_set",
            entity_id=self.media_player,
            volume_level=self.volume_level,
        )
        return exceeded

    async def hold_loop(self, direction):
        return await self.volume_change(direction)

    def default_delay(self):
        return 500
