from functools import lru_cache
from typing import Any, Dict, List, Optional, Set, Type

from cx_const import Light, Number, PredefinedActionsMapping, StepperDir, StepperMode
from cx_core.color_helper import Color, get_color_wheel
from cx_core.controller import action
from cx_core.feature_support.light import LightSupport
from cx_core.integration import EventData
from cx_core.integration.deconz import DeCONZIntegration
from cx_core.integration.z2m import Z2MIntegration
from cx_core.release_hold_controller import ReleaseHoldController
from cx_core.stepper import MinMax, Stepper
from cx_core.stepper.bounce_stepper import BounceStepper
from cx_core.stepper.index_loop_stepper import IndexLoopStepper
from cx_core.stepper.loop_stepper import LoopStepper
from cx_core.stepper.stop_stepper import StopStepper
from cx_core.type_controller import Entity, TypeController

DEFAULT_MANUAL_STEPS = 10
DEFAULT_AUTOMATIC_STEPS = 10
DEFAULT_MIN_BRIGHTNESS = 1
DEFAULT_MAX_BRIGHTNESS = 255
DEFAULT_MIN_WHITE_VALUE = 1
DEFAULT_MAX_WHITE_VALUE = 255
DEFAULT_MIN_COLOR_TEMP = 153
DEFAULT_MAX_COLOR_TEMP = 500
DEFAULT_TRANSITION = 300
DEFAULT_ADD_TRANSITION = True
DEFAULT_TRANSITION_TURN_TOGGLE = False

ColorMode = str
# Once the minimum supported version of Python is 3.8,
# we can declare the ColorMode as a Literal
# ColorMode = Literal["auto", "xy_color", "color_temp"]

COLOR_MODES = {"hs", "xy", "rgb", "rgbw", "rgbww"}
STEPPER_MODES: Dict[str, Type[Stepper]] = {
    StepperMode.STOP: StopStepper,
    StepperMode.LOOP: LoopStepper,
    StepperMode.BOUNCE: BounceStepper,
}


class LightEntity(Entity):
    color_mode: ColorMode

    def __init__(
        self,
        name: str,
        entities: Optional[List[str]] = None,
        color_mode: ColorMode = "auto",
    ) -> None:
        super().__init__(name, entities)
        self.color_mode = color_mode


