from cx_const import DefaultActionsMapping, Light, PredefinedActionsMapping
from cx_core import LightController
from cx_core.controller import action
from cx_core.integration import EventData
from cx_core.integration.deconz import DeCONZIntegration


class MLI404011LightController(LightController):

    CHANGE_XY_COLOR = "change_xy_color"

    @action
    async def change_xy_color(self, extra: EventData) -> None:
        if isinstance(self.integration, DeCONZIntegration):
            await self.on(xy_color=extra["xy"])

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        parent_mapping = super().get_predefined_actions_mapping()
        mapping: PredefinedActionsMapping = {
            MLI404011LightController.CHANGE_XY_COLOR: self.change_xy_color,
        }
        parent_mapping.update(mapping)
        return parent_mapping

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "off": Light.TOGGLE,
            "brightness_down_click": Light.CLICK_BRIGHTNESS_DOWN,
            "brightness_down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Light.RELEASE,
            "brightness_up_click": Light.CLICK_BRIGHTNESS_UP,
            "brightness_up_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_up_release": Light.RELEASE,
            # color_temp: "" # warm or cold
            # color_wheel: "" # Color ring press
            # "scene_3": "",  # reading button
            # "scene_1": "",  # sunset button
            # "scene_2": "",  # party button
            # "scene_6": "",  # night button
            # "scene_4": "",  # fire button
            # "scene_5": "",  # heart button
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
            6002: MLI404011LightController.CHANGE_XY_COLOR,  # Color ring press
            # 7002: "",  # reading button
            # 8002: "",  # sunset button
            # 9002: "",  # party button
            # 10002: "",  # night button
            # 11002: "",  # fire button
            # 12002: "",  # heart button
        }
