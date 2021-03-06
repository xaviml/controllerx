from cx_const import DefaultActionsMapping, Light
from cx_core import LightController
from cx_core.integration import EventData


class AUA1ZBR2GWLightController(LightController):
    # Different states reported from the controller:
    # on, off, brightness_step_up, brightness_step_down,
    # color_temperature_step_up, color_temperature_step_down
    # There is one copy of these actions per endpoint

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_toggle": Light.TOGGLE,
            "1_step_up": Light.CLICK_BRIGHTNESS_UP,
            "1_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "1_step_color_temp_up": Light.CLICK_COLOR_TEMP_UP,
            "1_step_color_temp_down": Light.CLICK_COLOR_TEMP_DOWN,
            "2_toggle": Light.TOGGLE,
            "2_step_up": Light.CLICK_BRIGHTNESS_UP,
            "2_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "2_step_color_temp_up": Light.CLICK_COLOR_TEMP_UP,
            "2_step_color_temp_down": Light.CLICK_COLOR_TEMP_DOWN,
        }

    def get_zha_action(self, data: EventData) -> str:
        endpoint_id = data.get("endpoint_id", 1)
        command = action = data["command"]
        args = data.get("args", [])
        if command == "step" or command == "step_color_temp":
            args_mapping = {0: "up", 1: "down", 3: "up"}
            action = "_".join((action, args_mapping[args[0]]))
        if command == "on" or command == "off":
            action = "toggle"
        action = f"{endpoint_id}_{action}"
        return action
