from cx_const import DefaultActionsMapping, Light
from cx_core import LightController
from cx_core.integration import EventData


class OsramAC025XX00NJLightController(LightController):
    # This mapping works for: AC0251100NJ / AC0251400NJ / AC0251600NJ / AC0251700NJ
    # (different models are just different colours)

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,  # Click Arrow up
            1001: Light.HOLD_BRIGHTNESS_UP,  # Hold Arrow Up
            1003: Light.RELEASE,  # Release Arrow Up
            2002: Light.OFF,  # Click Arrow down
            2001: Light.HOLD_BRIGHTNESS_DOWN,  # Hold Arrow down
            2003: Light.RELEASE,  # Release Arrow down
            3002: Light.SYNC,  # Click Circle button
            3001: Light.HOLD_COLOR_UP,  # Hold Circle button
            3003: Light.RELEASE,  # Release Circle button
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
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
