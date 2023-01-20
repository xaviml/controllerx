from cx_const import DefaultActionsMapping, Light, MediaPlayer, Switch, Z2MLight
from cx_core import (
    LightController,
    MediaPlayerController,
    SwitchController,
    Z2MLightController,
)
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
        command: str = data["command"]
        return command


class WXKG02LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Z2MLight.TOGGLE,
            "double_both": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_both": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "single_left": Z2MLight.TOGGLE,
            "double_left": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_left": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "single_right": Z2MLight.TOGGLE,
            "double_right": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_right": Z2MLight.CLICK_BRIGHTNESS_DOWN,
        }


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
        command: str = data["command"]
        return command


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
            "many": None,
            "hold": Light.HOLD_BRIGHTNESS_TOGGLE,
            "release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,  # single
            1004: Light.ON_FULL_BRIGHTNESS,  # double
            1005: Light.ON_MIN_BRIGHTNESS,  # triple
            1006: Light.SET_HALF_BRIGHTNESS,  # quadruple
            1010: None,  # many
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,  # hold the button
            1003: Light.RELEASE,  # release the button
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "triple": Light.ON_MIN_BRIGHTNESS,
            "quadruple": Light.SET_HALF_BRIGHTNESS,
        }

    def get_zha_action(self, data: EventData) -> str:
        args = data["args"]
        if "click_type" in args:
            return args["click_type"]
        return data["command"]


class WXKG01LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Z2MLight.TOGGLE,
            "double": Z2MLight.ON_FULL_BRIGHTNESS,
            "triple": Z2MLight.ON_MIN_BRIGHTNESS,
            "quadruple": Z2MLight.SET_HALF_BRIGHTNESS,
            "many": None,
            "hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "release": Z2MLight.RELEASE,
        }


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
        command: str = data["command"]
        return command


class WXKG11LMRemoteZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Z2MLight.TOGGLE,
            "double": Z2MLight.ON_FULL_BRIGHTNESS,
            "hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "release": Z2MLight.RELEASE,
        }


class WXKG11LMSensorSwitchLightController(LightController):
    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
            1005: Light.ON_MIN_BRIGHTNESS,
            1006: Light.SET_HALF_BRIGHTNESS,
        }

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


class WXKG12LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Z2MLight.TOGGLE,
            "double": Z2MLight.ON_FULL_BRIGHTNESS,
            "shake": Z2MLight.ON_MIN_BRIGHTNESS,
            "hold": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "release": Z2MLight.RELEASE,
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
        command: str = data["command"]
        action = command
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

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.OFF,
            1001: Light.HOLD_BRIGHTNESS_DOWN,
            1003: Light.RELEASE,
            2002: Light.ON,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
        }


class WXCJKG11LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Z2MLight.OFF,
            "button_1_double": Z2MLight.ON_MIN_BRIGHTNESS,
            "button_1_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "button_1_release": Z2MLight.RELEASE,
            "button_2_single": Z2MLight.ON,
            "button_2_double": Z2MLight.ON_FULL_BRIGHTNESS,
            "button_2_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "button_2_release": Z2MLight.RELEASE,
        }


class WXCJKG12LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.ON_MIN_COLOR_TEMP,
            "button_1_triple": None,
            "button_1_hold": Light.HOLD_COLOR_DOWN,
            "button_1_release": Light.RELEASE,
            "button_2_single": Light.ON,
            "button_2_double": Light.ON_FULL_COLOR_TEMP,
            "button_2_triple": None,
            "button_2_hold": Light.HOLD_COLOR_UP,
            "button_2_release": Light.RELEASE,
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            "button_3_triple": None,
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            "button_4_triple": None,
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Light.OFF,
            "1_double": Light.ON_MIN_COLOR_TEMP,
            "1_triple": None,
            "1_long press": Light.HOLD_COLOR_DOWN,
            "1_release": Light.RELEASE,
            "2_single": Light.ON,
            "2_double": Light.ON_FULL_COLOR_TEMP,
            "2_triple": None,
            "2_long press": Light.HOLD_COLOR_UP,
            "2_release": Light.RELEASE,
            "3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "3_double": Light.ON_MIN_BRIGHTNESS,
            "3_triple": None,
            "3_long press": Light.HOLD_BRIGHTNESS_DOWN,
            "3_release": Light.RELEASE,
            "4_single": Light.CLICK_BRIGHTNESS_UP,
            "4_double": Light.ON_FULL_BRIGHTNESS,
            "4_triple": None,
            "4_long press": Light.HOLD_BRIGHTNESS_UP,
            "4_release": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class WXCJKG12LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Z2MLight.OFF,
            "button_1_double": Z2MLight.ON_MIN_COLOR_TEMP,
            "button_1_triple": None,
            "button_1_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "button_1_release": Z2MLight.RELEASE,
            "button_2_single": Z2MLight.ON,
            "button_2_double": Z2MLight.ON_FULL_COLOR_TEMP,
            "button_2_triple": None,
            "button_2_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "button_2_release": Z2MLight.RELEASE,
            "button_3_single": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Z2MLight.ON_MIN_BRIGHTNESS,
            "button_3_triple": None,
            "button_3_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Z2MLight.RELEASE,
            "button_4_single": Z2MLight.CLICK_BRIGHTNESS_UP,
            "button_4_double": Z2MLight.ON_FULL_BRIGHTNESS,
            "button_4_triple": None,
            "button_4_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "button_4_release": Z2MLight.RELEASE,
        }


