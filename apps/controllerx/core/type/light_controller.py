from core.controller import ReleaseHoldController, action
from core.stepper import Stepper, MinMax

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10


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

    attribute_minmax = {"brightness": MinMax(1, 255), "color_temp": MinMax(153, 500)}
    index_color = 0
    value_attribute = None

    def initialize(self):
        super().initialize()
        self.light = self.get_light(self.args["light"])
        manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.manual_stepper = Stepper(attribute_minmax, manual_steps)
        self.automatic_stepper = Stepper(attribute_minmax, automatic_steps)
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
            self.attribute_minmax[attribute]["min"], attribute, Stepper.UP, 1
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
            direction == Stepper.UP
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
            self.value_attribute, attribute, direction, self.manual_stepper
        )

    @action
    async def hold(self, attribute, direction):
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        await super().hold(attribute, direction)

    async def hold_loop(self, attribute, direction):
        return await self.change_light_state(
            self.value_attribute, attribute, direction, self.automatic_stepper
        )

    async def change_light_state(self, old, attribute, direction, stepper):
        """
        This functions changes the state of the light depending on the previous
        value and attribute. It returns True when no more changes will need to be done.
        Otherwise, it returns False.
        """
        if attribute == "xy_color":
            self.index_color += Stepper.sign(direction)
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
        new_state_attribute, exceeded = stepper.step(old, attribute, direction)
        if self.check_smooth_power_on(
            attribute, direction, await self.get_state(self.light["name"])
        ):
            new_state_attribute = min_
            # The light needs to be turned on since the current state is off
            # and if the light is turned on with the brightness attribute,
            # the brightness state won't remain when turned of and on again.
            await self.on()
        attributes = {attribute: new_state_attribute, "transition": self.delay / 1000}
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


# class CustomLightController(LightController):
#
#     CUSTOM_LIGHT_ACTIONS = {
#         "click_on", self.on,
#         "click_off", self.off
#         "click_brightness_up", self.
#     }
#     def initialize(self):
#         self.custom_mapping = self.args["mapping"]
#         self.log(self.custom_mapping)
#         super().initialize()
#
#     def get_state_actions_mapping(self):
#         return {}
#
#     def get_event_actions_mapping(self):
#         return {}
