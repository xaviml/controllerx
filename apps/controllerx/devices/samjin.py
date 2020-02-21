from core import LightController, Stepper
from const import Light

class SamjinButton(LightController):
    """
    This controller allows press, double press, and hold.
    """

    # Different states reported from the controller:
    # press, double press, hold

    def get_zha_actions_mapping(self):
        return {
            "press": Light.TOGGLE,
            "double_press": Light.ON_FULL_BRIGHTNESS,
            "long_press": Light.HOLD_BRIGHTNESS_TOGGLE,
        }
