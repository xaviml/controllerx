from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class ZB5121LightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "step_with_on_off_0_32_0": Light.CLICK_BRIGHTNESS_UP,  # Click brightness up
            "move_with_on_off_0_50": Light.HOLD_BRIGHTNESS_UP,  # Hold brightness up
            "step_with_on_off_1_32_0": Light.CLICK_BRIGHTNESS_DOWN,  # Click brightness down
            "move_with_on_off_1_50": Light.HOLD_BRIGHTNESS_DOWN,  # Hold brightness down
            # "recall_0_1": "",  # Click clapperboard
            "stop": Light.RELEASE,  # long release
        }
