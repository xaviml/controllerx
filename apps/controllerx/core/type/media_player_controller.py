from core.controller import ReleaseHoldController, action
from core.stepper import Stepper
from const import MediaPlayer


class MediaPlayerController(ReleaseHoldController):
    def initialize(self):
        super().initialize()
        self.media_player = self.args["media_player"]

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
        self.call_service("media_player/volume_up", entity_id=self.media_player)

    @action
    async def volume_down(self):
        self.call_service("media_player/volume_down", entity_id=self.media_player)

    @action
    async def hold(self, direction):
        # This variable is responsible to count how many times hold_loop has been called
        # so we don't fall in a infinite loop
        self.hold_loop_times = 0
        await super().hold(direction)

    async def hold_loop(self, direction):
        if direction == Stepper.UP:
            self.call_service("media_player/volume_up", entity_id=self.media_player)
        else:
            self.call_service("media_player/volume_down", entity_id=self.media_player)
        self.hold_loop_times += 1
        return self.hold_loop_times > 10

    def default_delay(self):
        return 500
