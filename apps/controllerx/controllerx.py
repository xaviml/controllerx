"""
Bring full functionality to light and media player controllers.
From turning devices on/off to changing the color lights.

https://github.com/xaviml/controllerx
"""
import abc
import math
import random
import time
from collections import defaultdict
from functools import wraps

import hassapi as hass

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_DELAY = 350  # In milliseconds
DEFAULT_ACTION_DELTA = 300  # In milliseconds
DEFAULT_EVENT_NAME = "deconz_event"


def action(method):
    async def _action_impl(self, *args, **kwargs):
        continue_call = await self.before_action(method.__name__, *args, **kwargs)
        if continue_call:
            await method(self, *args, **kwargs)

    return _action_impl


###############################################################
###############################################################
###  CORE CLASSES                                           ###
###                                                         ###
###  All controllers must extend from Controller and        ###
###  implement get_state_actions_mapping to map the         ###
###  controller actions to the internal functions.          ###
###############################################################
###############################################################


class Controller(hass.Hass, abc.ABC):
    """
    This is the parent Controller, all controllers must extend from this class.
    It is mandatory to implement `get_state_actions_mapping` to map the controller 
    actions to the internal functions.
    """

    DIRECTION_UP = "up"
    DIRECTION_DOWN = "down"

    def initialize(self):
        ad_version = self.get_ad_version()
        major, minor, patch = ad_version.split(".")
        if int(major) < 4:
            raise ValueError("Please upgrade to AppDaemon 4.x")
        self.action_delta = self.args.get("action_delta", DEFAULT_ACTION_DELTA)
        self.action_times = defaultdict(lambda: 0)

        if "event_id" in self.args and "sensor" in self.args:
            raise ValueError("'event_id' and 'sensor' cannot be used together")
        action_mapping_type, self.actions_mapping = self.get_actions_mapping()
        if self.actions_mapping == None:
            raise ValueError(
                f"This controller does not support {action_mapping_type} actions."
            )
        included_actions = self.args.get("actions", list(self.actions_mapping.keys()))
        included_actions = self.get_list(included_actions)
        self.actions_mapping = {
            key: value
            for key, value in self.actions_mapping.items()
            if key in included_actions
        }

        if "event_id" in self.args:
            event_name = self.args.get("event", DEFAULT_EVENT_NAME)
            events_id = self.get_list(self.args.get("event_id"))
            for event_id in events_id:
                self.listen_event(self.event_callback, event_name, id=event_id)

        if "sensor" in self.args:
            sensors = self.get_list(self.args["sensor"])
            for sensor in sensors:
                self.listen_state(self.state_callback, sensor)

    def get_actions_mapping(self):
        if "event_id" in self.args:
            return "event", self.get_event_actions_mapping()
        elif "sensor" in self.args:
            return "state", self.get_state_actions_mapping()
        else:
            return None, None

    def get_list(self, entities):
        type_ = type(entities)
        if type_ == str:
            return entities.replace(" ", "").split(",")
        elif type_ == list:
            return entities

    async def state_callback(self, entity, attribute, old, new, kwargs):
        await self.handle_action(new)

    async def event_callback(self, event_name, data, kwargs):
        await self.handle_action(data["event"])

    async def handle_action(self, action_key):
        if action_key in self.actions_mapping:
            previous_call_time = self.action_times[action_key]
            now = time.time() * 1000
            self.action_times[action_key] = now
            if now - previous_call_time > self.action_delta:
                self.log(f"Button pressed after: {action_key}", level="DEBUG")
                action, *args = self.get_action(self.actions_mapping[action_key])
                await action(*args)

    async def before_action(self, action, *args, **kwargs):
        """
        Controllers have the option to implement this function, which is called
        everytime before an action is called and it has the check_before_action decorator.
        It should return True if the action shoul be called. Otherwise it should return False.
        """
        return True

    def get_action(self, action_value):
        if type(action_value) == tuple or type(action_value) == list:
            return action_value
        elif callable(action_value):
            return (action_value,)
        else:
            raise ValueError(
                "The action value from the action mapping should be a list or a function"
            )

    def get_state_actions_mapping(self):
        """
        Controllers can implement this function. It should return a dict
        with the states that a controller can take and the functions as values.
        This is used for z2m support.
        """
        return None

    def get_event_actions_mapping(self):
        """
        Controllers can implement this function. It should return a dict
        with the event id that a controller can take and the functions as values.
        This is used for deConz support.
        """
        return None

    async def get_attr_value(self, entity, attribute):
        if "group." in entity:
            entities = await self.get_state(entity, attribute="entity_id")
            entity = entities[0]
        out = await self.get_state(entity, attribute=attribute)
        return out