class WXCJKG13LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Light.OFF,
            "button_1_double": Light.SYNC,
            "button_1_triple": None,
            "button_1_hold": None,
            "button_1_release": None,
            "button_2_single": Light.ON,
            "button_2_double": Light.SYNC,
            "button_2_triple": None,
            "button_2_hold": None,
            "button_2_release": None,
            "button_3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Light.ON_MIN_BRIGHTNESS,
            "button_3_triple": None,
            "button_3_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Light.RELEASE,
            "button_4_single": Light.CLICK_BRIGHTNESS_UP,
            "button_4_double": Light.ON_FULL_BRIGHTNESS,
            "button_4_triple": None,
            "button_4_hold": Light.HOLD_BRIGHTNESS_UP,
            "button_4_release": Light.RELEASE,
            "button_5_single": Light.CLICK_COLOR_DOWN,
            "button_5_double": Light.ON_MIN_COLOR_TEMP,
            "button_5_triple": None,
            "button_5_hold": Light.HOLD_COLOR_DOWN,
            "button_5_release": Light.RELEASE,
            "button_6_single": Light.CLICK_COLOR_UP,
            "button_6_double": Light.ON_FULL_COLOR_TEMP,
            "button_6_triple": None,
            "button_6_hold": Light.HOLD_COLOR_UP,
            "button_6_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.OFF,
            1004: Light.SYNC,
            1005: None,
            1001: None,
            1003: None,
            2002: Light.ON,
            2004: Light.SYNC,
            2005: None,
            2001: None,
            2003: None,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            3004: Light.ON_MIN_BRIGHTNESS,
            3005: None,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4002: Light.CLICK_BRIGHTNESS_UP,
            4004: Light.ON_FULL_BRIGHTNESS,
            4005: None,
            4001: Light.HOLD_BRIGHTNESS_UP,
            4003: Light.RELEASE,
            5002: Light.CLICK_COLOR_DOWN,
            5004: Light.ON_MIN_COLOR_TEMP,
            5005: None,
            5001: Light.HOLD_COLOR_DOWN,
            5003: Light.RELEASE,
            6002: Light.CLICK_COLOR_UP,
            6004: Light.ON_FULL_COLOR_TEMP,
            6005: None,
            6001: Light.HOLD_COLOR_UP,
            6003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": Light.OFF,
            "1_double": Light.SYNC,
            "1_triple": None,
            "1_long": None,
            "1_release": None,
            "2_single": Light.ON,
            "2_double": Light.SYNC,
            "2_triple": None,
            "2_long": None,
            "2_release": None,
            "3_single": Light.CLICK_BRIGHTNESS_DOWN,
            "3_double": Light.ON_MIN_BRIGHTNESS,
            "3_triple": None,
            "3_long": Light.HOLD_BRIGHTNESS_DOWN,
            "3_release": Light.RELEASE,
            "4_single": Light.CLICK_BRIGHTNESS_UP,
            "4_double": Light.ON_FULL_BRIGHTNESS,
            "4_triple": None,
            "4_long": Light.HOLD_BRIGHTNESS_UP,
            "4_release": Light.RELEASE,
            "5_single": Light.CLICK_COLOR_DOWN,
            "5_double": Light.ON_MIN_COLOR_TEMP,
            "5_triple": None,
            "5_long": Light.HOLD_COLOR_DOWN,
            "5_release": Light.RELEASE,
            "6_single": Light.CLICK_COLOR_UP,
            "6_double": Light.ON_FULL_COLOR_TEMP,
            "6_triple": None,
            "6_long": Light.HOLD_COLOR_UP,
            "6_release": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class WXCJKG13LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": Z2MLight.OFF,
            "button_1_double": Z2MLight.ON_FULL_BRIGHTNESS,
            "button_1_triple": None,
            "button_1_hold": None,
            "button_1_release": None,
            "button_2_single": Z2MLight.ON,
            "button_2_double": Z2MLight.ON_FULL_BRIGHTNESS,
            "button_2_triple": None,
            "button_2_hold": None,
            "button_2_release": None,
            "button_3_single": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "button_3_double": Z2MLight.ON_MIN_BRIGHTNESS,
            "button_3_triple": None,
            "button_3_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "button_3_release": Z2MLight.RELEASE,
            "button_4_single": Z2MLight.CLICK_BRIGHTNESS_UP,
            "button_4_double": Z2MLight.ON_FULL_BRIGHTNESS,
            "button_4_triple": None,
            "button_4_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "button_4_release": Z2MLight.RELEASE,
            "button_5_single": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "button_5_double": Z2MLight.ON_MIN_COLOR_TEMP,
            "button_5_triple": None,
            "button_5_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "button_5_release": Z2MLight.RELEASE,
            "button_6_single": Z2MLight.CLICK_COLOR_TEMP_UP,
            "button_6_double": Z2MLight.ON_FULL_COLOR_TEMP,
            "button_6_triple": None,
            "button_6_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "button_6_release": Z2MLight.RELEASE,
        }


