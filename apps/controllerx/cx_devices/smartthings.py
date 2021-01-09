from cx_const import DefaultActionsMapping, Light, MediaPlayer
from cx_core import LightController, MediaPlayerController


class SmartThingsButtonLightController(LightController):
    """
    This controller sends click, double click, and hold commands.
    No release command is sent.
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_click": Light.TOGGLE,
            "double_click": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.SET_HALF_BRIGHTNESS,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
            1001: Light.SET_HALF_BRIGHTNESS,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_single_1_0_0_0": Light.TOGGLE,
            "button_double_2_0_0_0": Light.ON_FULL_BRIGHTNESS,
            "button_hold_3_0_0_0": Light.SET_HALF_BRIGHTNESS,
        }


class SmartThingsButtonMediaPlayerController(MediaPlayerController):
    """
    This controller sends click, double click, and hold commands.
    No release command is sent.
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_click": MediaPlayer.PLAY_PAUSE,
            "double_click": MediaPlayer.NEXT_TRACK,
            "hold": MediaPlayer.PREVIOUS_TRACK,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: MediaPlayer.PLAY_PAUSE,
            1004: MediaPlayer.NEXT_TRACK,
            1001: MediaPlayer.PREVIOUS_TRACK,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_single_1_0_0_0": MediaPlayer.PLAY_PAUSE,
            "button_double_2_0_0_0": MediaPlayer.NEXT_TRACK,
            "button_hold_3_0_0_0": MediaPlayer.PREVIOUS_TRACK,
        }