class ReleaseHoldController(Controller, abc.ABC):
    def initialize(self):
        super().initialize()
        self.on_hold = False
        self.delay = self.args.get("delay", self.default_delay())

    @action
    async def release(self):
        self.on_hold = False

    @action
    async def hold(self, *args):
        self.on_hold = True
        stop = False
        while self.on_hold and not stop:
            stop = await self.hold_loop(*args)
            await self.sleep(self.delay / 1000)

    async def before_action(self, action, *args, **kwargs):
        to_return = not (action == "hold" and self.on_hold)
        return await super().before_action(action, *args, **kwargs) and to_return

    @abc.abstractmethod
    async def hold_loop(self):
        """
        This function is called by the ReleaseHoldController depending on the settings.
        It stops calling the function once release action is called or when this function
        returns True.
        """
        pass

    def default_delay(self):
        """
        This function can be overwritten for each device to indeicate the delay 
        for the specific device, by default it returns the default delay from the app
        """
        return DEFAULT_DELAY


###############################################################
###############################################################
###  TYPE OF CONTROLLERS                                    ###
###                                                         ###
###  In this section, we will find the code for different   ###
###  types of controllers and their logic. This controllers ###
###  contain the actions that need to be map for the        ###
###  different devices.                                     ###
###############################################################
###############################################################


class LightController(ReleaseHoldController):
    """
    This is the main class that controls the lights for different devices.
    Type of actions:
        - On/Off/Toggle
        - Brightness click and hold
        - Color temperature click and hold
        - xy color click and hold
    If a light supports xy_color and color_temperature, then xy_color will be the
    default functionality. Parameters taken:
        - sensor (required): Inherited from Controller
        - light (required): This is either the light entity name or a dictionary as 
          {name: string, color_mode: auto | xy_color | color_temp}
        - delay (optional): Inherited from ReleaseHoldController
        - manual_steps (optional): Number of steps to go from min to max when clicking.
        - automatic_steps (optional): Number of steps to go from min to max when smoothing.
    """

    ATTRIBUTE_BRIGHTNESS = "brightness"
    ATTRIBUTE_COLOR = "color"

    # These are the 24 colors that appear in the circle color of home assistant
    colors = [
        (0.701, 0.299),
        (0.667, 0.284),
        (0.581, 0.245),
        (0.477, 0.196),
        (0.385, 0.155),
        (0.301, 0.116),
        (0.217, 0.077),
        (0.157, 0.05),
        (0.136, 0.04),
        (0.137, 0.065),
        (0.141, 0.137),
        (0.146, 0.238),
        (0.323, 0.329),  # white color middle
        (0.151, 0.343),
        (0.157, 0.457),
        (0.164, 0.591),
        (0.17, 0.703),
        (0.172, 0.747),
        (0.199, 0.724),
        (0.269, 0.665),
        (0.36, 0.588),
        (0.444, 0.517),
        (0.527, 0.447),
        (0.612, 0.374),
        (0.677, 0.319),
    ]

    attribute_minmax = {
        "brightness": {"min": 1, "max": 255},
        "color_temp": {"min": 153, "max": 500},
    }

    sign_mapping = {Controller.DIRECTION_UP: 1, Controller.DIRECTION_DOWN: -1}

    def initialize(self):
        super().initialize()
        self.light = self.get_light(self.args["light"])
        self.manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        self.automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.value_attribute = None
        self.index_color = 0
        self.smooth_power_on = self.args.get(
            "smooth_power_on", self.supports_smooth_power_on()
        )

    def get_light(self, light):
        type_ = type(light)
        if type_ == str:
            return {"name": light, "color_mode": "auto"}
        elif type_ == dict:
            if "color_mode" in light:
                return light
            else:
                return {"name": light["name"], "color_mode": "auto"}

    @action
    async def on(self, **attributes):
        self.call_service(
            "homeassistant/turn_on", entity_id=self.light["name"], **attributes
        )

    @action
    async def off(self):
        self.call_service("homeassistant/turn_off", entity_id=self.light["name"])

    @action
    async def toggle(self):
        self.call_service("homeassistant/toggle", entity_id=self.light["name"])

    @action
    async def on_full(self, attribute):
        await self.change_light_state(
            self.attribute_minmax[attribute]["min"], attribute, self.DIRECTION_UP, 1
        )

    async def get_attribute(self, attribute):
        if attribute == self.ATTRIBUTE_COLOR:
            entity_states = await self.get_state(self.light["name"], attribute="all")
            entity_attributes = entity_states["attributes"]
            if self.light["color_mode"] == "auto":
                if "xy_color" in entity_attributes:
                    return "xy_color"
                elif "color_temp" in entity_attributes:
                    return "color_temp"
                else:
                    raise ValueError(
                        "This light does not support xy_color or color_temp"
                    )
            else:
                return self.light["color_mode"]
        else:
            return attribute

    async def get_value_attribute(self, attribute):
        if attribute == "xy_color":
            return None
        else:
            return await self.get_attr_value(self.light["name"], attribute)

    def check_smooth_power_on(self, attribute, direction, light_state):
        return (
            direction == LightController.DIRECTION_UP
            and attribute == self.ATTRIBUTE_BRIGHTNESS
            and self.smooth_power_on
            and light_state == "off"
        )

    async def before_action(self, action, *args, **kwargs):
        to_return = True
        if action == "click" or action == "hold":
            attribute, direction, *_ = args
            light_state = await self.get_state(self.light["name"])
            to_return = light_state == "on" or self.check_smooth_power_on(
                attribute, direction, light_state
            )
        return await super().before_action(action, *args, **kwargs) and to_return

    @action
    async def click(self, attribute, direction):
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        await self.change_light_state(
            self.value_attribute, attribute, direction, self.manual_steps
        )

    @action
    async def hold(self, attribute, direction):
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        await super().hold(attribute, direction)

    async def hold_loop(self, attribute, direction):
        return await self.change_light_state(
            self.value_attribute, attribute, direction, self.automatic_steps
        )

    async def change_light_state(self, old, attribute, direction, steps):
        """
        This functions changes the state of the light depending on the previous
        value and attribute. It returns True when no more changes will need to be done.
        Otherwise, it returns False.
        """
        sign = self.sign_mapping[direction]
        if attribute == "xy_color":
            self.index_color += sign
            self.index_color = self.index_color % len(self.colors)
            new_state_attribute = self.colors[self.index_color]
            attributes = {
                attribute: new_state_attribute,
                "transition": self.delay / 1000,
            }
            await self.on(**attributes)
            # In case of xy_color mode it never finishes the loop, the hold loop
            # will only stop if the hold action is called when releasing the button.
            # I haven't experimented any problems with it, but a future implementation
            # would be to force the loop to stop after 4 or 5 loops as a safety measure.
            return False
        self.log(f"Attribute: {attribute}; Current value: {old}", level="DEBUG")
        max_ = self.attribute_minmax[attribute]["max"]
        min_ = self.attribute_minmax[attribute]["min"]
        step = (max_ - min_) // steps
        new_state_attribute = old + sign * step
        if self.check_smooth_power_on(
            attribute, direction, await self.get_state(self.light["name"])
        ):
            new_state_attribute = min_
            # The light needs to be turned on since the current state is off
            # and if the light is turned on with the brightness attribute,
            # the brightness state won't remain when turned of and on again.
            await self.on()
        attributes = {attribute: new_state_attribute, "transition": self.delay / 1000}
        if min_ <= new_state_attribute <= max_:
            await self.on(**attributes)
            self.value_attribute = new_state_attribute
            return False
        else:
            new_state_attribute = max(min_, min(new_state_attribute, max_))
            attributes[attribute] = new_state_attribute
            await self.on(**attributes)
            self.value_attribute = new_state_attribute
            return True

    def supports_smooth_power_on(self):
        """
        This function can be overrided for each device to indicate the default behaviour of the controller
        when the associated light is off and an event for incrementing brightness is received.
        Returns True if the associated light should be turned on with minimum brightness if an event for incrementing
        brightness is received, while the lamp is off.
        The behaviour can be overridden by the user with the 'smooth_power_on' option in app configuration.
        """
        return False


