from typing import Any, Dict, Union

from cx_const import Light, TypeActionsMapping
from cx_core.controller import ReleaseHoldController, TypeController, action
from cx_core.feature_support.light import LightSupport
from cx_core.stepper import Stepper
from cx_core.stepper.circular_stepper import CircularStepper
from cx_core.stepper.minmax_stepper import MinMaxStepper
from cx_core.color_helper import get_color_wheel

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_MIN_BRIGHTNESS = 1
DEFAULT_MAX_BRIGHTNESS = 254
DEFAULT_MIN_WHITE_VALUE = 1
DEFAULT_MAX_WHITE_VALUE = 254
DEFAULT_MIN_COLOR_TEMP = 153
DEFAULT_MAX_COLOR_TEMP = 500
DEFAULT_TRANSITION = 300

LightEntity = Dict[str, str]


class LightController(TypeController, ReleaseHoldController):
    """
    This is the main class that controls the lights for different devices.
    Type of actions:
        - On/Off/Toggle
        - Brightness click and hold
        - Color temperature click and hold
        - xy color click and hold
    If a light supports xy_color and color_temperature, then xy_color will be the
    default functionality. Parameters taken:
        - controller (required): Inherited from Controller
        - light (required): This is either the light entity name or a dictionary as
          {name: string, color_mode: auto | xy_color | color_temp}
        - delay (optional): Inherited from ReleaseHoldController
        - manual_steps (optional): Number of steps to go from min to max when clicking.
        - automatic_steps (optional): Number of steps to go from min to max when smoothing.
    """

    ATTRIBUTE_BRIGHTNESS = "brightness"
    ATTRIBUTE_WHITE_VALUE = "white_value"
    # With the following attribute, it will select color_temp or xy_color, depending on the light.
    ATTRIBUTE_COLOR = "color"
    ATTRIBUTE_COLOR_TEMP = "color_temp"
    ATTRIBUTE_XY_COLOR = "xy_color"

    index_color = 0
    value_attribute = None

    async def initialize(self) -> None:
        self.light = self.get_light(self.args["light"])
        await self.check_domain(self.light["name"])
        manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)
        self.min_brightness = self.args.get("min_brightness", DEFAULT_MIN_BRIGHTNESS)
        self.max_brightness = self.args.get("max_brightness", DEFAULT_MAX_BRIGHTNESS)
        self.min_white_value = self.args.get("min_white_value", DEFAULT_MIN_WHITE_VALUE)
        self.max_white_value = self.args.get("max_white_value", DEFAULT_MAX_WHITE_VALUE)
        self.min_color_temp = self.args.get("min_color_temp", DEFAULT_MIN_COLOR_TEMP)
        self.max_color_temp = self.args.get("max_color_temp", DEFAULT_MAX_COLOR_TEMP)
        self.transition = self.args.get("transition", DEFAULT_TRANSITION)
        self.color_wheel = get_color_wheel(
            self.args.get("color_wheel", "default_color_wheel")
        )

        color_stepper = CircularStepper(
            0, len(self.color_wheel) - 1, len(self.color_wheel)
        )
        self.manual_steppers: Dict[str, Stepper] = {
            LightController.ATTRIBUTE_BRIGHTNESS: MinMaxStepper(
                self.min_brightness, self.max_brightness, manual_steps
            ),
            LightController.ATTRIBUTE_WHITE_VALUE: MinMaxStepper(
                self.min_white_value, self.max_white_value, manual_steps
            ),
            LightController.ATTRIBUTE_COLOR_TEMP: MinMaxStepper(
                self.min_color_temp, self.max_color_temp, manual_steps
            ),
            LightController.ATTRIBUTE_XY_COLOR: color_stepper,
        }
        self.automatic_steppers: Dict[str, Stepper] = {
            LightController.ATTRIBUTE_BRIGHTNESS: MinMaxStepper(
                self.min_brightness, self.max_brightness, automatic_steps
            ),
            LightController.ATTRIBUTE_WHITE_VALUE: MinMaxStepper(
                self.min_white_value, self.max_white_value, automatic_steps
            ),
            LightController.ATTRIBUTE_COLOR_TEMP: MinMaxStepper(
                self.min_color_temp, self.max_color_temp, automatic_steps
            ),
            LightController.ATTRIBUTE_XY_COLOR: color_stepper,
        }
        self.smooth_power_on = self.args.get(
            "smooth_power_on", self.supports_smooth_power_on()
        )
        self.add_transition = self.args.get("add_transition", True)
        self.add_transition_turn_toggle = self.args.get(
            "add_transition_turn_toggle", False
        )

        self.supported_features = LightSupport(self.light["name"], self)
        await super().initialize()

    def get_domain(self) -> str:
        return "light"

    def get_type_actions_mapping(self,) -> TypeActionsMapping:
        return {
            Light.ON: self.on,
            Light.OFF: self.off,
            Light.TOGGLE: self.toggle,
            Light.RELEASE: self.release,
            Light.ON_FULL_BRIGHTNESS: (
                self.on_full,
                LightController.ATTRIBUTE_BRIGHTNESS,
            ),
            Light.ON_FULL_WHITE_VALUE: (
                self.on_full,
                LightController.ATTRIBUTE_WHITE_VALUE,
            ),
            Light.ON_FULL_COLOR_TEMP: (
                self.on_full,
                LightController.ATTRIBUTE_COLOR_TEMP,
            ),
            Light.ON_MIN_BRIGHTNESS: (
                self.on_min,
                LightController.ATTRIBUTE_BRIGHTNESS,
            ),
            Light.ON_MIN_WHITE_VALUE: (
                self.on_min,
                LightController.ATTRIBUTE_WHITE_VALUE,
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
            Light.SET_HALF_WHITE_VALUE: (
                self.set_value,
                LightController.ATTRIBUTE_WHITE_VALUE,
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
            Light.CLICK_WHITE_VALUE_UP: (
                self.click,
                LightController.ATTRIBUTE_WHITE_VALUE,
                Stepper.UP,
            ),
            Light.CLICK_WHITE_VALUE_DOWN: (
                self.click,
                LightController.ATTRIBUTE_WHITE_VALUE,
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
            Light.HOLD_WHITE_VALUE_UP: (
                self.hold,
                LightController.ATTRIBUTE_WHITE_VALUE,
                Stepper.UP,
            ),
            Light.HOLD_WHITE_VALUE_DOWN: (
                self.hold,
                LightController.ATTRIBUTE_WHITE_VALUE,
                Stepper.DOWN,
            ),
            Light.HOLD_WHITE_VALUE_TOGGLE: (
                self.hold,
                LightController.ATTRIBUTE_WHITE_VALUE,
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

    def get_light(self, light: Union[str, dict]) -> LightEntity:
        if isinstance(light, str):
            return {"name": light, "color_mode": "auto"}
        elif isinstance(light, dict):
            color_mode = light.get("color_mode", "auto")
            return {"name": light["name"], "color_mode": color_mode}
        else:
            raise ValueError(
                f"Type {type(light)} is not supported for `light` attribute"
            )

    async def call_light_service(
        self, service: str, turned_toggle: bool, **attributes
    ) -> None:

        if "transition" not in attributes:
            attributes["transition"] = self.transition / 1000
        if (
            await self.supported_features.not_supported(LightSupport.TRANSITION)
            or not self.add_transition
            or (turned_toggle and not self.add_transition_turn_toggle)
        ):
            del attributes["transition"]
        await self.call_service(service, entity_id=self.light["name"], **attributes)

    @action
    async def on(self, light_on: bool = None, **attributes) -> None:
        if light_on is None:
            light_state = await self.get_entity_state(self.light["name"])
            light_on = light_state == "on"
        await self.call_light_service(
            "light/turn_on", turned_toggle=not light_on, **attributes
        )

    @action
    async def off(self, **attributes) -> None:
        await self.call_light_service(
            "light/turn_off", turned_toggle=True, **attributes
        )

    @action
    async def toggle(self, **attributes) -> None:
        await self.call_light_service("light/toggle", turned_toggle=True, **attributes)

    @action
    async def set_value(
        self, attribute: str, fraction: float, light_on: bool = None
    ) -> None:
        fraction = max(0, min(fraction, 1))
        stepper = self.automatic_steppers[attribute]
        if isinstance(stepper, MinMaxStepper):
            min_ = stepper.minmax.min
            max_ = stepper.minmax.max
            value = (max_ - min_) * fraction + min_
            await self.on(light_on=light_on, **{attribute: value})

    @action
    async def on_full(self, attribute: str, light_on: bool = None) -> None:
        await self.set_value(attribute, 1, light_on=light_on)

    @action
    async def on_min(self, attribute: str, light_on: bool = None) -> None:
        await self.set_value(attribute, 0, light_on=light_on)

    @action
    async def sync(self) -> None:
        attributes: Dict[Any, Any] = {}
        try:
            color_attribute = await self.get_attribute(LightController.ATTRIBUTE_COLOR)
            if color_attribute == LightController.ATTRIBUTE_COLOR_TEMP:
                attributes[color_attribute] = 370  # 2700K light
            else:
                attributes[color_attribute] = (0.323, 0.329)  # white colour
        except ValueError:
            self.log("⚠️ `sync` action will only change brightness", level="WARNING")
        await self.on(**attributes, brightness=self.max_brightness)

    async def get_attribute(self, attribute: str) -> str:
        if attribute == LightController.ATTRIBUTE_COLOR:
            if self.light["color_mode"] == "auto":
                if await self.supported_features.is_supported(LightSupport.COLOR):
                    return LightController.ATTRIBUTE_XY_COLOR
                elif await self.supported_features.is_supported(
                    LightSupport.COLOR_TEMP
                ):
                    return LightController.ATTRIBUTE_COLOR_TEMP
                else:
                    raise ValueError(
                        "This light does not support xy_color or color_temp"
                    )
            else:
                return self.light["color_mode"]
        else:
            return attribute

    async def get_value_attribute(
        self, attribute: str, direction: str
    ) -> Union[float, int]:
        if self.check_smooth_power_on(
            attribute, direction, await self.get_entity_state(self.light["name"])
        ):
            return 0
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            return 0
        elif (
            attribute == LightController.ATTRIBUTE_BRIGHTNESS
            or attribute == LightController.ATTRIBUTE_WHITE_VALUE
            or attribute == LightController.ATTRIBUTE_COLOR_TEMP
        ):
            value = await self.get_entity_state(self.light["name"], attribute)
            if value is None:
                raise ValueError(
                    f"Value for `{attribute}` attribute could not be retrieved "
                    f"from `{self.light['name']}`. "
                    "Check the FAQ to know more about this error: "
                    "https://xaviml.github.io/controllerx/faq"
                )
            else:
                try:
                    return float(value)
                except ValueError:
                    raise ValueError(
                        f"Attribute `{attribute}` with `{value}` as a value "
                        "could not be converted to float"
                    )
        else:
            raise ValueError(f"Attribute `{attribute}` not expected")

    def check_smooth_power_on(
        self, attribute: str, direction: str, light_state: str
    ) -> bool:
        return (
            direction != Stepper.DOWN
            and attribute == self.ATTRIBUTE_BRIGHTNESS
            and self.smooth_power_on
            and light_state == "off"
        )

    async def before_action(self, action: str, *args, **kwargs) -> bool:
        to_return = True
        if action == "click" or action == "hold":
            attribute, direction = args
            light_state = await self.get_entity_state(self.light["name"])
            to_return = light_state == "on" or self.check_smooth_power_on(
                attribute, direction, light_state
            )
        return await super().before_action(action, *args, **kwargs) and to_return

    @action
    async def click(self, attribute: str, direction: str) -> None:
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute, direction)
        await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            self.manual_steppers[attribute],
            "click",
        )

    @action
    async def hold(self, attribute: str, direction: str) -> None:
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute, direction)
        direction = self.automatic_steppers[attribute].get_direction(
            self.value_attribute, direction
        )
        await super().hold(attribute, direction)

    async def hold_loop(self, attribute: str, direction: str) -> bool:  # type: ignore
        # Is value_attribute is None, then we stop the loop
        if self.value_attribute is None:
            return True
        return await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            self.automatic_steppers[attribute],
            "hold",
        )

    async def change_light_state(
        self,
        old: float,
        attribute: str,
        direction: str,
        stepper: Stepper,
        action_type: str,
    ) -> bool:
        """
        This functions changes the state of the light depending on the previous
        value and attribute. It returns True when no more changes will need to be done.
        Otherwise, it returns False.
        """
        attributes: Dict[str, Any]
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            index_color, _ = stepper.step(self.index_color, direction)
            self.index_color = int(index_color)
            xy_color = self.color_wheel[self.index_color]
            attributes = {attribute: xy_color}
            if action_type == "hold":
                attributes["transition"] = self.delay / 1000
            await self.on(**attributes, light_on=True)
            # In case of xy_color mode it never finishes the loop, the hold loop
            # will only stop if the hold action is called when releasing the button.
            # I haven't experimented any problems with it, but a future implementation
            # would be to force the loop to stop after 4 or 5 loops as a safety measure.
            return False
        if self.check_smooth_power_on(
            attribute, direction, await self.get_entity_state(self.light["name"])
        ):
            await self.on_min(attribute, light_on=False)
            # # After smooth power on, the light should not brighten up.
            return True
        new_state_attribute, exceeded = stepper.step(old, direction)
        attributes = {attribute: new_state_attribute}
        if action_type == "hold":
            attributes["transition"] = self.delay / 1000
        await self.on(**attributes, light_on=True)
        self.value_attribute = new_state_attribute
        return exceeded

    def supports_smooth_power_on(self) -> bool:
        """
        This function can be overrided for each device to indicate the default behaviour of the controller
        when the associated light is off and an event for incrementing brightness is received.
        Returns True if the associated light should be turned on with minimum brightness if an event for incrementing
        brightness is received, while the lamp is off.
        The behaviour can be overridden by the user with the 'smooth_power_on' option in app configuration.
        """
        return False
