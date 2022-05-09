from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class ROB2000070LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_1": Light.ON,
            "off_1": Light.OFF,
            "brightness_move_up_1": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_1": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_1": Light.RELEASE,
            "on_2": Light.ON,
            "off_2": Light.OFF,
            "brightness_move_up_2": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_2": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_2": Light.RELEASE,
            "on_3": Light.ON,
            "off_3": Light.OFF,
            "brightness_move_up_3": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_3": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_3": Light.RELEASE,
            "on_4": Light.ON,
            "off_4": Light.OFF,
            "brightness_move_up_4": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_4": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_4": Light.RELEASE,
        }