class LightController(TypeController[LightEntity], ReleaseHoldController):
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

    ATTRIBUTES_LIST = [
        ATTRIBUTE_BRIGHTNESS,
        ATTRIBUTE_WHITE_VALUE,
        ATTRIBUTE_COLOR,
        ATTRIBUTE_COLOR_TEMP,
        ATTRIBUTE_XY_COLOR,
    ]

    index_color = 0
    value_attribute = None

    # These are intermediate variables to store the checked value
    smooth_power_on_check: bool
    remove_transition_check: bool
    next_direction: Optional[str] = None

    manual_steps: Number
    automatic_steps: Number
    min_max_attributes: Dict[str, MinMax]

    domains = ["light"]
    entity_arg = "light"

    _supported_color_modes: Optional[Set[str]]

    async def init(self) -> None:
        self.manual_steps = self.args.get("manual_steps", DEFAULT_MANUAL_STEPS)
        self.automatic_steps = self.args.get("automatic_steps", DEFAULT_AUTOMATIC_STEPS)

        self.min_max_attributes = {
            self.ATTRIBUTE_BRIGHTNESS: MinMax(
                self.args.get("min_brightness", DEFAULT_MIN_BRIGHTNESS),
                self.args.get("max_brightness", DEFAULT_MAX_BRIGHTNESS),
            ),
            self.ATTRIBUTE_WHITE_VALUE: MinMax(
                self.args.get("min_white_value", DEFAULT_MIN_WHITE_VALUE),
                self.args.get("max_white_value", DEFAULT_MAX_WHITE_VALUE),
            ),
            self.ATTRIBUTE_COLOR_TEMP: MinMax(
                self.args.get("min_color_temp", DEFAULT_MIN_COLOR_TEMP),
                self.args.get("max_color_temp", DEFAULT_MAX_COLOR_TEMP),
            ),
        }

        self.transition = self.args.get("transition", DEFAULT_TRANSITION)
        self.color_wheel = get_color_wheel(
            self.args.get("color_wheel", "default_color_wheel")
        )
        self._supported_color_modes = self.args.get("supported_color_modes")

        self.smooth_power_on = self.args.get(
            "smooth_power_on", self.supports_smooth_power_on()
        )
        self.add_transition = self.args.get("add_transition", DEFAULT_ADD_TRANSITION)
        self.add_transition_turn_toggle = self.args.get(
            "add_transition_turn_toggle", DEFAULT_TRANSITION_TURN_TOGGLE
        )
        await super().init()

    def _get_entity_type(self) -> Type[LightEntity]:
        return LightEntity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            Light.ON: self.on,
            Light.OFF: self.off,
            Light.TOGGLE: self.toggle,
            Light.TOGGLE_FULL_BRIGHTNESS: (
                self.toggle_full,
                (LightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Light.TOGGLE_FULL_WHITE_VALUE: (
                self.toggle_full,
                (LightController.ATTRIBUTE_WHITE_VALUE,),
            ),
            Light.TOGGLE_FULL_COLOR_TEMP: (
                self.toggle_full,
                (LightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Light.TOGGLE_MIN_BRIGHTNESS: (
                self.toggle_min,
                (LightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Light.TOGGLE_MIN_WHITE_VALUE: (
                self.toggle_min,
                (LightController.ATTRIBUTE_WHITE_VALUE,),
            ),
            Light.TOGGLE_MIN_COLOR_TEMP: (
                self.toggle_min,
                (LightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Light.RELEASE: self.release,
            Light.ON_FULL_BRIGHTNESS: (
                self.on_full,
                (LightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Light.ON_FULL_WHITE_VALUE: (
                self.on_full,
                (LightController.ATTRIBUTE_WHITE_VALUE,),
            ),
            Light.ON_FULL_COLOR_TEMP: (
                self.on_full,
                (LightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Light.ON_MIN_BRIGHTNESS: (
                self.on_min,
                (LightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Light.ON_MIN_WHITE_VALUE: (
                self.on_min,
                (LightController.ATTRIBUTE_WHITE_VALUE,),
            ),
            Light.ON_MIN_COLOR_TEMP: (
                self.on_min,
                (LightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Light.SET_HALF_BRIGHTNESS: (
                self.set_value,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    0.5,
                ),
            ),
            Light.SET_HALF_WHITE_VALUE: (
                self.set_value,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    0.5,
                ),
            ),
            Light.SET_HALF_COLOR_TEMP: (
                self.set_value,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    0.5,
                ),
            ),
            Light.SYNC: self.sync,
            Light.CLICK: self.click,
            Light.CLICK_BRIGHTNESS_UP: (
                self.click,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.UP,
                ),
            ),
            Light.CLICK_BRIGHTNESS_DOWN: (
                self.click,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.DOWN,
                ),
            ),
            Light.CLICK_WHITE_VALUE_UP: (
                self.click,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    StepperDir.UP,
                ),
            ),
            Light.CLICK_WHITE_VALUE_DOWN: (
                self.click,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    StepperDir.DOWN,
                ),
            ),
            Light.CLICK_COLOR_UP: (
                self.click,
                (
                    LightController.ATTRIBUTE_COLOR,
                    StepperDir.UP,
                ),
            ),
            Light.CLICK_COLOR_DOWN: (
                self.click,
                (
                    LightController.ATTRIBUTE_COLOR,
                    StepperDir.DOWN,
                ),
            ),
            Light.CLICK_COLOR_TEMP_UP: (
                self.click,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.UP,
                ),
            ),
            Light.CLICK_COLOR_TEMP_DOWN: (
                self.click,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.DOWN,
                ),
            ),
            Light.CLICK_XY_COLOR_UP: (
                self.click,
                (
                    LightController.ATTRIBUTE_XY_COLOR,
                    StepperDir.UP,
                ),
            ),
            Light.CLICK_XY_COLOR_DOWN: (
                self.click,
                (
                    LightController.ATTRIBUTE_XY_COLOR,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD: self.hold,
            Light.HOLD_BRIGHTNESS_UP: (
                self.hold,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.UP,
                ),
            ),
            Light.HOLD_BRIGHTNESS_DOWN: (
                self.hold,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD_BRIGHTNESS_TOGGLE: (
                self.hold,
                (
                    LightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.TOGGLE,
                ),
            ),
            Light.HOLD_WHITE_VALUE_UP: (
                self.hold,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    StepperDir.UP,
                ),
            ),
            Light.HOLD_WHITE_VALUE_DOWN: (
                self.hold,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD_WHITE_VALUE_TOGGLE: (
                self.hold,
                (
                    LightController.ATTRIBUTE_WHITE_VALUE,
                    StepperDir.TOGGLE,
                ),
            ),
            Light.HOLD_COLOR_UP: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR,
                    StepperDir.UP,
                ),
            ),
            Light.HOLD_COLOR_DOWN: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD_COLOR_TOGGLE: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR,
                    StepperDir.TOGGLE,
                ),
            ),
            Light.HOLD_COLOR_TEMP_UP: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.UP,
                ),
            ),
            Light.HOLD_COLOR_TEMP_DOWN: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD_COLOR_TEMP_TOGGLE: (
                self.hold,
                (
                    LightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.TOGGLE,
                ),
            ),
            Light.HOLD_XY_COLOR_UP: (
                self.hold,
                (
                    LightController.ATTRIBUTE_XY_COLOR,
                    StepperDir.UP,
                ),
            ),
            Light.HOLD_XY_COLOR_DOWN: (
                self.hold,
                (
                    LightController.ATTRIBUTE_XY_COLOR,
                    StepperDir.DOWN,
                ),
            ),
            Light.HOLD_XY_COLOR_TOGGLE: (
                self.hold,
                (
                    LightController.ATTRIBUTE_XY_COLOR,
                    StepperDir.TOGGLE,
                ),
            ),
            Light.XYCOLOR_FROM_CONTROLLER: self.xycolor_from_controller,
            Light.COLORTEMP_FROM_CONTROLLER: self.colortemp_from_controller,
            Light.BRIGHTNESS_FROM_CONTROLLER: self.brightness_from_controller,
        }

    async def check_remove_transition(self, on_from_user: bool) -> bool:
        return (
            not self.add_transition
            or (on_from_user and not self.add_transition_turn_toggle)
            or await self.feature_support.not_supported(LightSupport.TRANSITION)
        )

    async def call_light_service(self, service: str, **attributes) -> None:
        if "transition" not in attributes:
            attributes["transition"] = self.transition / 1000
        if self.remove_transition_check:
            del attributes["transition"]
        await self.call_service(service, entity_id=self.entity.name, **attributes)

    async def _on(self, **attributes) -> None:
        await self.call_light_service("light/turn_on", **attributes)

    @action
    async def on(self, attributes: Optional[Dict[str, float]] = None) -> None:
        attributes = {} if attributes is None else attributes
        await self._on(**attributes)

    async def _off(self, **attributes) -> None:
        await self.call_light_service("light/turn_off", **attributes)

    @action
    async def off(self) -> None:
        await self._off()

    async def _toggle(self, **attributes) -> None:
        await self.call_light_service("light/toggle", **attributes)

    @action
    async def toggle(self, attributes: Optional[Dict[str, float]] = None) -> None:
        attributes = {} if attributes is None else attributes
        await self._toggle(**attributes)

    async def _set_value(self, attribute: str, fraction: float) -> None:
        fraction = max(0, min(fraction, 1))
        min_ = self.min_max_attributes[attribute].min
        max_ = self.min_max_attributes[attribute].max
        value = (max_ - min_) * fraction + min_
        await self._on(**{attribute: value})

    @action
    async def set_value(self, attribute: str, fraction: float) -> None:
        await self._set_value(attribute, fraction)

    @action
    async def toggle_full(self, attribute: str) -> None:
        await self._toggle(**{attribute: self.min_max_attributes[attribute].max})

    @action
    async def toggle_min(self, attribute: str) -> None:
        await self._toggle(**{attribute: self.min_max_attributes[attribute].min})

    async def _on_full(self, attribute: str) -> None:
        await self._set_value(attribute, 1)

    @action
    async def on_full(self, attribute: str) -> None:
        await self._on_full(attribute)

    async def _on_min(self, attribute: str) -> None:
        await self._set_value(attribute, 0)

    @action
    async def on_min(self, attribute: str) -> None:
        await self._on_min(attribute)

    @action
    async def sync(
        self,
        brightness: Optional[int] = None,
        color_temp: int = 370,  # 2700K light
        xy_color: Color = (0.323, 0.329),  # white colour
    ) -> None:
        attributes: Dict[Any, Any] = {}
        try:
            color_attribute = await self.get_attribute(LightController.ATTRIBUTE_COLOR)
            if color_attribute == LightController.ATTRIBUTE_COLOR_TEMP:
                attributes[color_attribute] = color_temp
            else:
                attributes[color_attribute] = list(xy_color)
        except ValueError:
            self.log(
                "⚠️ `sync` action will only change brightness",
                level="WARNING",
                ascii_encode=False,
            )
        await self._on(
            **attributes,
            brightness=(
                brightness
                or self.min_max_attributes[LightController.ATTRIBUTE_BRIGHTNESS].max
            ),
        )

    @action
    async def xycolor_from_controller(self, extra: Optional[EventData]) -> None:
        if extra is None:
            self.log("No event data present", level="WARNING")
            return
        if isinstance(self.integration, Z2MIntegration):
            if "action_color" not in extra:
                self.log(
                    "`action_color` is not present in the MQTT payload", level="WARNING"
                )
                return
            xy_color = extra["action_color"]
            await self._on(xy_color=[xy_color["x"], xy_color["y"]])
        elif isinstance(self.integration, DeCONZIntegration):
            if "xy" not in extra:
                self.log("`xy` is not present in the deCONZ event", level="WARNING")
                return
            await self._on(xy_color=list(extra["xy"]))

    @action
    async def colortemp_from_controller(self, extra: Optional[EventData]) -> None:
        if extra is None:
            self.log("No event data present", level="WARNING")
            return
        if isinstance(self.integration, Z2MIntegration):
            if "action_color_temperature" not in extra:
                self.log(
                    "`action_color_temperature` is not present in the MQTT payload",
                    level="WARNING",
                )
                return
            await self._on(color_temp=extra["action_color_temperature"])

    @action
    async def brightness_from_controller(self, extra: Optional[EventData]) -> None:
        if extra is None:
            self.log("No event data present", level="WARNING")
            return
        if isinstance(self.integration, Z2MIntegration):
            if "action_level" not in extra:
                self.log(
                    "`action_level` is not present in the MQTT payload",
                    level="WARNING",
                )
                return
            await self._on(brightness=extra["action_level"])

    @property
    async def supported_color_modes(self) -> Set[str]:
        if self._supported_color_modes is None or self.update_supported_features:
            supported_color_modes: List[str] = await self.get_entity_state(
                attribute="supported_color_modes"
            )
            if supported_color_modes is not None:
                self._supported_color_modes = set(supported_color_modes)
            else:
                raise ValueError(
                    f"`supported_color_modes` could not be read from `{self.entity}`. "
                    "Entity might not be available."
                )

        return self._supported_color_modes

    async def is_color_supported(self) -> bool:
        return len(COLOR_MODES.intersection(await self.supported_color_modes)) > 0

    async def is_colortemp_supported(self) -> bool:
        return "color_temp" in await self.supported_color_modes

    @lru_cache(maxsize=None)
    def get_stepper(self, attribute: str, steps: Number, mode: str) -> Stepper:
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            return IndexLoopStepper(len(self.color_wheel))
        if mode not in STEPPER_MODES:
            raise ValueError(
                f"`{mode}` mode is not available. Options are: {list(STEPPER_MODES.keys())}"
            )
        stepper_cls = STEPPER_MODES[mode]
        return stepper_cls(self.min_max_attributes[attribute], steps)

    async def get_attribute(self, attribute: str) -> str:
        if attribute == LightController.ATTRIBUTE_COLOR:
            if self.entity.color_mode == "auto":
                if await self.is_color_supported():
                    return LightController.ATTRIBUTE_XY_COLOR
                elif await self.is_colortemp_supported():
                    return LightController.ATTRIBUTE_COLOR_TEMP
                else:
                    raise ValueError(
                        "This light does not support xy_color or color_temp"
                    )
            else:
                return self.entity.color_mode
        else:
            return attribute

    async def get_value_attribute(self, attribute: str) -> Number:
        if self.smooth_power_on_check:
            return 0
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            return 0
        elif (
            attribute == LightController.ATTRIBUTE_BRIGHTNESS
            or attribute == LightController.ATTRIBUTE_WHITE_VALUE
            or attribute == LightController.ATTRIBUTE_COLOR_TEMP
        ):
            value = await self.get_entity_state(attribute=attribute)
            if value is None:
                raise ValueError(
                    f"Value for `{attribute}` attribute could not be retrieved "
                    f"from `{self.entity.main}`. "
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
            direction != StepperDir.DOWN
            and attribute == self.ATTRIBUTE_BRIGHTNESS
            and self.smooth_power_on
            and light_state == "off"
        )

    async def before_action(self, action: str, *args, **kwargs) -> bool:
        to_return = True
        if action in ("click", "hold"):
            if len(args) == 2:
                attribute, direction = args
            elif "attribute" in kwargs and "direction" in kwargs:
                attribute, direction = kwargs["attribute"], kwargs["direction"]
            else:
                raise ValueError(
                    f"`attribute` and `direction` are mandatory fields for `{action}` action"
                )
            light_state: str = await self.get_entity_state()
            self.smooth_power_on_check = self.check_smooth_power_on(
                attribute, direction, light_state
            )
            self.remove_transition_check = await self.check_remove_transition(
                on_from_user=False
            )
            self.next_direction = None
            to_return = (light_state == "on") or self.smooth_power_on_check
        else:
            self.remove_transition_check = await self.check_remove_transition(
                on_from_user=True
            )
            self.smooth_power_on_check = False
        return await super().before_action(action, *args, **kwargs) and to_return

    @action
    async def click(
        self,
        attribute: str,
        direction: str,
        mode: str = StepperMode.STOP,
        steps: Optional[Number] = None,
    ) -> None:
        attribute = self.get_option(
            attribute, LightController.ATTRIBUTES_LIST, "`click` action"
        )
        direction = self.get_option(
            direction, [StepperDir.UP, StepperDir.DOWN], "`click` action"
        )
        mode = self.get_option(
            mode, [StepperMode.STOP, StepperMode.LOOP], "`click` action"
        )
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            self.get_stepper(attribute, steps or self.manual_steps, mode),
            "click",
        )

    @action
    async def hold(  # type: ignore
        self,
        attribute: str,
        direction: str,
        mode: str = StepperMode.STOP,
        steps: Optional[Number] = None,
    ) -> None:
        attribute = self.get_option(
            attribute, LightController.ATTRIBUTES_LIST, "`hold` action"
        )
        direction = self.get_option(
            direction,
            [StepperDir.UP, StepperDir.DOWN, StepperDir.TOGGLE],
            "`hold` action",
        )
        mode = self.get_option(
            mode,
            [StepperMode.STOP, StepperMode.LOOP, StepperMode.BOUNCE],
            "`hold` action",
        )
        attribute = await self.get_attribute(attribute)
        self.value_attribute = await self.get_value_attribute(attribute)
        self.log(
            f"Attribute value before running the hold action: {self.value_attribute}",
            level="DEBUG",
        )
        stepper = self.get_stepper(attribute, steps or self.automatic_steps, mode)
        if direction == StepperDir.TOGGLE:
            self.log(
                f"Previous direction: {stepper.previous_direction}",
                level="DEBUG",
            )
        direction = stepper.get_direction(self.value_attribute, direction)
        self.log(f"Going direction: {direction}", level="DEBUG")
        await super().hold(attribute, direction, stepper)

    async def hold_loop(self, attribute: str, direction: str, stepper: Stepper) -> bool:  # type: ignore
        if self.value_attribute is None:
            return True
        return await self.change_light_state(
            self.value_attribute,
            attribute,
            direction,
            stepper,
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
        direction = self.next_direction or direction
        if attribute == LightController.ATTRIBUTE_XY_COLOR:
            stepper_output = stepper.step(self.index_color, direction)
            self.index_color = int(stepper_output.next_value)
            xy_color = self.color_wheel[self.index_color]
            attributes = {attribute: list(xy_color)}
            if action_type == "hold":
                attributes["transition"] = self.delay / 1000
            await self._on(**attributes)
            # In case of xy_color mode it never finishes the loop, the hold loop
            # will only stop if the hold action is called when releasing the button.
            # I haven't experimented any problems with it, but a future implementation
            # would be to force the loop to stop after 4 or 5 loops as a safety measure.
            return False
        if self.smooth_power_on_check:
            await self._on_min(attribute)
            # # After smooth power on, the light should not brighten up.
            return True
        stepper_output = stepper.step(old, direction)
        self.next_direction = stepper_output.next_direction
        attributes = {attribute: stepper_output.next_value}
        if action_type == "hold":
            attributes["transition"] = self.delay / 1000
        await self._on(**attributes)
        self.value_attribute = stepper_output.next_value
        return stepper_output.exceeded

    def supports_smooth_power_on(self) -> bool:
        """
        This function can be overrided for each device to indicate the default behaviour of the controller
        when the associated light is off and an event for incrementing brightness is received.
        Returns True if the associated light should be turned on with minimum brightness if an event for incrementing
        brightness is received, while the lamp is off.
        The behaviour can be overridden by the user with the 'smooth_power_on' option in app configuration.
        """
        return False
