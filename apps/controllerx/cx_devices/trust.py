from cx_const import DefaultActionsMapping, Light, MediaPlayer
from cx_core import LightController, MediaPlayerController


class ZYCT202LightController(LightController):
    """
    This controller does not send hold action for on/off
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "up-press": Light.HOLD_BRIGHTNESS_UP,
            "down-press": Light.HOLD_BRIGHTNESS_DOWN,
            "off": Light.OFF,
            "stop": Light.RELEASE,
        }


class ZYCT202MediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": MediaPlayer.PLAY_PAUSE,
            "up-press": MediaPlayer.HOLD_VOLUME_UP,
            "down-press": MediaPlayer.HOLD_VOLUME_DOWN,
            "off": MediaPlayer.PLAY_PAUSE,
            "stop": MediaPlayer.RELEASE,
        }
