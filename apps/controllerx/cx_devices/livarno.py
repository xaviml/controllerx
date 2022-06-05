from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController


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

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "step_0_51_10": Light.CLICK_BRIGHTNESS_UP,
            "move_0_51": Light.HOLD_BRIGHTNESS_UP,
            "stop": Light.RELEASE,
            "step_1_51_10": Light.CLICK_BRIGHTNESS_DOWN,
            "move_1_51": Light.HOLD_BRIGHTNESS_DOWN,
            "off": Light.OFF,
        }


class HG06323Z2MLightController(Z2MLightController):
    # Different states reported from the controller:
    # on, off, brightness_step_up, brightness_move_up,
    # brightness_step_down, brightness_move_down, brightness_stop

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "brightness_step_up": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Z2MLight.RELEASE,
            "brightness_step_down": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "off": Z2MLight.OFF,
        }
