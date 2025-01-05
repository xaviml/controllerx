from cx_const import (
    Cover,
    DefaultActionsMapping,
    Light,
    MediaPlayer,
    PredefinedActionsMapping,
    Switch,
    Z2MLight,
)
from cx_core import (
    CoverController,
    LightController,
    MediaPlayerController,
    SwitchController,
    Z2MLightController,
    action,
)
from cx_core.integration import EventData


class E1810Controller(LightController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": Light.TOGGLE,
            "toggle_hold": Light.SYNC,
            "brightness_up_click": Light.CLICK_BRIGHTNESS_UP,
            "brightness_down_click": Light.CLICK_BRIGHTNESS_DOWN,
            "arrow_left_click": Light.CLICK_COLOR_DOWN,
            "arrow_right_click": Light.CLICK_COLOR_UP,
            "brightness_up_hold": Light.HOLD_BRIGHTNESS_UP,
            "brightness_up_release": Light.RELEASE,
            "brightness_down_hold": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Light.RELEASE,
            "arrow_left_hold": Light.HOLD_COLOR_DOWN,
            "arrow_left_release": Light.RELEASE,
            "arrow_right_hold": Light.HOLD_COLOR_UP,
            "arrow_right_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1001: Light.SYNC,
            2002: Light.CLICK_BRIGHTNESS_UP,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            4002: Light.CLICK_COLOR_DOWN,
            5002: Light.CLICK_COLOR_UP,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            3003: Light.RELEASE,
            4001: Light.HOLD_COLOR_DOWN,
            4003: Light.RELEASE,
            5001: Light.HOLD_COLOR_UP,
            5003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": Light.TOGGLE,
            "press_2_0_0": Light.SYNC,
            "step_with_on_off_0_43_5": Light.CLICK_BRIGHTNESS_UP,
            "step_1_43_5_0_0": Light.CLICK_BRIGHTNESS_DOWN,
            "press_257_13_0": Light.CLICK_COLOR_DOWN,
            "press_256_13_0": Light.CLICK_COLOR_UP,
            "move_with_on_off_0_83": Light.HOLD_BRIGHTNESS_UP,
            "move_with_on_off_0_84": Light.HOLD_BRIGHTNESS_UP,  # ZigBee 3.0 firmware
            "move_1_83_0_0": Light.HOLD_BRIGHTNESS_DOWN,
            "move_1_84_0_0": Light.HOLD_BRIGHTNESS_DOWN,  # ZigBee 3.0 firmware
            "hold_3329_0": Light.HOLD_COLOR_DOWN,
            "hold_3328_0": Light.HOLD_COLOR_UP,
            "stop": Light.RELEASE,
            "stop_with_on_off": Light.RELEASE,
            "release": Light.RELEASE,
        }


class E1810Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": Z2MLight.TOGGLE,
            "toggle_hold": Z2MLight.ON_FULL_BRIGHTNESS,
            "brightness_up_click": Z2MLight.CLICK_BRIGHTNESS_UP,
            "brightness_down_click": Z2MLight.CLICK_BRIGHTNESS_DOWN,
            "arrow_left_click": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "arrow_right_click": Z2MLight.CLICK_COLOR_TEMP_UP,
            "brightness_up_hold": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_up_release": Z2MLight.RELEASE,
            "brightness_down_hold": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_down_release": Z2MLight.RELEASE,
            "arrow_left_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "arrow_left_release": Z2MLight.RELEASE,
            "arrow_right_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "arrow_right_release": Z2MLight.RELEASE,
        }


