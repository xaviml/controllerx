from core import LightController, MediaPlayerController, Stepper, action
from const import Light, MediaPlayer


class E1810Controller(LightController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self):
        return {
            "toggle": Light.TOGGLE,
            "brightness_up_click": Light.CLICK_BRIGHTNESS_UP,
            "brightness_down_click": Light.CLICK_BRIGHTNESS_DOWN,
            "arrow_left_click": Light.CLICK_COLOR_DOWN,
            "arrow_right_click": Light.CLICK_COLOR_UP,
            "brightness_up_hold": Light.HOLD_BRIGHTNESS_UP,
            "brightness_up_release": Light.RELEASE,
            "brightness_down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Light.RELEASE,
            "arrow_left_hold": Light.HOLD_COLOR_DOWN,
            "arrow_left_release": Light.RELEASE,
            "arrow_right_hold": Light.HOLD_COLOR_UP,
            "arrow_right_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: Light.TOGGLE,
            2002: Light.CLICK_BRIGHTNESS_UP,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            4002: Light.CLICK_COLOR_DOWN,
            5002: Light.CLICK_COLOR_UP,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
            5001: Light.HOLD_COLOR_UP,
            5003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self):
        return {
            "toggle": Light.TOGGLE,
            "step_with_on_off_0_43_5": Light.CLICK_BRIGHTNESS_UP,
            "step_1_43_5": Light.CLICK_BRIGHTNESS_DOWN,
            "press_257_13_0": Light.CLICK_COLOR_DOWN,
            "press_256_13_0": Light.CLICK_COLOR_UP,
            "move_with_on_off_0_83": Light.HOLD_BRIGHTNESS_UP,
            "move_1_83": Light.HOLD_BRIGHTNESS_DOWN,
            "hold_3329_0": Light.HOLD_COLOR_DOWN,
            "hold_3328_0": Light.HOLD_COLOR_UP,
            "stop": Light.RELEASE,
            "release": Light.RELEASE,
        }


class E1810MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self):
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,
            "brightness_up_click": MediaPlayer.VOLUME_UP,
            "brightness_down_click": MediaPlayer.VOLUME_DOWN,
            "arrow_left_click": MediaPlayer.PREVIOUS_TRACK,
            "arrow_right_click": MediaPlayer.NEXT_TRACK,
            "brightness_up_hold": MediaPlayer.HOLD_UP,
            "brightness_up_release": MediaPlayer.RELEASE,
            "brightness_down_hold": MediaPlayer.HOLD_DOWN,
            "brightness_down_release": MediaPlayer.RELEASE,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: MediaPlayer.PLAY_PAUSE,
            2002: MediaPlayer.VOLUME_UP,
            3002: MediaPlayer.VOLUME_DOWN,
            4002: MediaPlayer.PREVIOUS_TRACK,
            5002: MediaPlayer.NEXT_TRACK,
            2001: MediaPlayer.HOLD_UP,
            2003: MediaPlayer.RELEASE,
            3001: MediaPlayer.HOLD_DOWN,
            3003: MediaPlayer.RELEASE,
        }

    def get_zha_actions_mapping(self):
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,
            "step_with_on_off_0_43_5": MediaPlayer.VOLUME_UP,
            "step_1_43_5": MediaPlayer.VOLUME_DOWN,
            "press_257_13_0": MediaPlayer.PREVIOUS_TRACK,
            "press_256_13_0": MediaPlayer.NEXT_TRACK,
            "move_with_on_off_0_83": MediaPlayer.HOLD_UP,
            "stop": MediaPlayer.RELEASE,
            "move_1_83": MediaPlayer.HOLD_DOWN,
            "release": MediaPlayer.RELEASE,
        }


class E1743Controller(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_z2m_actions_mapping(self):
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "brightness_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: Light.ON,
            2002: Light.OFF,
            1001: Light.HOLD_BRIGHTNESS_UP,
            2001: Light.HOLD_BRIGHTNESS_DOWN,
            1003: Light.RELEASE,
            2003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self):
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "move_with_on_off_0_83": Light.HOLD_BRIGHTNESS_UP,
            "move_1_83": Light.HOLD_BRIGHTNESS_DOWN,
            "stop": Light.RELEASE,
        }


