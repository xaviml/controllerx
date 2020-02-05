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
