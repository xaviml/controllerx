from cx_const import Cover, DefaultActionsMapping, Light, Switch, Z2MLight
from cx_core import LightController


class TasmotaZ2MLightController(LightController):
    def get_tasmota_button_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "SINGLE": Z2MLight.TOGGLE,
            "DOUBLE": Z2MLight.ON_MIN_BRIGHTNESS,
            "TRIPLE": Z2MLight.SET_HALF_BRIGHTNESS,
            "QUAD": Z2MLight.ON_FULL_BRIGHTNESS,
            # "PENTA": "", # Nothing
            # "HOLD": "", # Nothing
        }

    def get_tasmota_switch_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Z2MLight.TOGGLE,
            "ON": Z2MLight.ON,
            "OFF": Z2MLight.OFF,
            "HOLD": Z2MLight.SET_HALF_BRIGHTNESS,
        }


class TasmotaLightController(LightController):
    def get_tasmota_button_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "SINGLE": Light.TOGGLE,
            "DOUBLE": Light.ON_MIN_BRIGHTNESS,
            "TRIPLE": Light.SET_HALF_BRIGHTNESS,
            "QUAD": Light.ON_FULL_BRIGHTNESS,
            # "PENTA": "", # Nothing
            "HOLD": Light.ON_MIN_MAX_BRIGHTNESS,
        }

    def get_tasmota_switch_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Light.TOGGLE,
            "ON": Light.ON,
            "OFF": Light.OFF,
            "HOLD": Light.ON_MIN_MAX_BRIGHTNESS,
        }


# Placeholder for Switchmode 11/12, for now Tasmota has some limitations when using this mode.
class TasmotaSM11LightController(LightController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Light.ON,
            "POWER_100": Light.RELEASE,
            "POWER_INCREMENT": Light.OFF,
            "POWER_RELEASE": Light.HOLD_COLOR_DOWN,
        }


class TasmotaSwitchController(LightController):
    def get_tasmota_button_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "SINGLE": Switch.TOGGLE,
            "DOUBLE": Switch.ON,
            "TRIPLE": Switch.OFF,
            # "QUAD": "", # Nothing
            # "PENTA": "", # Nothing
            # "HOLD": "" # Nothing
        }

    def get_tasmota_switch_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Switch.TOGGLE,
            "ON": Switch.ON,
            "OFF": Switch.OFF,
            # "HOLD": "" # Nothing
        }


class TasmotaCoverController(LightController):
    def get_tasmota_button_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "SINGLE": Cover.TOGGLE_OPEN,
            "DOUBLE": Cover.CLOSE,
            # "TRIPLE": "", # Nothing
            # "QUAD": "", # Nothing
            # "PENTA": "", # Nothing
            # "HOLD": "" # Nothing
        }

    def get_tasmota_switch_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Cover.TOGGLE_OPEN,
            "ON": Cover.OPEN,
            "OFF": Cover.CLOSE,
            "HOLD": Cover.TOGGLE_CLOSE,
        }