class WXCJKG13LMMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "button_1_single": MediaPlayer.CLICK_VOLUME_DOWN,
            "button_1_double": MediaPlayer.MUTE,
            "button_1_triple": None,
            "button_1_hold": MediaPlayer.HOLD_VOLUME_DOWN,
            "button_1_release": MediaPlayer.RELEASE,
            "button_2_single": MediaPlayer.CLICK_VOLUME_UP,
            "button_2_double": MediaPlayer.PLAY_PAUSE,
            "button_2_triple": None,
            "button_2_hold": MediaPlayer.HOLD_VOLUME_UP,
            "button_2_release": MediaPlayer.RELEASE,
            "button_3_single": MediaPlayer.PREVIOUS_TRACK,
            "button_3_double": None,
            "button_3_triple": None,
            "button_3_hold": None,
            "button_3_release": None,
            "button_4_single": MediaPlayer.NEXT_TRACK,
            "button_4_double": None,
            "button_4_triple": None,
            "button_4_hold": None,
            "button_4_release": None,
            "button_5_single": MediaPlayer.PREVIOUS_SOURCE,
            "button_5_double": None,
            "button_5_triple": None,
            "button_5_hold": None,
            "button_5_release": None,
            "button_6_single": MediaPlayer.NEXT_SOURCE,
            "button_6_double": None,
            "button_6_triple": None,
            "button_6_hold": None,
            "button_6_release": None,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        #######################
        # Button layout
        #######################
        # 1000: top-left
        # 2000: top-right
        # 3000: middle-left
        # 4000: middle-right
        # 5000: bottom-left
        # 6000: bottom-right
        #######################
        # Actions
        #######################
        # 0001: hold
        # 0002: click
        # 0003: release
        # 0004: double-click
        # 0005: triple-click
        #######################
        return {
            1002: MediaPlayer.CLICK_VOLUME_DOWN,
            1001: MediaPlayer.HOLD_VOLUME_DOWN,
            1003: MediaPlayer.RELEASE,
            1004: MediaPlayer.MUTE,
            1005: None,
            2002: MediaPlayer.CLICK_VOLUME_UP,
            2001: MediaPlayer.HOLD_VOLUME_UP,
            2003: MediaPlayer.RELEASE,
            2004: MediaPlayer.PLAY_PAUSE,
            2005: None,
            3002: MediaPlayer.PREVIOUS_TRACK,
            3001: None,
            3003: None,
            3004: None,
            3005: None,
            4002: MediaPlayer.NEXT_TRACK,
            4001: None,
            4003: None,
            4004: None,
            4005: None,
            5002: MediaPlayer.PREVIOUS_SOURCE,
            5001: None,
            5003: None,
            5004: None,
            5005: None,
            6002: MediaPlayer.NEXT_SOURCE,
            6001: None,
            6003: None,
            6004: None,
            6005: None,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_single": MediaPlayer.CLICK_VOLUME_DOWN,
            "1_double": MediaPlayer.MUTE,
            "1_triple": None,
            "1_long": MediaPlayer.HOLD_VOLUME_DOWN,
            "1_release": MediaPlayer.RELEASE,
            "2_single": MediaPlayer.CLICK_VOLUME_UP,
            "2_double": MediaPlayer.PLAY_PAUSE,
            "2_triple": None,
            "2_long": MediaPlayer.HOLD_VOLUME_UP,
            "2_release": MediaPlayer.RELEASE,
            "3_single": MediaPlayer.PREVIOUS_TRACK,
            "3_double": None,
            "3_triple": None,
            "3_long": None,
            "3_release": None,
            "4_single": MediaPlayer.NEXT_TRACK,
            "4_double": None,
            "4_triple": None,
            "4_long": None,
            "4_release": None,
            "5_single": MediaPlayer.PREVIOUS_SOURCE,
            "5_double": None,
            "5_triple": None,
            "5_long": None,
            "5_release": Light.RELEASE,
            "6_single": MediaPlayer.NEXT_SOURCE,
            "6_double": None,
            "6_triple": None,
            "6_long": None,
            "6_release": None,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class WXKG06LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.CLICK_BRIGHTNESS_UP,
            "hold": Light.CLICK_BRIGHTNESS_UP,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1001: Light.CLICK_BRIGHTNESS_DOWN,
            1004: Light.CLICK_BRIGHTNESS_UP,
        }