class MediaPlayerController(ReleaseHoldController):
    def initialize(self):
        super().initialize()
        self.media_player = self.args["media_player"]

    @action
    async def play_pause(self):
        self.call_service("media_player/media_play_pause", entity_id=self.media_player)

    @action
    async def previous_track(self):
        self.call_service(
            "media_player/media_previous_track", entity_id=self.media_player
        )

    @action
    async def next_track(self):
        self.call_service("media_player/media_next_track", entity_id=self.media_player)

    @action
    async def volume_up(self):
        self.call_service("media_player/volume_up", entity_id=self.media_player)

    @action
    async def volume_down(self):
        self.call_service("media_player/volume_down", entity_id=self.media_player)

    @action
    async def hold(self, direction):
        # This variable is responsible to count how many times hold_loop has been called
        # so we don't fall in a infinite loop
        self.hold_loop_times = 0
        await super().hold(direction)

    async def hold_loop(self, direction):
        if direction == Controller.DIRECTION_UP:
            self.call_service("media_player/volume_up", entity_id=self.media_player)
        else:
            self.call_service("media_player/volume_down", entity_id=self.media_player)
        self.hold_loop_times += 1
        return self.hold_loop_times > 10

    def default_delay(self):
        return 500


###############################################################
###############################################################
###  DEVICES                                                ###
###                                                         ###
###  In this section, we will find the code for different   ###
###  types of end controllers and their function is to map  ###
###  their states to the proper function of the controller  ###
###  (e.g. LightController)                                 ###
###############################################################
###############################################################


