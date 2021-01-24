from cx_const import DefaultActionsMapping, Light, PredefinedActionsMapping
from cx_core import LightController
from cx_core.controller import action
from cx_core.integration import EventData
from cx_core.integration.zha import ZHAIntegration


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


class ZB5122LightController(LightController):

    MOVE_TO_COLOR_TEMP = "move_to_color_temp"

    @action
    async def move_to_color_temp(self, extra: EventData) -> None:
        if isinstance(self.integration, ZHAIntegration):
            await self.on(color_temp=extra["args"][0])

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        parent_mapping = super().get_predefined_actions_mapping()
        mapping: PredefinedActionsMapping = {
            ZB5122LightController.MOVE_TO_COLOR_TEMP: self.move_to_color_temp,
        }
        parent_mapping.update(mapping)
        return parent_mapping

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,  # Click light on
            "off": Light.OFF,  # Click light off
            "hold_brightness_up": Light.HOLD_BRIGHTNESS_UP,  # Hold light on
            "hold_brightness_down": Light.HOLD_BRIGHTNESS_DOWN,  # Hold light off
            "stop": Light.RELEASE,  # long release
            "move_to_color": Light.CLICK_XY_COLOR_UP,  # click RGB
            "move_hue": Light.HOLD_XY_COLOR_UP,  # hold RGB
            "stop_move_hue": Light.RELEASE,  # release RGB
            "move_to_color_temp": ZB5122LightController.MOVE_TO_COLOR_TEMP,  # click CW
            "move_color_temp": Light.HOLD_COLOR_TEMP_TOGGLE,  # hold CW
            "stop_move_step": Light.RELEASE,  # release CW
            # "recall_0_1": "",  # Click clapperboard
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        if command == "move_with_on_off":
            return (
                "hold_brightness_up" if data["args"][0] == 0 else "hold_brightness_down"
            )
        elif command == "move_hue":
            return "stop_move_hue" if tuple(data["args"]) == (0, 0) else "move_hue"
        return command
