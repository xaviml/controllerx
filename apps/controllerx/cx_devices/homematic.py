from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class HMPB2WM552LightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.OFF,
            "PRESS_LONG_1": Light.HOLD_BRIGHTNESS_DOWN,
            "PRESS_CONT_1": None,
            "PRESS_LONG_RELEASE_1": Light.RELEASE,
            "PRESS_SHORT_2": Light.ON,
            "PRESS_LONG_2": Light.HOLD_BRIGHTNESS_UP,
            "PRESS_CONT_2": None,
            "PRESS_LONG_RELEASE_2": Light.RELEASE,
        }


class HMPBI4FMLightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.OFF,
            "PRESS_CONT_1": None,
            "PRESS_LONG_1": Light.CLICK_COLOR_DOWN,
            "PRESS_SHORT_2": Light.ON,
            "PRESS_CONT_2": None,
            "PRESS_LONG_2": Light.CLICK_COLOR_UP,
            "PRESS_SHORT_3": Light.CLICK_BRIGHTNESS_DOWN,
            "PRESS_CONT_3": None,
            "PRESS_LONG_3": Light.ON_MIN_BRIGHTNESS,
            "PRESS_SHORT_4": Light.CLICK_BRIGHTNESS_UP,
            "PRESS_CONT_4": None,
            "PRESS_LONG_4": Light.ON_FULL_BRIGHTNESS,
        }


class HMPB6WM55LightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.OFF,
            "PRESS_CONT_1": None,
            "PRESS_LONG_1": Light.SYNC,
            "PRESS_LONG_RELEASE_1": Light.RELEASE,
            "PRESS_SHORT_2": Light.ON,
            "PRESS_CONT_2": None,
            "PRESS_LONG_2": Light.SYNC,
            "PRESS_LONG_RELEASE_2": Light.RELEASE,
            "PRESS_SHORT_3": Light.CLICK_BRIGHTNESS_DOWN,
            "PRESS_CONT_3": None,
            "PRESS_LONG_3": Light.HOLD_BRIGHTNESS_DOWN,
            "PRESS_LONG_RELEASE_3": Light.RELEASE,
            "PRESS_SHORT_4": Light.CLICK_BRIGHTNESS_UP,
            "PRESS_CONT_4": None,
            "PRESS_LONG_4": Light.HOLD_BRIGHTNESS_UP,
            "PRESS_LONG_RELEASE_4": Light.RELEASE,
            "PRESS_SHORT_5": Light.CLICK_COLOR_DOWN,
            "PRESS_CONT_5": None,
            "PRESS_LONG_5": Light.HOLD_COLOR_DOWN,
            "PRESS_LONG_RELEASE_5": Light.RELEASE,
            "PRESS_SHORT_6": Light.CLICK_COLOR_UP,
            "PRESS_CONT_6": None,
            "PRESS_LONG_6": Light.HOLD_COLOR_UP,
            "PRESS_LONG_RELEASE_6": Light.RELEASE,
        }


class HMSenMDIRWM55LightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.OFF,
            "PRESS_LONG_1": Light.HOLD_BRIGHTNESS_DOWN,
            "PRESS_CONT_1": None,
            "PRESS_LONG_RELEASE_1": Light.RELEASE,
            "PRESS_SHORT_2": Light.ON,
            "PRESS_LONG_2": Light.HOLD_BRIGHTNESS_UP,
            "PRESS_CONT_2": None,
            "PRESS_LONG_RELEASE_2": Light.RELEASE,
        }
