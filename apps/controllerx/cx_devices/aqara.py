from cx_const import DefaultActionsMapping, Light, Switch
from cx_core import LightController, SwitchController
from cx_core.integration import EventData


class WXKG02LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Light.TOGGLE,
            "double_both": Light.CLICK_BRIGHTNESS_UP,
            "hold_both": Light.CLICK_BRIGHTNESS_DOWN,
            "single_left": Light.TOGGLE,
            "double_left": Light.CLICK_BRIGHTNESS_UP,
            "hold_left": Light.CLICK_BRIGHTNESS_DOWN,
            "single_right": Light.TOGGLE,
            "double_right": Light.CLICK_BRIGHTNESS_UP,
            "hold_right": Light.CLICK_BRIGHTNESS_DOWN,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,  # single left
            1001: Light.CLICK_BRIGHTNESS_DOWN,  # long left
            1004: Light.CLICK_BRIGHTNESS_UP,  # double left
            2002: Light.TOGGLE,  # single right
            2001: Light.CLICK_BRIGHTNESS_DOWN,  # long right
            2004: Light.CLICK_BRIGHTNESS_UP,  # double right
            3002: Light.TOGGLE,  # single both
            3001: Light.CLICK_BRIGHTNESS_DOWN,  # long both
            3004: Light.CLICK_BRIGHTNESS_UP,  # double both
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both_single": Light.TOGGLE,
            "both_double": Light.CLICK_BRIGHTNESS_UP,
            "both_long press": Light.CLICK_BRIGHTNESS_DOWN,
            "left_single": Light.TOGGLE,
            "left_double": Light.CLICK_BRIGHTNESS_UP,
            "left_long press": Light.CLICK_BRIGHTNESS_DOWN,
            "right_single": Light.TOGGLE,
            "right_double": Light.CLICK_BRIGHTNESS_UP,
            "right_long press": Light.CLICK_BRIGHTNESS_DOWN,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]


class WXKG02LMSwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Switch.TOGGLE,
            "single_left": Switch.TOGGLE,
            "single_right": Switch.TOGGLE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Switch.TOGGLE,
            2002: Switch.TOGGLE,
            3002: Switch.TOGGLE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both_single": Switch.TOGGLE,
            "left_single": Switch.TOGGLE,
            "right_single": Switch.TOGGLE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]


class WXKG01LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, triple, quadruple,
    many, hold, release
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
            # "many": "", # Nothing
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,  # single
            1004: Light.ON_FULL_BRIGHTNESS,  # double
            1005: Light.ON_MIN_BRIGHTNESS,  # triple
            1006: Light.SET_HALF_BRIGHTNESS,  # quadruple
            # 1010: "", # many
            1003: Light.HOLD_BRIGHTNESS_TOGGLE,  # hold the button
            1000: Light.RELEASE,  # release the button
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["args"]["click_type"]


class WXKG11LMRemoteLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,
            1003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]


class WXKG11LMSensorSwitchLightController(LightController):
    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
        }

    def get_zha_action(self, data: EventData) -> str:
        mapping = {
            1: "single",
            2: "double",
            3: "triple",
            4: "quadruple",
        }
        clicks = data["args"]["value"]
        return mapping.get(clicks, "")


class WXKG12LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, shake, hold, release
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "shake": Light.ON_MIN_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,  # button_1_press
            1004: Light.ON_FULL_BRIGHTNESS,  # button_1_double_press
            1007: Light.ON_MIN_BRIGHTNESS,  # button_1_shake
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,  # button_1_hold
            1003: Light.RELEASE,  # button_1_release_after_hold
        }


class MFKZQ01LMLightController(LightController):
    """
    This controller allows movement actions for Xiaomi Aqara Smart Cube as
    shake, wakeup, fall, slide, flip180 or 90 and rotate_left or right.
    Then from the apps.yaml the needed actions can be included and create
    different instances for different lights.
    """

    # Different states reported from the controller:
    # shake, wakeup, fall, tap, slide, flip180
    # flip90, rotate_left and rotate_right

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "shake": Light.ON_MIN_BRIGHTNESS,
            "tap": Light.TOGGLE,
            "slide": Light.ON_FULL_BRIGHTNESS,
            "flip180": Light.CLICK_COLOR_UP,
            "flip90": Light.CLICK_COLOR_DOWN,
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1: Light.ON_MIN_BRIGHTNESS,
            6: Light.TOGGLE,
            5: Light.ON_FULL_BRIGHTNESS,
            4: Light.CLICK_COLOR_UP,
            3: Light.CLICK_COLOR_DOWN,
            8: Light.CLICK_BRIGHTNESS_DOWN,
            7: Light.CLICK_BRIGHTNESS_UP,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "shake": Light.ON_MIN_BRIGHTNESS,
            "knock": Light.TOGGLE,
            "slide": Light.ON_FULL_BRIGHTNESS,
            "flip180": Light.CLICK_COLOR_UP,
            "flip90": Light.CLICK_COLOR_DOWN,
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_zha_action(self, data: EventData) -> str:
        command = action = data["command"]
        args = data.get("args", {})
        if command == "flip":
            action = command + str(args["flip_degrees"])
        return action


class WXCJKG11LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.ON_MIN_BRIGHTNESS,
            "button_1_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_1_release": Light.RELEASE,
            "button_2_single": Light.ON,
            "button_2_double": Light.ON_FULL_BRIGHTNESS,
            "button_2_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_2_release": Light.RELEASE,
        }


