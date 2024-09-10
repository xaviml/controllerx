from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class ShellyI3LightController(LightController):
    def get_shellyforhass_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.CLICK_BRIGHTNESS_UP,
            "long": Light.CLICK_BRIGHTNESS_DOWN,
            "double": Light.ON_FULL_BRIGHTNESS,
        }


class ShellyPlusI4LightController(LightController):
    def get_shelly_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_push_1": Light.ON,
            "long_push_1": Light.HOLD_COLOR_UP,
            "btn_up_1": Light.RELEASE,
            "double_push_1": Light.ON_FULL_COLOR_TEMP,
            "single_push_2": Light.OFF,
            "long_push_2": Light.HOLD_COLOR_DOWN,
            "btn_up_2": Light.RELEASE,
            "double_push_2": Light.ON_MIN_COLOR_TEMP,
            "single_push_3": Light.CLICK_BRIGHTNESS_UP,
            "long_push_3": Light.HOLD_BRIGHTNESS_UP,
            "btn_up_3": Light.RELEASE,
            "double_push_3": Light.ON_FULL_BRIGHTNESS,
            "single_push_4": Light.CLICK_BRIGHTNESS_DOWN,
            "long_push_4": Light.HOLD_BRIGHTNESS_DOWN,
            "btn_up_4": Light.RELEASE,
            "double_push_4": Light.ON_MIN_BRIGHTNESS,
        }


class Shelly25LightController(LightController):
    def get_shelly_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_push_1": Light.ON,
            "long_push_1": Light.HOLD_BRIGHTNESS_UP,
            "btn_up_1": Light.RELEASE,
            "double_push_1": Light.ON_FULL_BRIGHTNESS,
            "single_push_2": Light.OFF,
            "long_push_2": Light.HOLD_BRIGHTNESS_DOWN,
            "btn_up_2": Light.RELEASE,
            "double_push_2": Light.ON_MIN_BRIGHTNESS,
        }


class ShellyDimmer2LightController(LightController):
    def get_shelly_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_1": Light.TOGGLE,
            "single_2": None,
            "long_1": Light.TOGGLE,
            "long_2": None,
        }
