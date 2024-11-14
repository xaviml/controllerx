from cx_const import Cover, DefaultActionsMapping, Light, MediaPlayer, Z2MLight
from cx_core import (
    CoverController,
    LightController,
    MediaPlayerController,
    Z2MLightController,
)
from cx_core.integration import EventData


class TS0044LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Light.TOGGLE,
            "1_double": Light.CLICK_BRIGHTNESS_UP,
            "1_hold": Light.CLICK_BRIGHTNESS_DOWN,
            "2_single": Light.TOGGLE,
            "2_double": Light.CLICK_BRIGHTNESS_UP,
            "2_hold": Light.CLICK_BRIGHTNESS_DOWN,
            "3_single": Light.TOGGLE,
            "3_double": Light.CLICK_BRIGHTNESS_UP,
            "3_hold": Light.CLICK_BRIGHTNESS_DOWN,
            "4_single": Light.TOGGLE,
            "4_double": Light.CLICK_BRIGHTNESS_UP,
            "4_hold": Light.CLICK_BRIGHTNESS_DOWN,
        }


class TS0044FLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "brightness_step_up": Light.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Light.CLICK_BRIGHTNESS_DOWN,
        }


class TS0043LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Light.TOGGLE,
            "1_double": Light.CLICK_BRIGHTNESS_UP,
            "1_hold": Light.CLICK_BRIGHTNESS_DOWN,
            "2_single": Light.TOGGLE,
            "2_double": Light.CLICK_BRIGHTNESS_UP,
            "2_hold": Light.CLICK_BRIGHTNESS_DOWN,
            "3_single": Light.TOGGLE,
            "3_double": Light.CLICK_BRIGHTNESS_UP,
            "3_hold": Light.CLICK_BRIGHTNESS_DOWN,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_remote_button_short_press": Light.TOGGLE,
            "1_remote_button_double_press": Light.CLICK_BRIGHTNESS_UP,
            "1_remote_button_long_press": Light.CLICK_BRIGHTNESS_DOWN,
            "2_remote_button_short_press": Light.TOGGLE,
            "2_remote_button_double_press": Light.CLICK_BRIGHTNESS_UP,
            "2_remote_button_long_press": Light.CLICK_BRIGHTNESS_DOWN,
            "3_remote_button_short_press": Light.TOGGLE,
            "3_remote_button_double_press": Light.CLICK_BRIGHTNESS_UP,
            "3_remote_button_long_press": Light.CLICK_BRIGHTNESS_DOWN,
        }

    def get_zha_action(self, data: EventData) -> str:
        args: str = ""
        # Command is {endpoint_id}_{command}
        if len(data["args"]) > 0:
            if isinstance(data["args"], list):
                args = "_" + "_".join([str(d) for d in data["args"]])
            else:
                args = args + f"{data['args']}"
        command: str = f"{data['endpoint_id']}_{data['command']}{args}"
        return command


class TS0043CoverController(CoverController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Cover.OPEN,
            "2_single": Cover.STOP,
            "3_single": Cover.CLOSE,
        }


class TuYaERS10TZBVKAALightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # Command mode
            "brightness_step_up": Light.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "toggle": Light.TOGGLE,
            "hue_move": Light.HOLD_BRIGHTNESS_TOGGLE,
            "hue_stop": Light.RELEASE,
            "color_temperature_step_up": Light.CLICK_COLOR_UP,
            "color_temperature_step_down": Light.CLICK_COLOR_DOWN,
            # Event mode
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.ON_MIN_BRIGHTNESS,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": Light.TOGGLE,
            "step_brightness": Light.BRIGHTNESS_FROM_CONTROLLER_STEP,
            "step_color_temp": Light.COLORTEMP_FROM_CONTROLLER_STEP,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        if command == "step":
            return "step_brightness"
        return command


class TuYaERS10TZBVKAAZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # Command mode
            "brightness_step_up": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "toggle": Z2MLight.TOGGLE,
            "hue_move": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "hue_stop": Z2MLight.RELEASE,
            "color_temperature_step_up": Z2MLight.CLICK_COLOR_TEMP_UP,
            "color_temperature_step_down": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            # Event mode
            "rotate_left": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Z2MLight.CLICK_BRIGHTNESS_UP,
            "single": Z2MLight.TOGGLE,
            "double": Z2MLight.ON_FULL_BRIGHTNESS,
            "hold": Z2MLight.ON_MIN_BRIGHTNESS,
        }


class TuYaERS10TZBVKAAMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # Command mode
            "brightness_step_up": MediaPlayer.CLICK_VOLUME_UP,
            "brightness_step_down": MediaPlayer.CLICK_VOLUME_DOWN,
            "toggle": MediaPlayer.PLAY_PAUSE,
            "hue_move": MediaPlayer.HOLD_VOLUME_UP,
            "hue_stop": Z2MLight.RELEASE,
            "color_temperature_step_up": MediaPlayer.NEXT_TRACK,
            "color_temperature_step_down": MediaPlayer.PREVIOUS_TRACK,
            # Event mode
            "rotate_left": MediaPlayer.CLICK_VOLUME_DOWN,
            "rotate_right": MediaPlayer.CLICK_VOLUME_UP,
            "single": MediaPlayer.PLAY_PAUSE,
            "double": MediaPlayer.NEXT_TRACK,
            "hold": MediaPlayer.PREVIOUS_TRACK,
        }


class TS0042LightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_remote_button_short_press": Light.ON,
            "1_remote_button_double_press": Light.CLICK_BRIGHTNESS_UP,
            "1_remote_button_long_press": Light.ON_FULL_BRIGHTNESS,
            "2_remote_button_short_press": Light.OFF,
            "2_remote_button_double_press": Light.ON_MIN_BRIGHTNESS,
        }

    def get_zha_action(self, data: EventData) -> str:
        args: str = ""
        # Command is {endpoint_id}_{command}
        if len(data["args"]) > 0:
            if isinstance(data["args"], list):
                args = "_" + "_".join([str(d) for d in data["args"]])
            else:
                args = args + f"{data['args']}"
        command: str = f"{data['endpoint_id']}_{data['command']}{args}"
        return command
