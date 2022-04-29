from cx_const import DefaultActionsMapping, Light, MediaPlayer
from cx_core import LightController, MediaPlayerController
from cx_core.integration import EventData


class TerncyPP01LightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_single": Light.TOGGLE,
            "button_double": Light.ON_FULL_BRIGHTNESS,
            "button_triple": Light.ON_MIN_BRIGHTNESS,
            "button_quadruple": Light.SET_HALF_BRIGHTNESS,
            "button_quintuple": Light.SET_HALF_COLOR_TEMP,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class TerncySD01LightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_single": Light.TOGGLE,
            "button_double": Light.ON_FULL_BRIGHTNESS,
            "button_triple": Light.ON_MIN_BRIGHTNESS,
            "button_quadruple": Light.SET_HALF_BRIGHTNESS,
            "button_quintuple": Light.SET_HALF_COLOR_TEMP,
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class TerncySD01MediaPlayerController(MediaPlayerController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_single": MediaPlayer.PLAY_PAUSE,
            "button_double": MediaPlayer.MUTE,
            "button_triple": MediaPlayer.NEXT_TRACK,
            "button_quadruple": MediaPlayer.PREVIOUS_TRACK,
            "button_quintuple": MediaPlayer.NEXT_SOURCE,
            "rotate_left": MediaPlayer.CLICK_VOLUME_DOWN,
            "rotate_right": MediaPlayer.CLICK_VOLUME_UP,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command
