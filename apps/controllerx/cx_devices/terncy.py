from cx_const import Light, TypeActionsMapping
from cx_core import LightController
from cx_core.integration import EventData


class TerncyLightController(LightController):
    def get_zha_actions_mapping(self) -> TypeActionsMapping:
        return {
            "button_single": Light.TOGGLE,
            "button_double": Light.ON_FULL_BRIGHTNESS,
            "button_triple": Light.ON_MIN_BRIGHTNESS,
            "button_quadruple": Light.SET_HALF_BRIGHTNESS,
            "button_quintuple": Light.SET_HALF_BRIGHTNESS,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]

