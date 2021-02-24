from cx_const import DefaultActionsMapping, Light, MediaPlayer
from cx_core import LightController, MediaPlayerController


class LZL4BWHL01LightController(LightController):
    # Each button press fires an event but no separate
    # hold event. Press of up or down generates a stop event
    # when released.

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON_FULL_BRIGHTNESS,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.OFF,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "move_to_level_with_on_off_254_4": Light.ON_FULL_BRIGHTNESS,
            "step_with_on_off_0_30_6": Light.HOLD_BRIGHTNESS_UP,
            "step_1_30_6": Light.HOLD_BRIGHTNESS_DOWN,
            "move_to_level_with_on_off_0_4": Light.OFF,
            "stop": Light.RELEASE,
        }


class Z31BRLLightController(LightController):
    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            2002: Light.CLICK_BRIGHTNESS_UP,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
        }


class LutronPJ22BLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "4": Light.OFF,
        }

    def get_lutron_caseta_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_2_press": Light.ON,
            "button_4_press": Light.OFF,
        }


class LutronPJ22BMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "4": MediaPlayer.NEXT_TRACK,
        }

    def get_lutron_caseta_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_2_press": MediaPlayer.PLAY_PAUSE,
            "button_4_press": MediaPlayer.NEXT_TRACK,
        }


class LutronPJ22BRLLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "8": Light.HOLD_BRIGHTNESS_UP,
            "16": Light.HOLD_BRIGHTNESS_DOWN,
            "4": Light.OFF,
            "0": Light.RELEASE,
        }


class LutronPJ22BRLMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "8": MediaPlayer.HOLD_VOLUME_UP,
            "16": MediaPlayer.HOLD_VOLUME_DOWN,
            "4": MediaPlayer.NEXT_TRACK,
            "0": MediaPlayer.RELEASE,
        }


class LutronPJ23BRLLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "8": Light.HOLD_BRIGHTNESS_UP,
            "2": Light.SET_HALF_BRIGHTNESS,
            "16": Light.HOLD_BRIGHTNESS_DOWN,
            "4": Light.OFF,
            "0": Light.RELEASE,
        }

    def get_lutron_caseta_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_2_press": Light.ON_FULL_BRIGHTNESS,
            "button_4_press": Light.OFF,
            "button_3_press": Light.SET_HALF_BRIGHTNESS,
            "button_5_press": Light.HOLD_BRIGHTNESS_UP,
            "button_5_release": Light.RELEASE,
            "button_6_press": Light.HOLD_BRIGHTNESS_DOWN,
            "button_6_release": Light.RELEASE,
        }


class LutronPJ23BRLMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "8": MediaPlayer.HOLD_VOLUME_UP,
            "2": MediaPlayer.NEXT_SOURCE,
            "16": MediaPlayer.HOLD_VOLUME_DOWN,
            "4": MediaPlayer.NEXT_TRACK,
            "0": MediaPlayer.RELEASE,
        }

    def get_lutron_caseta_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_2_press": MediaPlayer.PLAY_PAUSE,
            "button_4_press": MediaPlayer.NEXT_TRACK,
            "button_3_press": MediaPlayer.NEXT_SOURCE,
            "button_5_press": MediaPlayer.HOLD_VOLUME_UP,
            "button_5_release": MediaPlayer.RELEASE,
            "button_6_press": MediaPlayer.HOLD_VOLUME_DOWN,
            "button_6_release": MediaPlayer.RELEASE,
        }


class LutronPJ24BLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "2": Light.HOLD_BRIGHTNESS_UP,
            "4": Light.HOLD_BRIGHTNESS_DOWN,
            "8": Light.OFF,
            "0": Light.RELEASE,
        }


class LutronPJ24BMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "2": MediaPlayer.HOLD_VOLUME_UP,
            "4": MediaPlayer.HOLD_VOLUME_DOWN,
            "8": MediaPlayer.NEXT_TRACK,
            "0": MediaPlayer.RELEASE,
        }
