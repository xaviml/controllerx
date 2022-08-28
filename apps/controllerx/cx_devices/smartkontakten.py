from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class SK5700002228949LightController(LightController):
    # This mapping works for: 5700002228949, 5700002228963, 5745000433087
    # The buttons are distributted like:
    # 1 3
    # 2 4

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,
            1001: Light.HOLD_BRIGHTNESS_UP,
            1003: Light.RELEASE,
            3002: Light.OFF,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            2002: Light.CLICK_COLOR_UP,
            2001: Light.HOLD_COLOR_UP,
            2003: Light.RELEASE,
            4002: Light.CLICK_COLOR_DOWN,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
        }