class E1810MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,
            "brightness_up_click": MediaPlayer.CLICK_VOLUME_UP,
            "brightness_down_click": MediaPlayer.CLICK_VOLUME_DOWN,
            "arrow_left_click": MediaPlayer.PREVIOUS_TRACK,
            "arrow_right_click": MediaPlayer.NEXT_TRACK,
            "arrow_left_hold": MediaPlayer.PREVIOUS_SOURCE,
            "arrow_right_hold": MediaPlayer.NEXT_SOURCE,
            "brightness_up_hold": MediaPlayer.HOLD_VOLUME_UP,
            "brightness_up_release": MediaPlayer.RELEASE,
            "brightness_down_hold": MediaPlayer.HOLD_VOLUME_DOWN,
            "brightness_down_release": MediaPlayer.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: MediaPlayer.PLAY_PAUSE,
            2002: MediaPlayer.CLICK_VOLUME_UP,
            3002: MediaPlayer.CLICK_VOLUME_DOWN,
            4002: MediaPlayer.PREVIOUS_TRACK,
            5002: MediaPlayer.NEXT_TRACK,
            2001: MediaPlayer.HOLD_VOLUME_UP,
            2003: MediaPlayer.RELEASE,
            3001: MediaPlayer.HOLD_VOLUME_DOWN,
            3003: MediaPlayer.RELEASE,
            4001: MediaPlayer.PREVIOUS_SOURCE,
            5001: MediaPlayer.NEXT_SOURCE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,
            "step_with_on_off_0_43_5": MediaPlayer.CLICK_VOLUME_UP,
            "step_1_43_5_0_0": MediaPlayer.CLICK_VOLUME_DOWN,
            "press_257_13_0": MediaPlayer.PREVIOUS_TRACK,
            "press_256_13_0": MediaPlayer.NEXT_TRACK,
            "move_with_on_off_0_83": MediaPlayer.HOLD_VOLUME_UP,
            "move_with_on_off_0_84": MediaPlayer.HOLD_VOLUME_UP,  # ZigBee 3.0 firmware
            "stop": MediaPlayer.RELEASE,
            "stop_with_on_off": MediaPlayer.RELEASE,
            "move_1_83_0_0": MediaPlayer.HOLD_VOLUME_DOWN,
            "move_1_84_0_0": MediaPlayer.HOLD_VOLUME_DOWN,  # ZigBee 3.0 firmware
            "hold_3329_0": MediaPlayer.PREVIOUS_SOURCE,
            "hold_3328_0": MediaPlayer.NEXT_SOURCE,
            "release": MediaPlayer.RELEASE,
        }


class E1743Controller(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,
            2002: Light.OFF,
            1001: Light.HOLD_BRIGHTNESS_UP,
            2001: Light.HOLD_BRIGHTNESS_DOWN,
            1003: Light.RELEASE,
            2003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "move_with_on_off_0_83": Light.HOLD_BRIGHTNESS_UP,
            "move_1_83_0_0": Light.HOLD_BRIGHTNESS_DOWN,
            "stop": Light.RELEASE,
            "stop_with_on_off": Light.RELEASE,
        }


class E1743Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "off": Z2MLight.OFF,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Z2MLight.RELEASE,
        }


class E1743MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": MediaPlayer.PLAY_PAUSE,
            "off": MediaPlayer.NEXT_TRACK,
            "brightness_move_up": MediaPlayer.HOLD_VOLUME_UP,
            "brightness_move_down": MediaPlayer.HOLD_VOLUME_DOWN,
            "brightness_stop": MediaPlayer.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: MediaPlayer.PLAY_PAUSE,
            2002: MediaPlayer.NEXT_TRACK,
            1001: MediaPlayer.HOLD_VOLUME_UP,
            2001: MediaPlayer.HOLD_VOLUME_DOWN,
            1003: MediaPlayer.RELEASE,
            2003: MediaPlayer.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": MediaPlayer.PLAY_PAUSE,
            "off": MediaPlayer.NEXT_TRACK,
            "move_with_on_off_0_83": MediaPlayer.HOLD_VOLUME_UP,
            "move_1_83_0_0": MediaPlayer.HOLD_VOLUME_DOWN,
            "stop": MediaPlayer.RELEASE,
            "stop_with_on_off": MediaPlayer.RELEASE,
        }


