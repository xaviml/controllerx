from core.controller import Controller, ReleaseHoldController, action


class MediaPlayerController(ReleaseHoldController):
    def initialize(self):
        super().initialize()
        self.media_player = self.args["media_player"]

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
        if direction == Controller.DIRECTION_UP:
            self.call_service("media_player/volume_up", entity_id=self.media_player)
        else:
            self.call_service("media_player/volume_down", entity_id=self.media_player)
        self.hold_loop_times += 1
        return self.hold_loop_times > 10

    def default_delay(self):
        return 500
