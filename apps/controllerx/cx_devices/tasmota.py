from cx_const import Cover, DefaultActionsMapping, Light, Switch, Z2MLight
from cx_core import (
    CoverController,
    LightController,
    SwitchController,
    Z2MLightController,
)


class TasmotaButtonZ2MLightController(Z2MLightController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Z2MLight.TOGGLE,
            "SINGLE": Z2MLight.TOGGLE,
            "DOUBLE": Z2MLight.ON_MIN_BRIGHTNESS,
            "TRIPLE": Z2MLight.SET_HALF_BRIGHTNESS,
            "QUAD": Z2MLight.ON_FULL_BRIGHTNESS,
            "PENTA": None,
            "HOLD": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "CLEAR": Z2MLight.RELEASE,
        }


class TasmotaSwitchZ2MLightController(Z2MLightController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Z2MLight.TOGGLE,
            "ON": Z2MLight.ON,
            "OFF": Z2MLight.OFF,
            "HOLD": Z2MLight.SET_HALF_BRIGHTNESS,
        }


class TasmotaButtonLightController(LightController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Light.TOGGLE,
            "SINGLE": Light.TOGGLE,
            "DOUBLE": Light.ON_MIN_BRIGHTNESS,
            "TRIPLE": Light.SET_HALF_BRIGHTNESS,
            "QUAD": Light.ON_FULL_BRIGHTNESS,
            "PENTA": None,
            "HOLD": Light.HOLD_BRIGHTNESS_TOGGLE,
            "CLEAR": Light.RELEASE,
        }


class TasmotaSwitchLightController(LightController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Light.TOGGLE,
            "ON": Light.ON,
            "OFF": Light.OFF,
            "HOLD": Light.ON_MIN_MAX_BRIGHTNESS,
        }


class TasmotaButtonSwitchController(SwitchController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Light.TOGGLE,
            "SINGLE": Switch.TOGGLE,
            "DOUBLE": Switch.ON,
            "TRIPLE": Switch.OFF,
            "QUAD": None,
            "PENTA": None,
            "HOLD": None,
            "CLEAR": None,
        }


class TasmotaSwitchSwitchController(SwitchController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Switch.TOGGLE,
            "ON": Switch.ON,
            "OFF": Switch.OFF,
            "HOLD": None,
        }


class TasmotaButtonCoverController(CoverController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Cover.TOGGLE_OPEN,
            "SINGLE": Cover.TOGGLE_OPEN,
            "DOUBLE": Cover.CLOSE,
            "TRIPLE": None,
            "QUAD": None,
            "PENTA": None,
            "HOLD": Cover.CLOSE,
            "CLEAR": None,
        }


class TasmotaSwitchCoverController(CoverController):
    def get_tasmota_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "TOGGLE": Cover.TOGGLE_OPEN,
            "ON": Cover.OPEN,
            "OFF": Cover.CLOSE,
            "HOLD": Cover.TOGGLE_CLOSE,
        }
