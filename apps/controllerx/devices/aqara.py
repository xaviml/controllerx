from core import LightController, Stepper


class DoubleKeyWirelessController(LightController):
    """
    This controller allows click, double click, hold and release for
    both, left and the right button. All action will do the same for both, left 
    and right. Then from the apps.yaml the needed actions can be included and create
    different instances for different lights.
    """

    # Different states reported from the controller:
    # both, both_double, both_hold, both_release, right, right_double
    # right_hold, right_release left, left_double, left_hold, left_release

    def get_z2m_actions_mapping(self):
        return {
            "both": self.toggle,
            "both_double": (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
            "both_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.TOGGLE,
            ),
            "both_release": self.release,
            "left": self.toggle,
            "left_double": (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
            "left_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.TOGGLE,
            ),
            "left_release": self.release,
            "right": self.toggle,
            "right_double": (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
            "right_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.TOGGLE,
            ),
            "right_release": self.release,
        }
