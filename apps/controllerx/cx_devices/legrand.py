from cx_const import DefaultActionsMapping, Light
from cx_core import LightController
from cx_core.integration import EventData


def get_zha_action_LegrandWallController(data: dict) -> str:
    endpoint_id = data.get("endpoint_id", 1)
    command = action = data["command"]
    args = data.get("args", {})
    args_mapping = {0: "up", 1: "down"}
    if command == "move":
        action = "_".join((action, args_mapping[args[0]]))
    action = "_".join((str(endpoint_id), action))
    return action


class Legrand600083LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_on": Light.ON,
            "1_off": Light.OFF,
            "1_move_up": Light.HOLD_BRIGHTNESS_UP,
            "1_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "1_stop": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return get_zha_action_LegrandWallController(data)


class Legrand600088LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on_left": Light.ON,
            "off_left": Light.OFF,
            "brightness_move_up_left": Light.HOLD_COLOR_UP,
            "brightness_move_down_left": Light.HOLD_COLOR_DOWN,
            "brightness_stop_left": Light.RELEASE,
            "on_right": Light.ON_FULL_BRIGHTNESS,
            "off_right": Light.ON_MIN_BRIGHTNESS,
            "brightness_move_up_right": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down_right": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop_right": Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_on": Light.ON,
            "1_off": Light.OFF,
            "1_move_up": Light.HOLD_COLOR_UP,
            "1_move_down": Light.HOLD_COLOR_DOWN,
            "1_stop": Light.RELEASE,
            "2_on": Light.ON_FULL_BRIGHTNESS,
            "2_off": Light.ON_MIN_BRIGHTNESS,
            "2_move_up": Light.HOLD_BRIGHTNESS_UP,
            "2_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "2_stop": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return get_zha_action_LegrandWallController(data)