class WXKG06LMSwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"single": Light.TOGGLE}

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {1002: Light.TOGGLE}


class WXKG07LMLightController(LightController):
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
            1001: Light.CLICK_BRIGHTNESS_DOWN,  # long left
            1002: Light.TOGGLE,  # single left
            1004: Light.CLICK_BRIGHTNESS_UP,  # double left
            2001: Light.CLICK_BRIGHTNESS_DOWN,  # long right
            2002: Light.TOGGLE,  # single right
            2004: Light.CLICK_BRIGHTNESS_UP,  # double right
            3001: Light.CLICK_BRIGHTNESS_DOWN,  # long both
            3002: Light.TOGGLE,  # single both
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
        command: str = data["command"]
        return command


class WXKG07LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Z2MLight.TOGGLE,
            "double_both": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_both": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "single_left": Z2MLight.TOGGLE,
            "double_left": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_left": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "single_right": Z2MLight.TOGGLE,
            "double_right": Z2MLight.CLICK_BRIGHTNESS_UP,
            "hold_right": Z2MLight.CLICK_BRIGHTNESS_DOWN,
        }


class WXKG07LMSwitchController(SwitchController):
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
        command: str = data["command"]
        return command


class ZNXNKG02LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": Light.TOGGLE,
            "double": Light.ON_FULL_BRIGHTNESS,
            "hold": Light.HOLD_COLOR_TOGGLE,
            "release": Light.RELEASE,
            "start_rotating": Light.BRIGHTNESS_FROM_CONTROLLER_ANGLE,
            "stop_rotating": Light.RELEASE,
        }


class ZNXNKG02LMMediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single": MediaPlayer.PLAY_PAUSE,
            "double": MediaPlayer.NEXT_TRACK,
            "hold": MediaPlayer.PREVIOUS_TRACK,
            "release": MediaPlayer.RELEASE,
            "start_rotating": MediaPlayer.VOLUME_FROM_CONTROLLER_ANGLE,
            "stop_rotating": MediaPlayer.RELEASE,
        }


class WXKG15LMLightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Light.TOGGLE,
            "double_both": Light.CLICK_BRIGHTNESS_UP,
            "triple_both": Light.CLICK_BRIGHTNESS_DOWN,
            "hold_both": Light.ON_FULL_BRIGHTNESS,
            "single_left": Light.TOGGLE,
            "double_left": Light.CLICK_BRIGHTNESS_UP,
            "triple_left": Light.CLICK_BRIGHTNESS_DOWN,
            "hold_left": Light.ON_FULL_BRIGHTNESS,
            "single_right": Light.TOGGLE,
            "double_right": Light.CLICK_BRIGHTNESS_UP,
            "triple_right": Light.CLICK_BRIGHTNESS_DOWN,
            "hold_right": Light.ON_FULL_BRIGHTNESS,
        }


class WXKG15LMZ2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Z2MLight.TOGGLE,
            "double_both": Z2MLight.CLICK_BRIGHTNESS_UP,
            "triple_both": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "hold_both": Z2MLight.ON_FULL_BRIGHTNESS,
            "single_left": Z2MLight.TOGGLE,
            "double_left": Z2MLight.CLICK_BRIGHTNESS_UP,
            "triple_left": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "hold_left": Z2MLight.ON_FULL_BRIGHTNESS,
            "single_right": Z2MLight.TOGGLE,
            "double_right": Z2MLight.CLICK_BRIGHTNESS_UP,
            "triple_right": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "hold_right": Z2MLight.ON_FULL_BRIGHTNESS,
        }


class WXKG15LMSwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "single_both": Switch.TOGGLE,
            "single_left": Switch.TOGGLE,
            "single_right": Switch.TOGGLE,
        }