class E1743SwitchController(SwitchController):
    # Different states reported from the controller:
    # on, off

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"on": Switch.ON, "off": Switch.OFF}

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {1002: Switch.ON, 2002: Switch.OFF}

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {"on": Switch.ON, "off": Switch.OFF}


class E1743CoverController(CoverController):
    # Different states reported from the controller:
    # on, off

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Cover.TOGGLE_OPEN,
            "off": Cover.TOGGLE_CLOSE,
            "brightness_move_up": Cover.OPEN,
            "brightness_move_down": Cover.CLOSE,
            "brightness_stop": Cover.STOP,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Cover.TOGGLE_OPEN,
            2002: Cover.TOGGLE_CLOSE,
            1001: Cover.OPEN,
            2001: Cover.CLOSE,
            1003: Cover.STOP,
            2003: Cover.STOP,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Cover.TOGGLE_OPEN,
            "off": Cover.TOGGLE_CLOSE,
            "move_with_on_off_0_83": Cover.OPEN,
            "move_1_83_0_0": Cover.CLOSE,
            "stop": Cover.STOP,
            "stop_with_on_off": Cover.STOP,
        }


class ICTCG1Controller(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_left_quick
    # rotate_right, rotate_right_quick
    # rotate_stop

    @action
    async def rotate_left_quick(self) -> None:
        await self.release()
        await self.off()

    @action
    async def rotate_right_quick(self) -> None:
        await self.release()
        await self.on_full(LightController.ATTRIBUTE_BRIGHTNESS)

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        parent_mapping = super().get_predefined_actions_mapping()
        mapping: PredefinedActionsMapping = {
            "rotate_left_quick": self.rotate_left_quick,
            "rotate_right_quick": self.rotate_right_quick,
        }
        mapping.update(parent_mapping)
        return mapping

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Light.RELEASE,
            "brightness_move_to_level": Light.BRIGHTNESS_FROM_CONTROLLER_LEVEL,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: "rotate_right_quick",
            2002: Light.CLICK_BRIGHTNESS_UP,
            3002: Light.CLICK_BRIGHTNESS_DOWN,
            4002: "rotate_left_quick",
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "move_1_70": Light.HOLD_BRIGHTNESS_DOWN,
            "move_1_195": Light.HOLD_BRIGHTNESS_DOWN,
            "move_to_level_with_on_off_0_1": "rotate_left_quick",
            "move_with_on_off_0_70": Light.HOLD_BRIGHTNESS_UP,
            "move_with_on_off_0_195": Light.ON,
            "move_to_level_with_on_off_255_1": "rotate_right_quick",
            "stop": Light.RELEASE,
        }


class ICTCG1Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_stop": Z2MLight.RELEASE,
            "brightness_move_to_level": Z2MLight.BRIGHTNESS_FROM_CONTROLLER_LEVEL,
        }


class ICTCG1MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # rotate_left, rotate_left_quick
    # rotate_right, rotate_right_quick
    # rotate_stop

    @action
    async def rotate_left_quick(self) -> None:
        await self.release()
        await self.pause()

    @action
    async def rotate_right_quick(self) -> None:
        await self.release()
        await self.play()

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        parent_mapping = super().get_predefined_actions_mapping()
        mapping: PredefinedActionsMapping = {
            "rotate_left_quick": self.rotate_left_quick,
            "rotate_right_quick": self.rotate_right_quick,
        }
        mapping.update(parent_mapping)
        return mapping

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_up": MediaPlayer.HOLD_VOLUME_UP,
            "brightness_move_down": MediaPlayer.HOLD_VOLUME_DOWN,
            "brightness_stop": MediaPlayer.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: "rotate_right_quick",
            2002: MediaPlayer.CLICK_VOLUME_UP,
            3002: MediaPlayer.CLICK_VOLUME_DOWN,
            4002: "rotate_left_quick",
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "move_1_70": MediaPlayer.HOLD_VOLUME_DOWN,
            "move_1_195": MediaPlayer.HOLD_VOLUME_DOWN,
            "move_to_level_with_on_off_0_1": "rotate_left_quick",
            "move_with_on_off_0_70": MediaPlayer.HOLD_VOLUME_UP,
            "move_with_on_off_0_195": MediaPlayer.HOLD_VOLUME_UP,
            "move_to_level_with_on_off_255_1": "rotate_right_quick",
            "stop": MediaPlayer.RELEASE,
        }


