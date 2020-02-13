from core.type.light_controller import LightController
from core.type.media_player_controller import MediaPlayerController
from const import Light, MediaPlayer


class CustomController(LightController, MediaPlayerController):
    def initialize(self):
        super().initialize()
        custom_mapping = self.args["mapping"]
