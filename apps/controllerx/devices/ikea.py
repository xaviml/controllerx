from core import LightController, MediaPlayerController, Stepper, action


class E1810Controller(LightController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self):
        return {
            "toggle": self.toggle,
            "brightness_up_click": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "brightness_down_click": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "arrow_left_click": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.DOWN,
            ),
            "arrow_right_click": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.UP,
            ),
            "brightness_up_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "brightness_up_release": self.release,
            "brightness_down_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "brightness_down_release": self.release,
            "arrow_left_hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                Stepper.DOWN,
            ),
            "arrow_left_release": self.release,
            "arrow_right_hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                Stepper.UP,
            ),
            "arrow_right_release": self.release,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: self.toggle,
            2002: (self.click, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.UP,),
            3002: (self.click, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.DOWN,),
            4002: (self.click, LightController.ATTRIBUTE_COLOR, Stepper.DOWN,),
            5002: (self.click, LightController.ATTRIBUTE_COLOR, Stepper.UP,),
            2001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.UP,),
            2003: self.release,
            3001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.DOWN,),
            3003: self.release,
            4001: (self.hold, LightController.ATTRIBUTE_COLOR, Stepper.DOWN,),
            4003: self.release,
            5001: (self.hold, LightController.ATTRIBUTE_COLOR, Stepper.UP,),
            5003: self.release,
        }

    def get_zha_actions_mapping(self):
        return {
            "toggle": self.toggle,
            "step_with_on_off_0_43_5": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "step_1_43_5": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "press_257_13_0": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.DOWN,
            ),
            "press_256_13_0": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.UP,
            ),
            "move_with_on_off_0_83": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "move_1_83": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "hold_3329_0": (self.hold, LightController.ATTRIBUTE_COLOR, Stepper.DOWN,),
            "hold_3328_0": (self.hold, LightController.ATTRIBUTE_COLOR, Stepper.UP,),
            "stop": self.release,
            "release": self.release,
        }


class E1810MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_z2m_actions_mapping(self):
        return {
            "toggle": self.play_pause,
            "brightness_up_click": self.volume_up,
            "brightness_down_click": self.volume_down,
            "arrow_left_click": self.previous_track,
            "arrow_right_click": self.next_track,
            "brightness_up_hold": (self.hold, Stepper.UP),
            "brightness_up_release": self.release,
            "brightness_down_hold": (self.hold, Stepper.DOWN),
            "brightness_down_release": self.release,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: self.play_pause,
            2002: self.volume_up,
            3002: self.volume_down,
            4002: self.previous_track,
            5002: self.next_track,
            2001: (self.hold, Stepper.UP),
            2003: self.release,
            3001: (self.hold, Stepper.DOWN),
            3003: self.release,
        }

    def get_zha_actions_mapping(self):
        return {
            "toggle": self.play_pause,
            "step_with_on_off_0_43_5": self.volume_up,
            "step_1_43_5": self.volume_down,
            "press_257_13_0": self.previous_track,
            "press_256_13_0": self.next_track,
            "move_with_on_off_0_83": (self.hold, Stepper.UP),
            "move_1_83": (self.hold, Stepper.DOWN),
            "stop": self.release,
            "release": self.release,
        }


class E1743Controller(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_z2m_actions_mapping(self):
        return {
            "on": self.on,
            "off": self.off,
            "brightness_up": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "brightness_down": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "brightness_stop": self.release,
        }

    def get_deconz_actions_mapping(self):
        return {
            1002: self.on,
            2002: self.off,
            1001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.UP),
            2001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.DOWN),
            1003: self.release,
            2003: self.release,
        }

    def get_zha_actions_mapping(self):
        return {
            "on": self.on,
            "off": self.off,
            "move_with_on_off_0_83": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "move_1_83": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "stop": self.release,
        }


class ICTCG1Controller(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_left_quick
    # rotate_right, rotate_right_quick
    # rotate_stop

    @action
    async def rotate_left_quick(self):
        await self.release()
        await self.off()

    @action
    async def rotate_right_quick(self):
        await self.release()
        await self.on_full(LightController.ATTRIBUTE_BRIGHTNESS)

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "rotate_left_quick": self.rotate_left_quick,
            "rotate_right": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "rotate_right_quick": self.rotate_right_quick,
            "rotate_stop": self.release,
        }


class E1744LightController(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_right, rotate_stop,
    # play_pause, skip_forward, skip_backward

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            "rotate_right": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            "rotate_stop": self.release,
            "play_pause": self.toggle,
            "skip_forward": (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
        }

    def get_deconz_actions_mapping(self):
        return {
            2001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.DOWN,),
            3001: (self.hold, LightController.ATTRIBUTE_BRIGHTNESS, Stepper.UP,),
            2003: self.release,
            3003: self.release,
            1002: self.toggle,
            1004: (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
        }

    def default_delay(self):
        return 1200


class E1744MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # rotate_left, rotate_right, rotate_stop,
    # play_pause, skip_forward, skip_backward

    def get_z2m_actions_mapping(self):
        return {
            "rotate_left": (self.hold, Stepper.DOWN),
            "rotate_right": (self.hold, Stepper.UP),
            "rotate_stop": self.release,
            "play_pause": self.play_pause,
            "skip_forward": self.next_track,
            "skip_backward": self.previous_track,
        }

    def get_deconz_actions_mapping(self):
        return {
            2001: (self.hold, Stepper.DOWN),
            3001: (self.hold, Stepper.UP),
            2003: self.release,
            3003: self.release,
            1002: self.play_pause,
            1004: self.next_track,
            1005: self.previous_track,
        }

    def get_zha_actions_mapping(self):
        return {
            "move_1_195": (self.hold, Stepper.DOWN),
            "move_0_195": (self.hold, Stepper.UP),
            "stop": self.release,
            "stop": self.release,
            "toggle": self.play_pause,
            "step_0_1_0": self.next_track,
            "step_1_1_0": self.previous_track,
        }

    def default_delay(self):
        return 1000