class E1744LightController(LightController):
    # Different states reported from the controller:
    # brightness_move_down, brightness_move_up, brightness_stop,
    # toggle, brightness_step_up, brightness_step_down

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Light.RELEASE,
            "toggle": Light.TOGGLE,
            "brightness_step_up": Light.ON_FULL_BRIGHTNESS,
            "brightness_step_down": Light.ON_MIN_BRIGHTNESS,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            3001: Light.HOLD_BRIGHTNESS_DOWN,
            2001: Light.HOLD_BRIGHTNESS_UP,
            2003: Light.RELEASE,
            3003: Light.RELEASE,
            1002: Light.TOGGLE,
            1004: Light.ON_FULL_BRIGHTNESS,
            1005: Light.ON_MIN_BRIGHTNESS,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "move_1_195_0_0": Light.HOLD_BRIGHTNESS_DOWN,
            "move_0_195_0_0": Light.HOLD_BRIGHTNESS_UP,
            "stop": Light.RELEASE,
            "toggle": Light.TOGGLE,
            "step_0_1_0_0_0": Light.ON_FULL_BRIGHTNESS,
            "step_1_1_0_0_0": Light.ON_MIN_BRIGHTNESS,
        }

    def default_delay(self) -> int:
        return 500


class E1744Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Z2MLight.RELEASE,
            "toggle": Z2MLight.TOGGLE,
            "brightness_step_up": Z2MLight.ON_FULL_BRIGHTNESS,
            "brightness_step_down": Z2MLight.ON_MIN_BRIGHTNESS,
        }


class E1744MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # brightness_move_down, brightness_move_up, brightness_stop,
    # toggle, brightness_step_up, brightness_step_down

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "brightness_move_down": MediaPlayer.HOLD_VOLUME_DOWN,
            "brightness_move_up": MediaPlayer.HOLD_VOLUME_UP,
            "brightness_stop": MediaPlayer.RELEASE,
            "toggle": MediaPlayer.PLAY_PAUSE,
            "brightness_step_up": MediaPlayer.NEXT_TRACK,
            "brightness_step_down": MediaPlayer.PREVIOUS_TRACK,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            2001: MediaPlayer.HOLD_VOLUME_UP,
            3001: MediaPlayer.HOLD_VOLUME_DOWN,
            2003: MediaPlayer.RELEASE,
            3003: MediaPlayer.RELEASE,
            1002: MediaPlayer.PLAY_PAUSE,
            1004: MediaPlayer.NEXT_TRACK,
            1005: MediaPlayer.PREVIOUS_TRACK,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "move_1_195_0_0": MediaPlayer.HOLD_VOLUME_DOWN,
            "move_0_195_0_0": MediaPlayer.HOLD_VOLUME_UP,
            "stop": MediaPlayer.RELEASE,
            "toggle": MediaPlayer.PLAY_PAUSE,
            "step_0_1_0_0_0": MediaPlayer.NEXT_TRACK,
            "step_1_1_0_0_0": MediaPlayer.PREVIOUS_TRACK,
        }

    def default_delay(self) -> int:
        return 500


class E1766LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"open": Light.ON, "close": Light.OFF}

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,
            1003: Light.ON_FULL_BRIGHTNESS,
            2002: Light.OFF,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "up_open": Light.ON,
            "down_close": Light.OFF,
        }


class E1766Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"open": Z2MLight.ON, "close": Z2MLight.OFF}


