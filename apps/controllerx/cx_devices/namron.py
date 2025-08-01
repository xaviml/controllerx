from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


class Namron4512773LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_l1": Light.ON,
            "off_l1": Light.OFF,
            "brightness_move_up_l1": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l1": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l1": Light.RELEASE,
            "on_l2": Light.ON,
            "off_l2": Light.OFF,
            "brightness_move_up_l2": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l2": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l2": Light.RELEASE,
            "on_l3": Light.ON,
            "off_l3": Light.OFF,
            "brightness_move_up_l3": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l3": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l3": Light.RELEASE,
            "on_l4": Light.ON,
            "off_l4": Light.OFF,
            "brightness_move_up_l4": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l4": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l4": Light.RELEASE,
        }


class Namron4512773Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_l1": Z2MLight.ON,
            "off_l1": Z2MLight.OFF,
            "brightness_move_up_l1": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l1": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l1": Z2MLight.RELEASE,
            "on_l2": Z2MLight.ON,
            "off_l2": Z2MLight.OFF,
            "brightness_move_up_l2": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l2": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l2": Z2MLight.RELEASE,
            "on_l3": Z2MLight.ON,
            "off_l3": Z2MLight.OFF,
            "brightness_move_up_l3": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l3": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l3": Z2MLight.RELEASE,
            "on_l4": Z2MLight.ON,
            "off_l4": Z2MLight.OFF,
            "brightness_move_up_l4": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_l4": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_l4": Z2MLight.RELEASE,
        }
