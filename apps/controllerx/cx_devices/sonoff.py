from cx_const import DefaultActionsMapping, Light
from cx_core import LightController
from cx_core.integration import EventData


class SNZB01LightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": Light.TOGGLE,  # single click
            "on": Light.ON_FULL_BRIGHTNESS,  # double click
            "off": Light.ON_MIN_BRIGHTNESS,  # hold
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]