class E1766SwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"open": Switch.ON, "close": Switch.OFF}

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {1002: Switch.ON, 2002: Switch.OFF}

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {"up_open": Switch.ON, "down_close": Switch.OFF}


class E1766CoverController(CoverController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "open": Cover.TOGGLE_OPEN,
            "close": Cover.TOGGLE_CLOSE,
            "stop": Cover.STOP,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Cover.TOGGLE_OPEN,
            1003: Cover.STOP,
            2002: Cover.TOGGLE_CLOSE,
            2003: Cover.STOP,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "up_open": Cover.TOGGLE_OPEN,
            "down_close": Cover.TOGGLE_CLOSE,
            "stop": Cover.STOP,
        }


class E1812LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_TOGGLE,
            "brightness_stop": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.TOGGLE,
            1001: Light.HOLD_BRIGHTNESS_TOGGLE,
            1003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.TOGGLE,
            "move_with_on_off": Light.HOLD_BRIGHTNESS_TOGGLE,
            "stop": Light.RELEASE,
        }

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class E1812Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.TOGGLE,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_TOGGLE,
            "brightness_stop": Z2MLight.RELEASE,
        }


class E1812SwitchController(SwitchController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {"on": Switch.TOGGLE}

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {1002: Switch.TOGGLE}

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {"on": Light.TOGGLE}

    def get_zha_action(self, data: EventData) -> str:
        command: str = data["command"]
        return command


class E2002LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "arrow_left_click": Light.CLICK_COLOR_DOWN,
            "arrow_right_click": Light.CLICK_COLOR_UP,
            "brightness_move_up": Light.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Light.RELEASE,
            "brightness_move_down": Light.HOLD_BRIGHTNESS_DOWN,
            "arrow_left_hold": Light.HOLD_COLOR_DOWN,
            "arrow_left_release": Light.RELEASE,
            "arrow_right_hold": Light.HOLD_COLOR_UP,
            "arrow_right_release": Light.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: Light.ON,
            2002: Light.OFF,
            3002: Light.CLICK_COLOR_DOWN,
            4002: Light.CLICK_COLOR_UP,
            1001: Light.HOLD_BRIGHTNESS_UP,
            1003: Light.RELEASE,
            2001: Light.HOLD_BRIGHTNESS_DOWN,
            2003: Light.RELEASE,
            3001: Light.HOLD_COLOR_DOWN,
            3003: Light.RELEASE,
            4001: Light.HOLD_COLOR_UP,
            4003: Light.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Light.ON,
            "off": Light.OFF,
            "press_257_13_0": Light.CLICK_COLOR_DOWN,
            "press_256_13_0": Light.CLICK_COLOR_UP,
            "move_with_on_off_0_83": Light.HOLD_BRIGHTNESS_UP,
            "move_1_83_0_0": Light.HOLD_BRIGHTNESS_DOWN,
            "hold_3329_0": Light.HOLD_COLOR_DOWN,
            "hold_3328_0": Light.HOLD_COLOR_UP,
            "stop": Light.RELEASE,
            "stop_with_on_off": Light.RELEASE,
            "release": Light.RELEASE,
        }


class W2049LightController(E2002LightController):
    async def initialize(self) -> None:
        await super().initialize()
        self.log(
            "⚠️ `W2049LightController` is deprecated and will be removed. Use `E2002LightController` instead.",
            level="WARNING",
            ascii_encode=False,
        )


class E2002Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": Z2MLight.ON,
            "off": Z2MLight.OFF,
            "arrow_left_click": Z2MLight.CLICK_COLOR_TEMP_DOWN,
            "arrow_right_click": Z2MLight.CLICK_COLOR_TEMP_UP,
            "brightness_move_up": Z2MLight.HOLD_BRIGHTNESS_UP,
            "brightness_stop": Z2MLight.RELEASE,
            "brightness_move_down": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "arrow_left_hold": Z2MLight.HOLD_COLOR_TEMP_DOWN,
            "arrow_left_release": Z2MLight.RELEASE,
            "arrow_right_hold": Z2MLight.HOLD_COLOR_TEMP_UP,
            "arrow_right_release": Z2MLight.RELEASE,
        }


