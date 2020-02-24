from core import LightController, Stepper
from const import Light


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

    def get_z2m_actions_mapping(self):
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

    def get_z2m_actions_mapping(self):
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
            "long": Light.HOLD_BRIGHTNESS_TOGGLE,
            "long_release": Light.RELEASE,
        }


class WXKG12LMLightController(LightController):
    """
    Different states reported from the controller:
    single, double, shake, hold, release
    """

    def get_z2m_actions_mapping(self):
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "shake": Light.ON_MIN_BRIGHTNESS,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
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

    def get_z2m_actions_mapping(self):
        return {
            "shake": Light.ON_MIN_BRIGHTNESS,
            "tap": Light.TOGGLE,
            "slide": Light.ON_FULL_BRIGHTNESS,
            "flip180": Light.CLICK_COLOR_UP,
            "flip90": Light.CLICK_COLOR_DOWN,
            "rotate_left": Light.CLICK_BRIGHTNESS_DOWN,
            "rotate_right": Light.CLICK_BRIGHTNESS_UP,
        }
        
    def get_deconz_actions_mapping(self):
        return {
            1: Light.ON_MIN_BRIGHTNESS,
            6: Light.TOGGLE,
            5: Light.ON_FULL_BRIGHTNESS,
            4: Light.CLICK_COLOR_UP,
            3: Light.CLICK_COLOR_DOWN,
            8: Light.CLICK_BRIGHTNESS_DOWN,
            7: Light.CLICK_BRIGHTNESS_UP,
        }

