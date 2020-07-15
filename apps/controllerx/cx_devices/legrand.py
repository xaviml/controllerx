from cx_const import Light, TypeActionsMapping
from cx_core import LightController


class SimpleWallSwitchController(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_zha_actions_mapping(self) -> TypeActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "move_0_255": Light.HOLD_BRIGHTNESS_UP,
            "move_1_255": Light.HOLD_BRIGHTNESS_DOWN,
            "stop": Light.RELEASE,
        }
