from cx_const import DefaultActionsMapping, Light
from cx_core import LightController

def generate_n45127772_chanmap(index: int) -> DefaultActionsMapping:
    """Generate mapping for a namron 45127772 channel group."""
    if index not in range(1, 5):
        raise ValueError("Only values between 1 and 4 are supported.")

    return {
        f"on_l{index}": Light.ON,
        f"off_l{index}": Light.OFF,
        f"brightness_move_up_l{index}": Light.HOLD_BRIGHTNESS_UP,
        f"brightness_move_down_l{index}": Light.HOLD_BRIGHTNESS_DOWN,
        f"brightness_stop_l{index}": Light.RELEASE,
    }

class Namron4512772Controller(LightController):
    """Namron 4512772 Wall Switch with 8 buttons.

    This controller is meant to handle up to four different lights, with on/off and
    brightness up/down.

    It has swappable physical buttons, and can support 1, 2 or 4 lights.
    """

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        """Actions mapping.

        The controller is divided in to four groups all emitting the same events
        suffixed with _l1 to _l4.

        """
        mapping: DefaultActionsMapping = {}
        for n in range(1, 5):
            mapping |= generate_n45127772_chanmap(n)
        return mapping

    def default_delay(self) -> int:
        """Set a default delay.

        This gives a better dimming experience.
        """
        return 500