class E1810Controller(LightController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_state_actions_mapping(self):
        return {
            "toggle": self.toggle,
            "brightness_up_click": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "brightness_down_click": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "arrow_left_click": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            "arrow_right_click": (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            "brightness_up_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "brightness_up_release": self.release,
            "brightness_down_hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "brightness_down_release": self.release,
            "arrow_left_hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            "arrow_left_release": self.release,
            "arrow_right_hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            "arrow_right_release": self.release,
        }

    def get_event_actions_mapping(self):
        return {
            1002: self.toggle,
            2002: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            3002: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            4002: (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            5002: (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            2001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            2003: self.release,
            3001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            3003: self.release,
            4001: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            4003: self.release,
            5001: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            5003: self.release,
        }


class E1810MediaPlayerController(MediaPlayerController):
    # Different states reported from the controller:
    # toggle, brightness_up_click, brightness_down_click
    # arrow_left_click, arrow_right_click, brightness_up_hold
    # brightness_up_release, brightness_down_hold, brightness_down_release,
    # arrow_left_hold, arrow_left_release, arrow_right_hold
    # arrow_right_release

    def get_state_actions_mapping(self):
        return {
            "toggle": self.play_pause,
            "brightness_up_click": self.volume_up,
            "brightness_down_click": self.volume_down,
            "arrow_left_click": self.previous_track,
            "arrow_right_click": self.next_track,
            "brightness_up_hold": (self.hold, Controller.DIRECTION_UP),
            "brightness_up_release": self.release,
            "brightness_down_hold": (self.hold, Controller.DIRECTION_DOWN),
            "brightness_down_release": self.release,
        }

    def get_event_actions_mapping(self):
        return {
            1002: self.play_pause,
            2002: self.volume_up,
            3002: self.volume_down,
            4002: self.previous_track,
            5002: self.next_track,
            2001: (self.hold, Controller.DIRECTION_UP),
            2003: self.release,
            3001: (self.hold, Controller.DIRECTION_DOWN),
            3003: self.release,
        }


class E1743Controller(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_state_actions_mapping(self):
        return {
            "on": self.on,
            "off": self.off,
            "brightness_up": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "brightness_down": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "brightness_stop": self.release,
        }

    def get_event_actions_mapping(self):
        return {
            2002: self.on,
            1002: self.off,
            2001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            1001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            2003: self.release,
            1003: self.release,
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

    def get_state_actions_mapping(self):
        return {
            "rotate_left": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "rotate_left_quick": self.rotate_left_quick,
            "rotate_right": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "rotate_right_quick": self.rotate_right_quick,
            "rotate_stop": self.release,
        }


class E1744LightController(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_right, rotate_stop,
    # play_pause, skip_forward, skip_backward

    def get_state_actions_mapping(self):
        return {
            "rotate_left": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "rotate_right": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "rotate_stop": self.release,
            "play_pause": self.toggle,
            "skip_forward": (self.on_full, LightController.ATTRIBUTE_BRIGHTNESS),
        }

    def get_event_actions_mapping(self):
        return {
            2001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            3001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
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

    def get_state_actions_mapping(self):
        return {
            "rotate_left": (self.hold, Controller.DIRECTION_DOWN),
            "rotate_right": (self.hold, Controller.DIRECTION_UP),
            "rotate_stop": self.release,
            "play_pause": self.play_pause,
            "skip_forward": self.next_track,
            "skip_backward": self.previous_track,
        }

    def get_event_actions_mapping(self):
        return {
            2001: (self.hold, Controller.DIRECTION_DOWN),
            3001: (self.hold, Controller.DIRECTION_UP),
            2003: self.release,
            3003: self.release,
            1002: self.play_pause,
            1004: self.next_track,
            1005: self.previous_track,
        }

    def default_delay(self):
        return 1000


class HueDimmerController(LightController):
    # Different states reported from the controller:
    # on-press, on-hold, on-hold-release, up-press, up-hold,
    # up-hold-release, down-press, down-hold, down-hold-release,
    # off-press, off-hold, off-hold-release

    def get_state_actions_mapping(self):
        return {
            "on-press": self.on,
            "on-hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            "on-hold-release": (self.release,),
            "up-press": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "up-hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            "up-hold-release": self.release,
            "down-press": (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "down-hold": (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            "down-hold-release": self.release,
            "off-press": self.off,
            "off-hold": (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            "off-hold-release": self.release,
        }

    def get_event_actions_mapping(self):
        return {
            1000: self.on,
            1001: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_UP,
            ),
            1003: self.release,
            2000: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            2001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            2003: self.release,
            3000: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_DOWN,
            ),
            3001: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                LightController.DIRECTION_UP,
            ),
            3003: self.release,
            4000: self.off,
            4001: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                LightController.DIRECTION_DOWN,
            ),
            4003: self.release,
        }
