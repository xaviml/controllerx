from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


class ZS23000278LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "brightness_step_up": Light.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_to_level": Light.BRIGHTNESS_FROM_CONTROLLER_LEVEL,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
            "color_temperature_move": Light.COLORTEMP_FROM_CONTROLLER,
            "color_temperature_move_up": Light.CLICK_COLOR_TEMP_UP,
            "color_temperature_move_down": Light.CLICK_COLOR_TEMP_DOWN,
            "color_move": Light.XYCOLOR_FROM_CONTROLLER,
        }


class ZS23000278Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "off": Z2MLight.OFF,
            "brightness_step_up": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_to_level": Z2MLight.BRIGHTNESS_FROM_CONTROLLER_LEVEL,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Z2MLight.RELEASE,
            "color_temperature_move": Z2MLight.COLORTEMP_FROM_CONTROLLER,
            "color_temperature_move_up": Z2MLight.CLICK_COLOR_TEMP_UP,
            "color_temperature_move_down": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "color_move": Z2MLight.XYCOLOR_FROM_CONTROLLER,
        }
