from cx_const import DefaultActionsMapping, Light, MediaPlayer
from cx_core import LightController, MediaPlayerController


class LutronCasetaProPicoLightController(LightController):
    # This requires the LutronCasetaPro CUSTOM integration by upsert
    # https://github.com/upsert/lutron-caseta-pro
    # THIS WILL NOT WORK with the default Lutron Caseta integration
    # Pico remotes using this integration report 6 states from their sensor:
    # top button = "1", up button = "8", middle round = "2", down arrow = "16",
    # bottom button = "4", no button pressed = "0"

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "8": Light.HOLD_BRIGHTNESS_UP,
            "2": Light.SET_HALF_BRIGHTNESS,
            "16": Light.HOLD_BRIGHTNESS_DOWN,
            "4": Light.OFF,
            "0": Light.RELEASE,
        }


class LutronCasetaProPicoMediaPlayerController(MediaPlayerController):
    # This requires the LutronCasetaPro CUSTOM integration by upsert
    # https://github.com/upsert/lutron-caseta-pro
    # THIS WILL NOT WORK with the default Lutron Caseta integration
    # Pico remotes using this integration report 6 states from their sensor:
    # top button = "1", up button = "8", middle round = "2", down arrow = "16",
    # bottom button = "4", no button pressed = "0"

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "8": MediaPlayer.HOLD_VOLUME_UP,
            "2": MediaPlayer.NEXT_SOURCE,
            "16": MediaPlayer.HOLD_VOLUME_DOWN,
            "4": MediaPlayer.NEXT_TRACK,
            "0": MediaPlayer.RELEASE,
        }


class LutronCasetaProPJ24BLightController(LightController):
    # This requires the LutronCasetaPro CUSTOM integration by upsert
    # https://github.com/upsert/lutron-caseta-pro
    # THIS WILL NOT WORK with the default Lutron Caseta integration
    # Pico remotes using this integration report 5 states from their sensor:
    # top button = "1", second button = "2", third button = "4",
    # bottom button = "8", no button pressed = "0"

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": Light.ON_FULL_BRIGHTNESS,
            "2": Light.HOLD_BRIGHTNESS_UP,
            "4": Light.HOLD_BRIGHTNESS_DOWN,
            "8": Light.OFF,
            "0": Light.RELEASE,
        }


class LutronCasetaProPJ24BMediaPlayerController(MediaPlayerController):
    # This requires the LutronCasetaPro CUSTOM integration by upsert
    # https://github.com/upsert/lutron-caseta-pro
    # THIS WILL NOT WORK with the default Lutron Caseta integration
    # Pico remotes using this integration report 5 states from their sensor:
    # top button = "1", second button = "2", third button = "4",
    # bottom button = "8", no button pressed = "0"

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1": MediaPlayer.PLAY_PAUSE,
            "2": MediaPlayer.HOLD_VOLUME_UP,
            "4": MediaPlayer.HOLD_VOLUME_DOWN,
            "8": MediaPlayer.NEXT_TRACK,
            "0": MediaPlayer.RELEASE,
        }


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
