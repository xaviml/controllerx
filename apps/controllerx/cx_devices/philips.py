from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController
from cx_core.integration import EventData


class HueDimmerController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_press_release": Light.ON,
            "on_hold": Light.HOLD_COLOR_UP,
            "on_hold_release": Light.RELEASE,
            "up_press_release": Light.CLICK_BRIGHTNESS_UP,
            "up_hold": Light.HOLD_BRIGHTNESS_UP,
            "up_hold_release": Light.RELEASE,
            "down_press_release": Light.CLICK_BRIGHTNESS_DOWN,
            "down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "down_hold_release": Light.RELEASE,
            "off_press_release": Light.OFF,
            "off_hold": Light.HOLD_COLOR_DOWN,
            "off_hold_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,
            1001: Light.HOLD_COLOR_UP,
            1003: Light.RELEASE,
            2002: Light.CLICK_BRIGHTNESS_UP,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.OFF,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "off_long_release": Light.RELEASE,
            "off_hold": Light.HOLD_COLOR_DOWN,
            "off_short_release": Light.OFF,
            "down_long_release": Light.RELEASE,
            "down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "down_short_release": Light.CLICK_BRIGHTNESS_DOWN,
            "up_long_release": Light.RELEASE,
            "up_hold": Light.HOLD_BRIGHTNESS_UP,
            "up_short_release": Light.CLICK_BRIGHTNESS_UP,
            "on_long_release": Light.RELEASE,
            "on_hold": Light.HOLD_COLOR_UP,
            "on_short_release": Light.ON,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class HueDimmerZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_press_release": Z2MLight.ON,
            "on_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "on_hold_release": Z2MLight.RELEASE,
            "up_press_release": Z2MLight.CLICK_BRIGHTNESS_UP,
            "up_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "up_hold_release": Z2MLight.RELEASE,
            "down_press_release": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "down_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "down_hold_release": Z2MLight.RELEASE,
            "off_press_release": Z2MLight.OFF,
            "off_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "off_hold_release": Z2MLight.RELEASE,
        }


class Philips929002398602LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_press_release": Light.TOGGLE,
            "on_hold": Light.TOGGLE,
            "on_hold_release": Light.RELEASE,
            "up_press_release": Light.CLICK_BRIGHTNESS_UP,
            "up_hold": Light.HOLD_BRIGHTNESS_UP,
            "up_hold_release": Light.RELEASE,
            "down_press_release": Light.CLICK_BRIGHTNESS_DOWN,
            "down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "down_hold_release": Light.RELEASE,
            "off_press_release": Light.CLICK_COLOR_UP,
            "off_hold": Light.HOLD_COLOR_DOWN,
            "off_hold_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1001: Light.TOGGLE,
            1003: Light.RELEASE,
            2002: Light.CLICK_BRIGHTNESS_UP,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.CLICK_COLOR_UP,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "off_long_release": Light.RELEASE,
            "off_hold": Light.HOLD_COLOR_DOWN,
            "off_short_release": Light.CLICK_COLOR_UP,
            "down_long_release": Light.RELEASE,
            "down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "down_short_release": Light.CLICK_BRIGHTNESS_DOWN,
            "up_long_release": Light.RELEASE,
            "up_hold": Light.HOLD_BRIGHTNESS_UP,
            "up_short_release": Light.CLICK_BRIGHTNESS_UP,
            "on_long_release": Light.RELEASE,
            "on_hold": Light.TOGGLE,
            "on_short_release": Light.TOGGLE,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class Philips929002398602Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_press_release": Z2MLight.ON,
            "on_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "on_hold_release": Z2MLight.RELEASE,
            "up_press_release": Z2MLight.CLICK_BRIGHTNESS_UP,
            "up_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "up_hold_release": Z2MLight.RELEASE,
            "down_press_release": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "down_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "down_hold_release": Z2MLight.RELEASE,
            "off_press_release": Z2MLight.OFF,
            "off_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "off_hold_release": Z2MLight.RELEASE,
        }


