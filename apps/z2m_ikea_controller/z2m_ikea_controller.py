"""
Bring full functionality to light controllers

https://github.com/xaviml/z2m_ikea_controller
"""
import abc
import math
import random
import time
from functools import wraps

import appdaemon.plugins.hass.hassapi as hass

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_DELAY = 350


def check_before_action(method):
    @wraps(method)
    def _impl(self, *args, **kwargs):
        continue_call = self.before_action(method.__name__)
        if continue_call:
            method(self, *args, **kwargs)

    return _impl


###############################################################
###############################################################
###  CORE CLASSES                                           ###
###                                                         ###
###  All controllers must extend from Controller and        ###
###  implement get_actions_mapping to map the controller    ###
###  actions to the internal functions.                     ###
###############################################################
###############################################################


class Controller(hass.Hass, abc.ABC):
    """
    This is the parent Controller, all controllers must extend from this class.
    It is mandatory to implement `get_actions_mapping` to map the controller 
    actions to the internal functions.
    """

    def initialize(self):
        self.actions_mapping = self.get_actions_mappings()
        included_actions = self.args.get("actions", self.actions_mapping.keys())
        included_actions = self.get_list(included_actions)
        self.actions_mapping = {
            key: value
            for key, value in self.actions_mapping.items()
            if key in included_actions
        }
        self.sensors = self.get_list(self.args["sensor"])
        for sensor in self.sensors:
            self.listen_state(self.state, sensor)

    def get_list(self, entities):
        type_ = type(entities)
        if type_ == str:
            return entities.replace(" ", "").split(",")
        elif type_ == list:
            return entities

    def state(self, entity, attribute, old, new, kwargs):
        if new in self.actions_mapping and old == new:
            self.log(f"Button pressed: {new}", level="DEBUG")
            action = self.actions_mapping[new]
            action()

    def before_action(self, action):
        """
        Controllers have the option to implement this function, which is called
        everytime before an action is called and it has the check_before_action decorator.
        It should return True if the action shoul be called. Otherwise it should return False.
        """
        return True

    @abc.abstractmethod
    def get_actions_mappings(self):
        """
        All controllers must implement this function. It should return a dict
        with the states that a controller can take and the functions as values.
        """
        pass

    def get_attr_value(self, entity, attribute):
        if "group." in entity:
            entities = self.get_state(entity, attribute="entity_id")
            entity = entities[0]
        out = self.get_state(entity, attribute=attribute)
        return out


