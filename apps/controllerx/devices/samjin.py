from core import LightController, Stepper
from const import Light

class SamjinButton(LightController):
    """
    This controller allows click, double click, and hold.
    No release command is sent.
    """

    # Different states reported from the controller:
    # button_single, button_double, button_hold

    def get_zha_actions_mapping(self):
        return {
            "button_single": Light.TOGGLE,
            "button_double": Light.ON_FULL_BRIGHTNESS,
            "button_hold": Light.SET_HALF_BRIGHTNESS,
        }
