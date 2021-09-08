from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


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