class E2002MediaPlayerController(MediaPlayerController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": MediaPlayer.PLAY_PAUSE,
            "off": MediaPlayer.CLICK_VOLUME_DOWN,
            "arrow_left_click": MediaPlayer.PREVIOUS_TRACK,
            "arrow_right_click": MediaPlayer.NEXT_TRACK,
            "arrow_left_hold": MediaPlayer.PREVIOUS_SOURCE,
            "arrow_left_release": MediaPlayer.RELEASE,
            "arrow_right_hold": MediaPlayer.NEXT_SOURCE,
            "arrow_right_release": MediaPlayer.RELEASE,
            "brightness_move_up": MediaPlayer.HOLD_VOLUME_UP,
            "brightness_move_down": MediaPlayer.HOLD_VOLUME_DOWN,
            "brightness_stop": MediaPlayer.RELEASE,
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: MediaPlayer.PLAY_PAUSE,
            2002: MediaPlayer.CLICK_VOLUME_DOWN,
            3002: MediaPlayer.PREVIOUS_TRACK,
            4002: MediaPlayer.NEXT_TRACK,
            1001: MediaPlayer.HOLD_VOLUME_UP,
            1003: MediaPlayer.RELEASE,
            2001: MediaPlayer.HOLD_VOLUME_DOWN,
            2003: MediaPlayer.RELEASE,
            3001: MediaPlayer.PREVIOUS_SOURCE,
            3003: MediaPlayer.RELEASE,
            4001: MediaPlayer.NEXT_SOURCE,
            4003: MediaPlayer.RELEASE,
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "on": MediaPlayer.PLAY_PAUSE,
            "off": MediaPlayer.CLICK_VOLUME_DOWN,
            "press_257_13_0": MediaPlayer.PREVIOUS_TRACK,
            "press_256_13_0": MediaPlayer.NEXT_TRACK,
            "move_with_on_off_0_83": MediaPlayer.HOLD_VOLUME_UP,
            "move_1_83_0_0": MediaPlayer.HOLD_VOLUME_DOWN,
            "hold_3329_0": MediaPlayer.PREVIOUS_SOURCE,
            "hold_3328_0": MediaPlayer.NEXT_SOURCE,
            "stop": MediaPlayer.RELEASE,
            "stop_with_on_off": MediaPlayer.RELEASE,
            "release": MediaPlayer.RELEASE,
        }


class W2049MediaPlayerController(E2002MediaPlayerController):
    async def initialize(self) -> None:
        await super().initialize()
        self.log(
            "⚠️ `W2049MediaPlayerController` is deprecated and will be removed. "
            "Use `E2002MediaPlayerController` instead.",
            level="WARNING",
            ascii_encode=False,
        )


class E2213LightController(LightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_initial_press": Light.ON,
            "2_initial_press": Light.OFF,
            "1_long_press": Light.HOLD_BRIGHTNESS_UP,
            "2_long_press": Light.HOLD_BRIGHTNESS_DOWN,
            "1_short_release": Light.RELEASE,
            "2_short_release": Light.RELEASE,
            "1_long_release": Light.RELEASE,
            "2_long_release": Light.RELEASE,
            "1_double_press": Light.HOLD_COLOR_UP,
            "2_double_press": Light.HOLD_COLOR_DOWN,
        }


class E2213Z2MLightController(Z2MLightController):
    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "1_initial_press": Z2MLight.ON,
            "2_initial_press": Z2MLight.OFF,
            "1_long_press": Z2MLight.HOLD_BRIGHTNESS_UP,
            "2_long_press": Z2MLight.HOLD_BRIGHTNESS_DOWN,
            "1_short_release": Z2MLight.RELEASE,
            "2_short_release": Z2MLight.RELEASE,
            "1_long_release": Z2MLight.RELEASE,
            "2_long_release": Z2MLight.RELEASE,
            "1_double_press": Z2MLight.HOLD_COLOR_TEMP_UP,
            "2_double_press": Z2MLight.HOLD_COLOR_TEMP_DOWN,
        }


