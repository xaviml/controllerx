from cx_const import Light, TypeActionsMapping
from cx_core import LightController


class DoubleKeyWirelessAqaraController(LightController):
    """
    This controller allows click, double click, hold and release for
    both, left and the right button. All action will do the same for both, left
    and right. Then from the apps.yaml the needed actions can be included and create
    different instances for different lights.
    """

    # Different states reported from the controller:
    # both, both_double, both_long, right, right_double
    # right_long, left, left_double, left_long

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "both": Light.TOGGLE,
            "both_double": Light.CLICK_BRIGHTNESS_UP,
            "both_long": Light.CLICK_BRIGHTNESS_DOWN,
            "left": Light.TOGGLE,
            "left_double": Light.CLICK_BRIGHTNESS_UP,
            "left_long": Light.CLICK_BRIGHTNESS_DOWN,
            "right": Light.TOGGLE,
            "right_double": Light.CLICK_BRIGHTNESS_UP,
            "right_long": Light.CLICK_BRIGHTNESS_DOWN,
        }


class WXKG01LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, triple, quadruple,
    many, long, long_release
    """

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
            "long": Light.HOLD_BRIGHTNESS_TOGGLE,
            "long_release": Light.RELEASE,
        }


class WXKG11LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, shake, hold, release
    """

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> TypeActionsMapping:
        return {
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,
            1003: Light.RELEASE,
        }


class WXKG12LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, shake, hold, release
    """

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "shake": Light.ON_MIN_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> TypeActionsMapping:
        return {
            1002: Light.TOGGLE,  # button_1_press
            1004: Light.ON_FULL_BRIGHTNESS,  # button_1_double_press
            1006: Light.ON_MIN_BRIGHTNESS,  # button_1_shake
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

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "shake": Light.ON_MIN_BRIGHTNESS,
            "tap": Light.TOGGLE,
            "slide": Light.ON_FULL_BRIGHTNESS,
            "flip180": Light.CLICK_COLOR_UP,
            "flip90": Light.CLICK_COLOR_DOWN,
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_deconz_actions_mapping(self) -> TypeActionsMapping:
        return {
            1: Light.ON_MIN_BRIGHTNESS,
            6: Light.TOGGLE,
            5: Light.ON_FULL_BRIGHTNESS,
            4: Light.CLICK_COLOR_UP,
            3: Light.CLICK_COLOR_DOWN,
            8: Light.CLICK_BRIGHTNESS_DOWN,
            7: Light.CLICK_BRIGHTNESS_UP,
        }


class WXCJKG11LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
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
    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.ON_MIN_COLOR_TEMP,
            "button_1_hold": Light.HOLD_COLOR_DOWN,
            "button_1_release": Light.RELEASE,
            "button_2_single": Light.ON,
            "button_2_double": Light.ON_FULL_COLOR_TEMP,
            "button_2_hold": Light.HOLD_COLOR_UP,
            "button_2_release": Light.RELEASE,
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
        }


class WXCJKG13LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.SYNC,
            # "button_1_hold": "", # Nothing
            # "button_1_release": "", # Nothing
            "button_2_single": Light.ON,
            "button_2_double": Light.SYNC,
            # "button_2_hold": "", # Nothing
            # "button_2_release": "", # Nothing
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
            "button_5_single": Light.CLICK_COLOR_DOWN,
            "button_5_double": Light.ON_MIN_COLOR_TEMP,
            "button_5_hold": Light.HOLD_COLOR_DOWN,
            "button_5_release": Light.RELEASE,
            "button_6_single": Light.CLICK_COLOR_UP,
            "button_6_double": Light.ON_FULL_COLOR_TEMP,
            "button_6_hold": Light.HOLD_COLOR_UP,
            "button_6_release": Light.RELEASE,
        }
