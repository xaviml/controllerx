from cx_const import Light, TypeActionsMapping
from cx_core import LightController
from cx_core.integration import EventData


class OsramAC025XX00NJLightController(LightController):
    # This mapping works for: AC0251100NJ / AC0251400NJ / AC0251600NJ / AC0251700NJ
    # (different models are just different colours)
    def get_zha_actions_mapping(self) -> TypeActionsMapping:
        return {
            "1_on": Light.ON,
            "1_move_with_on_off": Light.HOLD_BRIGHTNESS_UP,
            "1_stop": Light.RELEASE,
            # "3_move_to_level_with_on_off" : "", # Nothing
            "3_move_to_color_temp": Light.SYNC,
            "3_move_to_saturation": Light.HOLD_COLOR_UP,
            "3_move_hue": Light.RELEASE,
            "2_off": Light.OFF,
            "2_move": Light.HOLD_BRIGHTNESS_DOWN,
            "2_stop": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        return f"{data['endpoint_id']}_{data['command']}"


# on: Sent when arrow up is pressed
# move_with_on_off: Sent when arrow up is held
# stop: Sent when arrow up or down is released after hold
# move_to_level_with_on_off: Sent when circle button is pressed
# move_to_color_temp: Sent when circle button is released after press
# move_to_saturation: Sent when circle button is held
# move_hue: Sent when circle button is released after hold
# off: Sent when arrow down is pressed
# move: Sent when arrow down is held
