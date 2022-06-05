from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


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


class ROB2000070Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_1": Z2MLight.ON,
            "off_1": Z2MLight.OFF,
            "brightness_move_up_1": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_1": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_1": Z2MLight.RELEASE,
            "on_2": Z2MLight.ON,
            "off_2": Z2MLight.OFF,
            "brightness_move_up_2": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_2": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_2": Z2MLight.RELEASE,
            "on_3": Z2MLight.ON,
            "off_3": Z2MLight.OFF,
            "brightness_move_up_3": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_3": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_3": Z2MLight.RELEASE,
            "on_4": Z2MLight.ON,
            "off_4": Z2MLight.OFF,
            "brightness_move_up_4": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_4": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_4": Z2MLight.RELEASE,
        }
