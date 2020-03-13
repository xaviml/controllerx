from collections import defaultdict

from const import Light
from core.controller import ReleaseHoldController, action
from core import light_features
from core.stepper import Stepper
from core.stepper.circular_stepper import CircularStepper
from core.stepper.minmax_stepper import MinMaxStepper

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_MIN_BRIGHTNESS = 1
DEFAULT_MAX_BRIGHTNESS = 255
DEFAULT_MIN_COLOR_TEMP = 153
DEFAULT_MAX_COLOR_TEMP = 500
DEFAULT_TRANSITION = 300


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
    # With the following attribute, it will select color_temp or xy_color, depending on the light.
    ATTRIBUTE_COLOR = "color"
    ATTRIBUTE_COLOR_TEMP = "color_temp"
    ATTRIBUTE_XY_COLOR = "xy_color"

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
        (0.323, 0.329),  # 12; white color middle
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

    index_color = 0
    value_attribute = None

    def initialize(self):
        super().initialize()
        self.light = self.get_light(self.args["light"])
        manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.min_brightness = self.args.get("min_brightness", DEFAULT_MIN_BRIGHTNESS)
        self.max_brightness = self.args.get("max_brightness", DEFAULT_MAX_BRIGHTNESS)
        self.min_color_temp = self.args.get("min_color_temp", DEFAULT_MIN_COLOR_TEMP)
        self.max_color_temp = self.args.get("max_color_temp", DEFAULT_MAX_COLOR_TEMP)
        self.transition = self.args.get("transition", DEFAULT_TRANSITION)
        color_stepper = CircularStepper(0, len(self.colors) - 1, len(self.colors))
        self.manual_steppers = {
            LightController.ATTRIBUTE_BRIGHTNESS: MinMaxStepper(
                self.min_brightness, self.max_brightness, manual_steps
            ),
            LightController.ATTRIBUTE_COLOR_TEMP: MinMaxStepper(
                self.min_color_temp, self.max_color_temp, manual_steps
            ),
            LightController.ATTRIBUTE_XY_COLOR: color_stepper,
        }
        self.automatic_steppers = {
            LightController.ATTRIBUTE_BRIGHTNESS: MinMaxStepper(
                self.min_brightness, self.max_brightness, automatic_steps
            ),
            LightController.ATTRIBUTE_COLOR_TEMP: MinMaxStepper(
                self.min_color_temp, self.max_color_temp, automatic_steps
            ),
            LightController.ATTRIBUTE_XY_COLOR: color_stepper,
        }
        self.smooth_power_on = self.args.get(
            "smooth_power_on", self.supports_smooth_power_on()
        )

    def get_type_actions_mapping(self):
        return {
            Light.ON: self.on,
            Light.OFF: self.off,
            Light.TOGGLE: self.toggle,
            Light.RELEASE: self.release,
            Light.ON_FULL_BRIGHTNESS: (
                self.on_full,
                LightController.ATTRIBUTE_BRIGHTNESS,
            ),
            Light.ON_FULL_COLOR_TEMP: (
                self.on_full,
                LightController.ATTRIBUTE_COLOR_TEMP,
            ),
            Light.ON_MIN_BRIGHTNESS: (
                self.on_min,
                LightController.ATTRIBUTE_BRIGHTNESS,
            ),
            Light.ON_MIN_COLOR_TEMP: (
                self.on_min,
                LightController.ATTRIBUTE_COLOR_TEMP,
            ),
            Light.SET_HALF_BRIGHTNESS: (
                self.set_value,
                LightController.ATTRIBUTE_BRIGHTNESS,
                0.5,
            ),
            Light.SET_HALF_COLOR_TEMP: (
                self.set_value,
                LightController.ATTRIBUTE_COLOR_TEMP,
                0.5,
            ),
            Light.SYNC: self.sync,
            Light.CLICK_BRIGHTNESS_UP: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            Light.CLICK_BRIGHTNESS_DOWN: (
                self.click,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            Light.CLICK_COLOR_UP: (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.UP,
            ),
            Light.CLICK_COLOR_DOWN: (
                self.click,
                LightController.ATTRIBUTE_COLOR,
                Stepper.DOWN,
            ),
            Light.CLICK_COLOR_TEMP_UP: (
                self.click,
                LightController.ATTRIBUTE_COLOR_TEMP,
                Stepper.UP,
            ),
            Light.CLICK_COLOR_TEMP_DOWN: (
                self.click,
                LightController.ATTRIBUTE_COLOR_TEMP,
                Stepper.DOWN,
            ),
            Light.CLICK_XY_COLOR_UP: (
                self.click,
                LightController.ATTRIBUTE_XY_COLOR,
                Stepper.UP,
            ),
            Light.CLICK_XY_COLOR_DOWN: (
                self.click,
                LightController.ATTRIBUTE_XY_COLOR,
                Stepper.DOWN,
            ),
            Light.HOLD_BRIGHTNESS_UP: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.UP,
            ),
            Light.HOLD_BRIGHTNESS_DOWN: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.DOWN,
            ),
            Light.HOLD_BRIGHTNESS_TOGGLE: (
                self.hold,
                LightController.ATTRIBUTE_BRIGHTNESS,
                Stepper.TOGGLE,
            ),
            Light.HOLD_COLOR_UP: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                Stepper.UP,
            ),
            Light.HOLD_COLOR_DOWN: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                Stepper.DOWN,
            ),
            Light.HOLD_COLOR_TOGGLE: (
                self.hold,
                LightController.ATTRIBUTE_COLOR,
                Stepper.TOGGLE,
            ),
            Light.HOLD_COLOR_TEMP_UP: (
                self.hold,
                LightController.ATTRIBUTE_COLOR_TEMP,
                Stepper.UP,
            ),
            Light.HOLD_COLOR_TEMP_DOWN: (
                self.hold,
                LightController.ATTRIBUTE_COLOR_TEMP,
                Stepper.DOWN,
            ),
            Light.HOLD_COLOR_TEMP_TOGGLE: (
                self.hold,
                LightController.ATTRIBUTE_COLOR_TEMP,
                Stepper.TOGGLE,
            ),
            Light.HOLD_XY_COLOR_UP: (
                self.hold,
                LightController.ATTRIBUTE_XY_COLOR,
                Stepper.UP,
            ),
            Light.HOLD_XY_COLOR_DOWN: (
                self.hold,
                LightController.ATTRIBUTE_XY_COLOR,
                Stepper.DOWN,
            ),
            Light.HOLD_XY_COLOR_TOGGLE: (
                self.hold,
                LightController.ATTRIBUTE_XY_COLOR,
                Stepper.TOGGLE,
            ),
        }

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
        if "transition" not in attributes:
            attributes["transition"] = self.transition / 1000
        self.call_service(
            "homeassistant/turn_on", entity_id=self.light["name"], **attributes,
        )

    @action
    async def off(self):
        self.call_service("homeassistant/turn_off", entity_id=self.light["name"])

    @action
    async def toggle(self):
        self.call_service("homeassistant/toggle", entity_id=self.light["name"])

    @action
    async def set_value(self, attribute, fraction):
        fraction = max(0, min(fraction, 1))
        stepper = self.automatic_steppers[attribute]
        min_ = stepper.minmax.min
        max_ = stepper.minmax.max
        value = (max_ - min_) * fraction + min_
        await self.on(**{attribute: value})

    @action
    async def on_full(self, attribute):
        stepper = self.automatic_steppers[attribute]
        stepper.previous_direction = Stepper.TOGGLE_UP
        await self.set_value(attribute, 1)

    @action
    async def on_min(self, attribute):
        stepper = self.automatic_steppers[attribute]
        stepper.previous_direction = Stepper.TOGGLE_DOWN
        await self.set_value(attribute, 0)

    @action
    async def sync(self):
        await self.on(brightness=self.max_brightness, transition=0)
        attributes = {}
        try:
            color_attribute = await self.get_attribute(LightController.ATTRIBUTE_COLOR)
            if color_attribute == LightController.ATTRIBUTE_COLOR_TEMP:
                attributes[color_attribute] = 370  # 2700K light
            else:
                self.index_color = 12  # white colour
                attributes[color_attribute] = self.colors[self.index_color]
        except:
            self.log("sync action will only change brightness", level="DEBUG")
        if attributes != {}:
            await self.on(**attributes)

    async def get_attribute(self, attribute):
        if attribute == LightController.ATTRIBUTE_COLOR:
            bitfield = await self.get_entity_state(
                self.light["name"], attribute="supported_features"
            )
            supported_features = light_features.decode(bitfield)
            if self.light["color_mode"] == "auto":
                if light_features.SUPPORT_COLOR in supported_features:
                    return LightController.ATTRIBUTE_XY_COLOR
                elif light_features.SUPPORT_COLOR_TEMP in supported_features:
                    return LightController.ATTRIBUTE_COLOR_TEMP
                else:
                    raise ValueError(
                        "This light does not support xy_color or color_temp"
                    )
            else:
                return self.light["color_mode"]
        else:
            return attribute

    async def get_value_attribute(self, attribute):
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            return None
        else:
            return await self.get_entity_state(self.light["name"], attribute)

    def check_smooth_power_on(self, attribute, direction, light_state):
        return (
            direction != Stepper.DOWN
            and attribute == self.ATTRIBUTE_BRIGHTNESS
            and self.smooth_power_on
            and light_state == "off"
        )

    async def before_action(self, action, *args, **kwargs):
        to_return = True
        if action == "click" or action == "hold":
            attribute, direction = args
            light_state = await self.get_entity_state(self.light["name"])
            to_return = light_state == "on" or self.check_smooth_power_on(
                attribute, direction, light_state
            )
        return await super().before_action(action, *args, **kwargs) and to_return

    @action
    async def click(self, attribute, direction):
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            self.manual_steppers[attribute],
            "click",
        )

    @action
    async def hold(self, attribute, direction):
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        direction = self.automatic_steppers[attribute].get_direction(direction)
        await super().hold(attribute, direction)

    async def hold_loop(self, attribute, direction):
        return await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            self.automatic_steppers[attribute],
            "hold",
        )

    async def change_light_state(self, old, attribute, direction, stepper, action_type):
        """
        This functions changes the state of the light depending on the previous
        value and attribute. It returns True when no more changes will need to be done.
        Otherwise, it returns False.
        """
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            self.index_color, _ = stepper.step(self.index_color, direction)
            new_state_attribute = self.colors[self.index_color]
            attributes = {attribute: new_state_attribute}
            if action_type == "hold":
                attributes["transition"] = self.delay / 1000
            await self.on(**attributes)
            # In case of xy_color mode it never finishes the loop, the hold loop
            # will only stop if the hold action is called when releasing the button.
            # I haven't experimented any problems with it, but a future implementation
            # would be to force the loop to stop after 4 or 5 loops as a safety measure.
            return False
        self.log(f"Attribute: {attribute}; Current value: {old}", level="DEBUG")
        if self.check_smooth_power_on(
            attribute, direction, await self.get_entity_state(self.light["name"])
        ):
            await self.on_min(attribute)
            # # After smooth power on, the light should not brighten up.
            return True
        else:
            new_state_attribute, exceeded = stepper.step(old, direction)
        attributes = {attribute: new_state_attribute}
        if action_type == "hold":
            attributes["transition"] = self.delay / 1000
        await self.on(**attributes)
        self.value_attribute = new_state_attribute
        return exceeded

    def supports_smooth_power_on(self):
        """
        This function can be overrided for each device to indicate the default behaviour of the controller
        when the associated light is off and an event for incrementing brightness is received.
        Returns True if the associated light should be turned on with minimum brightness if an event for incrementing
        brightness is received, while the lamp is off.
        The behaviour can be overridden by the user with the 'smooth_power_on' option in app configuration.
        """
        return False
