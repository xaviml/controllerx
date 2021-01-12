from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class HG06323LightController(LightController):
    # Different states reported from the controller:
    # on, off, brightness_step_up, brightness_move_up,
    # brightness_step_down, brightness_move_down, brightness_stop

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "brightness_step_up": Light.CLICK_BRIGHTNESS_UP,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Light.RELEASE,
            "brightness_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "off": Light.OFF,
        }
