from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


class E1EG7FLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "on_long": Light.CLICK_COLOR_UP,
            "on_double": Light.ON_FULL_COLOR_TEMP,
            "up": Light.CLICK_BRIGHTNESS_UP,
            "up_long": Light.ON_FULL_BRIGHTNESS,
            "down": Light.CLICK_BRIGHTNESS_DOWN,
            "down_long": Light.ON_MIN_BRIGHTNESS,
            "off": Light.OFF,
            "off_long": Light.CLICK_COLOR_DOWN,
            "off_double": Light.ON_MIN_COLOR_TEMP,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "on_long": Light.CLICK_COLOR_UP,
            "on_double": Light.ON_FULL_COLOR_TEMP,
            "step_0_1_0": Light.CLICK_BRIGHTNESS_UP,
            "step_0_2_0": Light.ON_FULL_BRIGHTNESS,
            "step_1_1_0": Light.CLICK_BRIGHTNESS_DOWN,
            "step_1_2_0": Light.ON_MIN_BRIGHTNESS,
            "off": Light.OFF,
            "off_long": Light.CLICK_COLOR_DOWN,
            "off_double": Light.ON_MIN_COLOR_TEMP,
        }


class E1EG7FZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "on_long": Z2MLight.CLICK_COLOR_TEMP_UP,
            "on_double": Z2MLight.ON_FULL_COLOR_TEMP,
            "up": Z2MLight.CLICK_BRIGHTNESS_UP,
            "up_long": Z2MLight.ON_FULL_BRIGHTNESS,
            "down": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "down_long": Z2MLight.ON_MIN_BRIGHTNESS,
            "off": Z2MLight.OFF,
            "off_long": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "off_double": Z2MLight.ON_MIN_COLOR_TEMP,
        }
