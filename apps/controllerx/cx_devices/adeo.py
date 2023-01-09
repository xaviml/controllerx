from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


class AdeoHRC99CZC045LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "brightness_step_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_step_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
            "color_hue_step_up": Light.HOLD_COLOR_UP,
            "color_hue_step_down": Light.HOLD_COLOR_DOWN,
            "color_saturation_step_up": Light.HOLD_COLOR_UP,
            "color_saturation_step_down": Light.HOLD_COLOR_DOWN,
            "color_temperature_step_up": Light.HOLD_COLOR_TEMP_UP,
            "color_temperature_step_down": Light.HOLD_COLOR_TEMP_DOWN,
            "color_stop": Light.RELEASE,
            "scene_1": None,
            "scene_2": None,
            "scene_3": None,
            "scene_4": None,
        }


class AdeoHRC99CZC045Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "off": Z2MLight.OFF,
            "brightness_step_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_step_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Z2MLight.RELEASE,
            "color_hue_step_up": Z2MLight.HOLD_COLOR_TEMP_UP,
            "color_hue_step_down": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "color_saturation_step_up": Z2MLight.HOLD_COLOR_TEMP_UP,
            "color_saturation_step_down": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "color_temperature_step_up": Z2MLight.HOLD_COLOR_TEMP_UP,
            "color_temperature_step_down": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "color_stop": Z2MLight.RELEASE,
            "scene_1": None,
            "scene_2": None,
            "scene_3": None,
            "scene_4": None,
        }
