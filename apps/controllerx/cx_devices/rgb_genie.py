from cx_const import DefaultActionsMapping, Light
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
    @action
    async def colortemp_from_controller(self, extra: EventData) -> None:
        if isinstance(self.integration, ZHAIntegration):
            await self._on(color_temp=extra["args"][0])

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
            "move_to_color_temp": Light.COLORTEMP_FROM_CONTROLLER,  # click CW
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


class ZB3009LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
            "color_temperature_move_down": Light.CLICK_COLOR_TEMP_DOWN,
            "color_temperature_move_up": Light.CLICK_COLOR_TEMP_UP,
            "color_temperature_move": Light.COLORTEMP_FROM_CONTROLLER,
            "color_move": Light.XYCOLOR_FROM_CONTROLLER,
            # "hue_move": "",  # Play/pause button
            # "recall_1": "",  # Scene 1
            # "recall_3": "",  # Scene 2
            # "recall_2": "",  # Scene 3
        }
