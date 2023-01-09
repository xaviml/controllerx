from cx_const import DefaultActionsMapping, Light, Z2MLight
from cx_core import LightController, Z2MLightController
from cx_core.controller import Controller
from cx_core.integration import EventData


class MLI404011LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "brightness_down_click": Light.CLICK_BRIGHTNESS_DOWN,
            "brightness_down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Light.RELEASE,
            "brightness_up_click": Light.CLICK_BRIGHTNESS_UP,
            "brightness_up_hold": Light.HOLD_BRIGHTNESS_UP,
            "brightness_up_release": Light.RELEASE,
            "color_wheel": Light.XYCOLOR_FROM_CONTROLLER,  # Color ring press
            "color_temp": Light.COLORTEMP_FROM_CONTROLLER,  # warm or cold
            "scene_1": None,  # sunset button
            "scene_2": None,  # party button
            "scene_3": None,  # reading button
            "scene_4": None,  # fire button
            "scene_5": None,  # heart button
            "scene_6": None,  # night button
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2002: Light.CLICK_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.CLICK_COLOR_UP,
            5002: Light.CLICK_COLOR_DOWN,
            6002: Light.XYCOLOR_FROM_CONTROLLER,  # Color ring press
            7002: None,  # reading button
            8002: None,  # sunset button
            9002: None,  # party button
            10002: None,  # night button
            11002: None,  # fire button
            12002: None,  # heart button
        }


class MLI404011Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.TOGGLE,
            "off": Z2MLight.TOGGLE,
            "brightness_down_click": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "brightness_down_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Z2MLight.RELEASE,
            "brightness_up_click": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_up_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_up_release": Z2MLight.RELEASE,
            "color_wheel": Z2MLight.XYCOLOR_FROM_CONTROLLER,  # Color ring press
            "color_temp": Z2MLight.COLORTEMP_FROM_CONTROLLER,  # warm or cold
            "scene_1": None,  # sunset button
            "scene_2": None,  # party button
            "scene_3": None,  # reading button
            "scene_4": None,  # fire button
            "scene_5": None,  # heart button
            "scene_6": None,  # night button
        }


class MLI404002Controller(Controller):
    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        if command not in ("move", "step"):
            return command
        args = data["args"]
        direction_mapping = {0: "up", 1: "down"}
        return f"{command}_{direction_mapping[args[0]]}"


class MLI404002LightController(MLI404002Controller, LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "brightness_step_up": Light.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
            "recall_1": Light.ON_FULL_BRIGHTNESS,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "move_up": Light.HOLD_BRIGHTNESS_UP,
            "move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "stop": Light.RELEASE,
            "step_up": Light.CLICK_BRIGHTNESS_UP,
            "step_down": Light.CLICK_BRIGHTNESS_DOWN,
            "recall": Light.ON_FULL_BRIGHTNESS,
        }


class MLI404002Z2MLightController(MLI404002Controller, Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.TOGGLE,
            "off": Z2MLight.TOGGLE,
            "brightness_step_up": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_step_down": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Z2MLight.RELEASE,
            "recall_1": Z2MLight.ON_FULL_BRIGHTNESS,
        }
