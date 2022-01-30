from cx_const import DefaultActionsMapping, Light
from cx_core import LightController


class HMPBI4FMLightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.TOGGLE,
            "PRESS_CONT_1": "",
            "PRESS_LONG_1": "",
            "PRESS_SHORT_2": Light.TOGGLE,
            "PRESS_CONT_2": "",
            "PRESS_LONG_2": "",
            "PRESS_SHORT_3": Light.TOGGLE,
            "PRESS_CONT_3": "",
            "PRESS_LONG_3": "",
            "PRESS_SHORT_4": Light.TOGGLE,
            "PRESS_CONT_4": "",
            "PRESS_LONG_4": "",
        }


class HMPB6WM55LightController(LightController):
    def get_homematic_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "PRESS_SHORT_1": Light.TOGGLE,
            "PRESS_CONT_1": "",
            "PRESS_LONG_1": "",
            "PRESS_LONG_RELEASE_1": Light.RELEASE,
            "PRESS_SHORT_2": Light.TOGGLE,
            "PRESS_CONT_2": "",
            "PRESS_LONG_2": "",
            "PRESS_LONG_RELEASE_2": Light.RELEASE,
            "PRESS_SHORT_3": Light.TOGGLE,
            "PRESS_CONT_3": "",
            "PRESS_LONG_3": "",
            "PRESS_LONG_RELEASE_3": Light.RELEASE,
            "PRESS_SHORT_4": Light.TOGGLE,
            "PRESS_CONT_4": "",
            "PRESS_LONG_4": "",
            "PRESS_LONG_RELEASE_4": Light.RELEASE,
            "PRESS_SHORT_5": Light.TOGGLE,
            "PRESS_CONT_5": "",
            "PRESS_LONG_5": "",
            "PRESS_LONG_RELEASE_5": Light.RELEASE,
            "PRESS_SHORT_6": Light.TOGGLE,
            "PRESS_CONT_6": "",
            "PRESS_LONG_6": "",
            "PRESS_LONG_RELEASE_6": Light.RELEASE,
        }
