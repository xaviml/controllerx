from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


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