class E2123MediaPlayerController(MediaPlayerController):

    def get_z2m_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,  # click Play button
            "play_pause": MediaPlayer.PLAY_PAUSE,  # click Play button
            "track_next": MediaPlayer.NEXT_TRACK,  # click Next Track
            "track_previous": MediaPlayer.PREVIOUS_TRACK,  # click Previous Track
            "volume_up": MediaPlayer.CLICK_VOLUME_UP,  # click + (Volume up)
            "volume_up_hold": MediaPlayer.CLICK_VOLUME_UP,  # hold + (Volume up)
            "volume_down": MediaPlayer.CLICK_VOLUME_DOWN,  # click - (Volume down)
            "volume_down_hold": MediaPlayer.CLICK_VOLUME_DOWN,  # hold - (Volume down)
            "dots_1_initial_press": MediaPlayer.PREVIOUS_SOURCE,  # click . (Previous Source)
            "dots_2_initial_press": MediaPlayer.NEXT_SOURCE,  # click .. (Next Source)
        }

    def get_deconz_actions_mapping(self) -> DefaultActionsMapping:
        return {
            1002: MediaPlayer.PLAY,  # Play; Press/Release or Hold
            2001: MediaPlayer.HOLD_VOLUME_UP,  # +; Hold (every 0.2s)
            2002: MediaPlayer.RELEASE,  # +; Press/Release
            3001: MediaPlayer.HOLD_VOLUME_DOWN,  # +; Hold (every 0.2s)
            3002: MediaPlayer.RELEASE,  # -; Press/Release
            4002: MediaPlayer.PREVIOUS_TRACK,  # Previous; Press/Release or Hold
            5002: MediaPlayer.NEXT_TRACK,  # Next; Press/Release or Hold
            6000: MediaPlayer.PREVIOUS_SOURCE,  # .; Initial Press
            7000: MediaPlayer.NEXT_SOURCE,  # ..; Initial Press
        }

    def get_zha_actions_mapping(self) -> DefaultActionsMapping:
        return {
            "toggle": MediaPlayer.PLAY_PAUSE,  # click Play button
            "play_pause": MediaPlayer.PLAY_PAUSE,  # click Play button
            "step_0_1_0_0_0": MediaPlayer.NEXT_TRACK,  # click Next Track
            "step_1_1_0_0_0": MediaPlayer.PREVIOUS_TRACK,  # click Previous Track
            "move_with_on_off_0_255": MediaPlayer.CLICK_VOLUME_UP,  # click + (Volume up)
            "move_0_255_0_0": MediaPlayer.HOLD_VOLUME_UP,  # hold + (Volume up)
            "move_with_on_off_1_255": MediaPlayer.CLICK_VOLUME_DOWN,  # click - (Volume down)
            "move_1_255_0_0": MediaPlayer.HOLD_VOLUME_DOWN,  # hold - (Volume down)
            "2_initial_press_0": MediaPlayer.PREVIOUS_SOURCE,  # click . (Previous Source)
            "3_initial_press_0": MediaPlayer.NEXT_SOURCE,  # click .. (Next Source)
        }

    def get_zha_action(self, data: EventData) -> str:
        command = data["command"]
        args = data["args"]
        if isinstance(args, dict):
            args = args["args"]
        args = list(map(str, args))
        action = command
        if not (command == "stop" or command == "release"):
            if len(args) > 0:
                action += "_" + "_".join(args)
        endpoint = data["endpoint_id"]
        # We only need to add the endpoint ID for the dot buttons, which use 2 and 3
        if endpoint != 1:
            return f"{data['endpoint_id']}_{action}"
        else:
            return action
