from core import LightController
from const import Light, TypeActionsMapping


class HueDimmerController(LightController):
    # Different states reported from the controller:
    # on-press, on-hold, on-hold-release, up-press, up-hold,
    # up-hold-release, down-press, down-hold, down-hold-release,
    # off-press, off-hold, off-hold-release

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "on-press": Light.ON,
            "on-hold": Light.HOLD_COLOR_UP,
            "on-hold-release": Light.RELEASE,
            "up-press": Light.CLICK_BRIGHTNESS_UP,
            "up-hold": Light.HOLD_BRIGHTNESS_UP,
            "up-hold-release": Light.RELEASE,
            "down-press": Light.CLICK_BRIGHTNESS_DOWN,
            "down-hold": Light.HOLD_BRIGHTNESS_DOWN,
            "down-hold-release": Light.RELEASE,
            "off-press": Light.OFF,
            "off-hold": Light.HOLD_COLOR_DOWN,
            "off-hold-release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> TypeActionsMapping:
        return {
            1000: Light.ON,
            1001: Light.HOLD_COLOR_UP,
            1003: Light.RELEASE,
            2000: Light.CLICK_BRIGHTNESS_UP,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3000: Light.CLICK_BRIGHTNESS_DOWN,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4000: Light.OFF,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
        }