class WXCJKG12LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.ON_MIN_COLOR_TEMP,
            # "button_1_triple": "",
            "button_1_hold": Light.HOLD_COLOR_DOWN,
            "button_1_release": Light.RELEASE,
            "button_2_single": Light.ON,
            "button_2_double": Light.ON_FULL_COLOR_TEMP,
            # "button_2_triple": "",
            "button_2_hold": Light.HOLD_COLOR_UP,
            "button_2_release": Light.RELEASE,
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            # "button_3_triple": "",
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            # "button_4_triple": "",
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Light.OFF,
            "1_double": Light.ON_MIN_COLOR_TEMP,
            # "1_triple": "", # Nothing
            "1_long press": Light.HOLD_COLOR_DOWN,
            "1_release": Light.RELEASE,
            "2_single": Light.ON,
            "2_double": Light.ON_FULL_COLOR_TEMP,
            # "2_triple": "", # Nothing
            "2_long press": Light.HOLD_COLOR_UP,
            "2_release": Light.RELEASE,
            "3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "3_double": Light.ON_MIN_BRIGHTNESS,
            # "3_triple": "", # Nothing
            "3_long press": Light.HOLD_BRIGHTNESS_DOWN,
            "3_release": Light.RELEASE,
            "4_single": Light.CLICK_BRIGHTNESS_UP,
            "4_double": Light.ON_FULL_BRIGHTNESS,
            # "4_triple": "", # Nothing
            "4_long press": Light.HOLD_BRIGHTNESS_UP,
            "4_release": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]


class WXCJKG13LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.SYNC,
            # "button_1_triple": "", # Nothing
            # "button_1_hold": "", # Nothing
            # "button_1_release": "", # Nothing
            "button_2_single": Light.ON,
            "button_2_double": Light.SYNC,
            # "button_2_triple": "", # Nothing
            # "button_2_hold": "", # Nothing
            # "button_2_release": "", # Nothing
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            # "button_3_triple": "", # Nothing
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            # "button_4_triple": "", # Nothing
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
            "button_5_single": Light.CLICK_COLOR_DOWN,
            "button_5_double": Light.ON_MIN_COLOR_TEMP,
            # "button_5_triple": "", # Nothing
            "button_5_hold": Light.HOLD_COLOR_DOWN,
            "button_5_release": Light.RELEASE,
            "button_6_single": Light.CLICK_COLOR_UP,
            "button_6_double": Light.ON_FULL_COLOR_TEMP,
            # "button_6_triple": "", # Nothing
            "button_6_hold": Light.HOLD_COLOR_UP,
            "button_6_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.OFF,
            1004: Light.SYNC,
            # 1005: "",  # Nothing
            # 1001: "",  # Nothing
            # 1003: "",  # Nothing
            2002: Light.ON,
            2004: Light.SYNC,
            # 2005: "",  # Nothing
            # 2001: "",  # Nothing
            # 2003: "",  # Nothing
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            3004: Light.ON_MIN_BRIGHTNESS,
            # 3005: "",  # Nothing
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.CLICK_BRIGHTNESS_UP,
            4004: Light.ON_FULL_BRIGHTNESS,
            # 4005: "",  # Nothing
            4001: Light.HOLD_BRIGHTNESS_UP,
            4003: Light.RELEASE,
            5002: Light.CLICK_COLOR_DOWN,
            5004: Light.ON_MIN_COLOR_TEMP,
            # 5005: "",  # Nothing
            5001: Light.HOLD_COLOR_DOWN,
            5003: Light.RELEASE,
            6002: Light.CLICK_COLOR_UP,
            6004: Light.ON_FULL_COLOR_TEMP,
            # 6005: "",  # Nothing
            6001: Light.HOLD_COLOR_UP,
            6003: Light.RELEASE,
        }


class WXKG07LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both": Light.TOGGLE,
            "both_double": Light.CLICK_BRIGHTNESS_UP,
            "both_long": Light.CLICK_BRIGHTNESS_UP,
            "left": Light.TOGGLE,
            "left_double": Light.CLICK_BRIGHTNESS_UP,
            "left_long": Light.CLICK_BRIGHTNESS_UP,
            "right": Light.TOGGLE,
            "right_double": Light.CLICK_BRIGHTNESS_UP,
            "right_long": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,  # single left
            1001: Light.CLICK_BRIGHTNESS_DOWN,  # long left
            1004: Light.CLICK_BRIGHTNESS_UP,  # double left
            2002: Light.TOGGLE,  # single right
            2001: Light.CLICK_BRIGHTNESS_DOWN,  # long right
            2004: Light.CLICK_BRIGHTNESS_UP,  # double right
            3002: Light.TOGGLE,  # single both
            3001: Light.CLICK_BRIGHTNESS_DOWN,  # long both
            3004: Light.CLICK_BRIGHTNESS_UP,  # double both
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both_single": Light.TOGGLE,
            "both_double": Light.CLICK_BRIGHTNESS_UP,
            "both_long press": Light.CLICK_BRIGHTNESS_DOWN,
            "left_single": Light.TOGGLE,
            "left_double": Light.CLICK_BRIGHTNESS_UP,
            "left_long press": Light.CLICK_BRIGHTNESS_DOWN,
            "right_single": Light.TOGGLE,
            "right_double": Light.CLICK_BRIGHTNESS_UP,
            "right_long press": Light.CLICK_BRIGHTNESS_DOWN,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]


class WXKG07LMSwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both": Switch.TOGGLE,
            "left": Switch.TOGGLE,
            "right": Switch.TOGGLE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Switch.TOGGLE,
            2002: Switch.TOGGLE,
            3002: Switch.TOGGLE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "both_single": Switch.TOGGLE,
            "left_single": Switch.TOGGLE,
            "right_single": Switch.TOGGLE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return data["command"]