class ICTCG1Controller(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_left_quick
    # rotate_right, rotate_right_quick
    # rotate_stop

    @action
    async def rotate_left_quick(self):
        await self.release()
        await self.off()

    @action
    async def rotate_right_quick(self):
        await self.release()
        await self.on_full(LightController.ATTRIBUTE_BRIGHTNESS)

    def get_type_actions_mapping(self):
        parent_mapping = super().get_type_actions_mapping()
        mapping = {
            "rotate_left_quick": self.rotate_left_quick,
            "rotate_right_quick": self.rotate_right_quick,
        }
        return {**parent_mapping, **mapping}

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": Light.HOLD_BRIGHTNESS_DOWN,
            "rotate_left_quick": "rotate_left_quick",
            "rotate_right": Light.HOLD_BRIGHTNESS_UP,
            "rotate_right_quick": "rotate_right_quick",
            "rotate_stop": Light.RELEASE,
        }

    def get_zha_actions_mapping(self):
        return {
            "move_1_70": Light.HOLD_BRIGHTNESS_DOWN,
            "move_1_195": Light.HOLD_BRIGHTNESS_DOWN,
            "move_to_level_with_on_off_0_1": "rotate_left_quick",
            "move_with_on_off_0_70": Light.HOLD_BRIGHTNESS_UP,
            "move_with_on_off_0_195": Light.ON,
            "move_to_level_with_on_off_255_1": "rotate_right_quick",
            "stop": Light.RELEASE,
        }


class E1744LightController(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_right, rotate_stop,
    # play_pause, skip_forward, skip_backward

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": Light.HOLD_BRIGHTNESS_DOWN,
            "rotate_right": Light.HOLD_BRIGHTNESS_UP,
            "rotate_stop": Light.RELEASE,
            "play_pause": Light.TOGGLE,
            "skip_forward": Light.ON_FULL_BRIGHTNESS,
        }

    def get_deconz_actions_mapping(self):
        return {
            2001: Light.HOLD_BRIGHTNESS_DOWN,
            3001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3003: Light.RELEASE,
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
        }

    def get_zha_actions_mapping(self):
        return {
            "move_1_195": Light.HOLD_BRIGHTNESS_DOWN,
            "move_0_195": Light.HOLD_BRIGHTNESS_UP,
            "stop": Light.RELEASE,
            "stop": Light.RELEASE,
            "toggle": Light.TOGGLE,
            "step_0_1_0": Light.ON_FULL_BRIGHTNESS,
        }

    def default_delay(self):
        return 1200


class E1744MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # rotate_left, rotate_right, rotate_stop,
    # play_pause, skip_forward, skip_backward

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": MediaPlayer.HOLD_DOWN,
            "rotate_right": MediaPlayer.HOLD_UP,
            "rotate_stop": MediaPlayer.RELEASE,
            "play_pause": MediaPlayer.PLAY_PAUSE,
            "skip_forward": MediaPlayer.NEXT_TRACK,
            "skip_backward": MediaPlayer.PREVIOUS_TRACK,
        }

    def get_deconz_actions_mapping(self):
        return {
            2001: MediaPlayer.HOLD_DOWN,
            3001: MediaPlayer.HOLD_UP,
            2003: MediaPlayer.RELEASE,
            3003: MediaPlayer.RELEASE,
            1002: MediaPlayer.PLAY_PAUSE,
            1004: MediaPlayer.NEXT_TRACK,
            1005: MediaPlayer.PREVIOUS_TRACK,
        }

    def get_zha_actions_mapping(self):
        return {
            "move_1_195": MediaPlayer.HOLD_DOWN,
            "move_0_195": MediaPlayer.HOLD_UP,
            "stop": MediaPlayer.RELEASE,
            "toggle": MediaPlayer.PLAY_PAUSE,
            "step_0_1_0": MediaPlayer.NEXT_TRACK,
            "step_1_1_0": MediaPlayer.PREVIOUS_TRACK,
        }

    def default_delay(self):
        return 1000