class PTM215XLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "press_1": Light.ON,
            "release_1": Light.RELEASE,
            "press_2": Light.OFF,
            "release_2": Light.RELEASE,
            "press_3": Light.ON_FULL_BRIGHTNESS,
            "release_3": Light.RELEASE,
            "press_4": Light.ON_MIN_BRIGHTNESS,
            "release_4": Light.RELEASE,
            "press_1_and_3": Light.ON_FULL_COLOR_TEMP,
            "release_1_and_3": Light.RELEASE,
            "press_2_and_4": Light.ON_MIN_COLOR_TEMP,
            "release_2_and_4": Light.RELEASE,
            "press_energy_bar": Light.SYNC,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,  # button_1_release
            1001: Light.SYNC,  # button_1_hold
            1000: None,  # button_1_press
            1003: None,  # button_1_release_after_hold
            2002: Light.OFF,  # button_2_release
            2001: Light.SYNC,  # button_2_hold
            2000: None,  # button_2_press
            2003: None,  # button_2_release_after_hold
            3002: Light.ON_FULL_BRIGHTNESS,  # button_3_release
            3001: Light.HOLD_BRIGHTNESS_UP,  # button_3_hold
            3000: None,  # button_3_press
            3003: Light.RELEASE,  # button_3_release_after_hold
            4002: Light.ON_MIN_BRIGHTNESS,  # button_4_release
            4001: Light.HOLD_BRIGHTNESS_DOWN,  # button_4_hold
            4000: None,  # button_4_press
            4003: Light.RELEASE,  # button_4_release_after_hold
            5002: Light.ON_FULL_COLOR_TEMP,  # button_1_3_release
            5001: Light.HOLD_COLOR_UP,  # button_1_3_hold
            5000: None,  # button_1_3_press
            5003: Light.RELEASE,  # button_1_3_release_after_hold
            6002: Light.ON_MIN_COLOR_TEMP,  # button_2_4_release
            6001: Light.HOLD_COLOR_DOWN,  # button_2_4_hold
            6000: None,  # button_2_4_press
            6003: Light.RELEASE,  # button_2_4_release_after_hold
        }


class HueSmartButtonLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1000: None,  # Initial press
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,
            1002: Light.TOGGLE,
            1003: Light.RELEASE,
        }


class HueSmartButtonZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.TOGGLE,
            "off": Z2MLight.TOGGLE,
            "hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "release": Z2MLight.RELEASE,
        }


class Philips929003017102LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # "left_press": Light.TOGGLE,
            "left_press_release": Light.TOGGLE,
            "left_hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "left_hold_release": Light.RELEASE,
            # "right_press": Light.TOGGLE,
            "right_press_release": Light.TOGGLE,
            "right_hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "right_hold_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1000: None,  # Initial press
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,
            1002: Light.TOGGLE,
            1003: Light.RELEASE,
            2000: None,  # Initial press
            2001: Light.HOLD_BRIGHTNESS_TOGGLE,
            2002: Light.TOGGLE,
            2003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # "left_press": Light.TOGGLE,
            "left_press_release": Light.TOGGLE,
            "left_hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "left_hold_release": Light.RELEASE,
            # "right_press": Light.TOGGLE,
            "right_press_release": Light.TOGGLE,
            "right_hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "right_hold_release": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class Philips929003017102Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            # "left_press": Z2MLight.TOGGLE,
            "left_press_release": Z2MLight.TOGGLE,
            "left_hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "left_hold_release": Z2MLight.RELEASE,
            # "right_press": Z2MLight.TOGGLE,
            "right_press_release": Z2MLight.TOGGLE,
            "right_hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "right_hold_release": Z2MLight.RELEASE,
        }


class PhilipsRDM002LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_press_release": Light.OFF,
            "button_1_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_1_hold_release": Light.RELEASE,
            "button_2_press_release": Light.ON,
            "button_2_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_2_hold_release": Light.RELEASE,
            "button_3_press_release": Light.CLICK_COLOR_DOWN,
            "button_3_hold": Light.HOLD_COLOR_DOWN,
            "button_3_hold_release": Light.RELEASE,
            "button_4_press_release": Light.CLICK_COLOR_UP,
            "button_4_hold": Light.HOLD_COLOR_UP,
            "button_4_hold_release": Light.RELEASE,
            "dial_rotate_left_step": Light.CLICK_BRIGHTNESS_DOWN,
            "dial_rotate_left_slow": Light.ON_MIN_COLOR_TEMP,
            "dial_rotate_left_fast": Light.ON_MIN_BRIGHTNESS,
            "dial_rotate_right_step": Light.CLICK_BRIGHTNESS_UP,
            "dial_rotate_right_slow": Light.ON_FULL_COLOR_TEMP,
            "dial_rotate_right_fast": Light.ON_FULL_BRIGHTNESS,
        }


class PhilipsRDM002Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_press_release": Z2MLight.OFF,
            "button_1_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "button_1_hold_release": Z2MLight.RELEASE,
            "button_2_press_release": Z2MLight.ON,
            "button_2_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "button_2_hold_release": Z2MLight.RELEASE,
            "button_3_press_release": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "button_3_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "button_3_hold_release": Z2MLight.RELEASE,
            "button_4_press_release": Z2MLight.CLICK_COLOR_TEMP_UP,
            "button_4_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "button_4_hold_release": Z2MLight.RELEASE,
            "dial_rotate_left_step": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "dial_rotate_left_slow": Z2MLight.ON_MIN_COLOR_TEMP,
            "dial_rotate_left_fast": Z2MLight.ON_MIN_BRIGHTNESS,
            "dial_rotate_right_step": Light.CLICK_BRIGHTNESS_UP,
            "dial_rotate_right_slow": Z2MLight.ON_FULL_COLOR_TEMP,
            "dial_rotate_right_fast": Z2MLight.ON_FULL_BRIGHTNESS,
        }