class ReleaseHoldController(Controller, abc.ABC):
    def initialize(self):
        super().initialize()
        self.on_hold = False
        # Since time.sleep is not recommended I limited to 1s
        self.delay = min(1000, self.args.get("delay", DEFAULT_DELAY))

    def release(self):
        self.on_hold = False

    def hold(self, *args):
        self.on_hold = True
        stop = False
        while self.on_hold and not stop:
            stop = self.hold_loop(*args)
            # value = self.turn_on_light(
            #     attribute, value, sign, self.automatic_steps
            # )
            # The use of the time.sleep is due to not have a support of seconds
            # in run_every function. It is also fine to use as long is in control:
            # https://github.com/home-assistant/appdaemon/issues/26#issuecomment-274798324
            time.sleep(self.delay / 1000)

    @abc.abstractmethod
    def hold_loop(self):
        """
        This function is called by the ReleaseHoldController depending on the settings.
        It stops calling the function once release action is called or when this function
        returns True.
        """
        pass


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

    ATTRUBUTE_BRIGHTNESS = "brightness"
    ATTRUBUTE_COLOR = "color"
    DIRECTION_UP = "up"
    DIRECTION_DOWN = "down"

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

    sign_mapping = {DIRECTION_UP: 1, DIRECTION_DOWN: -1}

    def initialize(self):
        super().initialize()
        self.light = self.get_light(self.args["light"])
        self.manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        self.automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.value_attribute = None
        self.index_color = 0

    def get_light(self, light):
        type_ = type(light)
        if type_ == str:
            return {"name": light, "color_mode": "auto"}
        elif type_ == dict:
            if "color_mode" in light:
                return light
            else:
                return {"name": light["name"], "color_mode": "auto"}

    def on(self):
        self.turn_on(self.light["name"])

    def off(self):
        self.turn_off(self.light["name"])

    def toggle(self):
        super().toggle(self.light["name"])

    def on_full(self, attribute):
        self.change_light_state(
            self.attribute_minmax[attribute]["min"], attribute, self.DIRECTION_UP, 1
        )

    def get_attribute(self, attribute):
        if attribute == self.ATTRUBUTE_COLOR:
            entity_states = self.get_state(self.light["name"], attribute="all")
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

    def get_value_attribute(self, attribute):
        if attribute == "xy_color":
            return None
        else:
            return self.get_attr_value(self.light["name"], attribute)

    def before_action(self, action):
        if action == "click" or action == "hold":
            light_state = self.get_state(self.light["name"])
            return light_state == "on"
        return True

    @check_before_action
    def click(self, attribute, direction):
        attribute = self.get_attribute(attribute)
        self.value_attribute = self.get_value_attribute(attribute)
        self.change_light_state(
            self.value_attribute, attribute, direction, self.manual_steps
        )

    @check_before_action
    def hold(self, attribute, direction):
        attribute = self.get_attribute(attribute)
        self.value_attribute = self.get_value_attribute(attribute)
        super().hold(attribute, direction)

    def hold_loop(self, attribute, direction):
        return self.change_light_state(
            self.value_attribute, attribute, direction, self.automatic_steps
        )

    def change_light_state(self, old, attribute, direction, steps):
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
            self.turn_on(self.light["name"], **attributes)
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
        attributes = {attribute: new_state_attribute, "transition": self.delay / 1000}
        if min_ <= new_state_attribute <= max_:
            self.turn_on(self.light["name"], **attributes)
            self.value_attribute = new_state_attribute
            return False
        else:
            new_state_attribute = max(min_, min(new_state_attribute, max_))
            attributes[attribute] = new_state_attribute
            self.turn_on(self.light["name"], **attributes)
            return True


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

    def get_actions_mappings(self):
        return {
            "toggle": lambda: self.toggle(),
            "brightness_up_click": lambda: self.click(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_UP
            ),
            "brightness_down_click": lambda: self.click(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_DOWN
            ),
            "arrow_left_click": lambda: self.click(
                LightController.ATTRUBUTE_COLOR, LightController.DIRECTION_DOWN
            ),
            "arrow_right_click": lambda: self.click(
                LightController.ATTRUBUTE_COLOR, LightController.DIRECTION_UP
            ),
            "brightness_up_hold": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_UP
            ),
            "brightness_up_release": lambda: self.release(),
            "brightness_down_hold": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_DOWN
            ),
            "brightness_down_release": lambda: self.release(),
            "arrow_left_hold": lambda: self.hold(
                LightController.ATTRUBUTE_COLOR, LightController.DIRECTION_DOWN
            ),
            "arrow_left_release": lambda: self.release(),
            "arrow_right_hold": lambda: self.hold(
                LightController.ATTRUBUTE_COLOR, LightController.DIRECTION_UP
            ),
            "arrow_right_release": lambda: self.release(),
        }


class E1743Controller(LightController):
    # Different states reported from the controller:
    # on, off, brightness_up, brightness_down, brightness_stop

    def get_actions_mappings(self):
        return {
            "on": lambda: self.on(),
            "off": lambda: self.off(),
            "brightness_up": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_UP
            ),
            "brightness_down": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_DOWN
            ),
            "brightness_stop": lambda: self.release(),
        }


class ICTCG1Controller(LightController):
    # Different states reported from the controller:
    # rotate_left, rotate_left_quick
    # rotate_right, rotate_right_quick
    # rotate_stop

    def get_actions_mappings(self):
        return {
            "rotate_left": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_DOWN
            ),
            "rotate_left_quick": lambda: self.off(),
            "rotate_right": lambda: self.hold(
                LightController.ATTRUBUTE_BRIGHTNESS, LightController.DIRECTION_UP
            ),
            "rotate_right_quick": lambda: self.on_full(
                LightController.ATTRUBUTE_BRIGHTNESS
            ),
            "rotate_stop": lambda: self.release(),
        }
