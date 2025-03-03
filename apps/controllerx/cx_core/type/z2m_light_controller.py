import json
from collections.abc import Awaitable
from functools import lru_cache
from typing import Annotated, Any, Callable, Literal, Optional

from cx_const import PredefinedActionsMapping, StepperDir, Z2MLight
from cx_core.controller import Controller, action
from cx_core.integration import EventData
from cx_core.integration.z2m import Z2MIntegration
from cx_core.stepper import InvertStepper, MinMax
from cx_core.type_controller import Entity, TypeController

DEFAULT_CLICK_STEPS = 70
DEFAULT_HOLD_STEPS = 70
DEFAULT_TRANSITION = 0.5
DEFAULT_MODE = "ha"
DEFAULT_TOPIC_PREFIX = "zigbee2mqtt"

Mode = Annotated[str, Literal["ha", "mqtt"]]


class Z2MLightEntity(Entity):
    mode: Mode
    topic_prefix: str

    def __init__(
        self,
        name: str,
        entities: Optional[list[str]] = None,
        mode: Mode = DEFAULT_MODE,
        topic_prefix: str = DEFAULT_TOPIC_PREFIX,
    ) -> None:
        super().__init__(name, entities)
        mode = Controller.get_option(mode, ["ha", "mqtt"])
        self.mode = mode
        self.topic_prefix = topic_prefix


class Z2MLightController(TypeController[Z2MLightEntity]):
    """
    This is the main class that controls the Zigbee2MQTT lights for different devices.
    Type of actions:
        - On/Off/Toggle
        - Brightness click and hold
        - Color temp click and hold
    """

    ATTRIBUTE_BRIGHTNESS = "brightness"
    ATTRIBUTE_COLOR_TEMP = "color_temp"

    ATTRIBUTES_LIST = [
        ATTRIBUTE_BRIGHTNESS,
        ATTRIBUTE_COLOR_TEMP,
    ]

    MIN_MAX_ATTR = {
        ATTRIBUTE_BRIGHTNESS: MinMax(min=1, max=254),
        ATTRIBUTE_COLOR_TEMP: MinMax(min=250, max=454),
    }

    entity_arg = "light"

    click_steps: float
    hold_steps: float
    transition: float
    use_onoff: bool

    hold_attribute: Optional[str]

    _mqtt_fn: dict[Mode, Callable[[str, str], Awaitable[None]]]

    async def init(self) -> None:
        self.click_steps = self.args.get("click_steps", DEFAULT_CLICK_STEPS)
        self.hold_steps = self.args.get("hold_steps", DEFAULT_HOLD_STEPS)
        self.transition = self.args.get("transition", DEFAULT_TRANSITION)
        self.use_onoff = self.args.get("use_onoff", False)

        self._mqtt_fn = {
            "ha": self._ha_mqtt_call,
            "mqtt": self._mqtt_plugin_call,
        }
        self.hold_attribute = None

        await super().init()

    def _get_entity_type(self) -> type[Z2MLightEntity]:
        return Z2MLightEntity

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {
            Z2MLight.ON: self.on,
            Z2MLight.OFF: self.off,
            Z2MLight.TOGGLE: self.toggle,
            Z2MLight.RELEASE: self.release,
            Z2MLight.ON_FULL_BRIGHTNESS: (
                self.on_full,
                (Z2MLightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Z2MLight.ON_FULL_COLOR_TEMP: (
                self.on_full,
                (Z2MLightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Z2MLight.ON_MIN_BRIGHTNESS: (
                self.on_min,
                (Z2MLightController.ATTRIBUTE_BRIGHTNESS,),
            ),
            Z2MLight.ON_MIN_COLOR_TEMP: (
                self.on_min,
                (Z2MLightController.ATTRIBUTE_COLOR_TEMP,),
            ),
            Z2MLight.SET_HALF_BRIGHTNESS: (
                self.set_value,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    0.5,
                ),
            ),
            Z2MLight.SET_HALF_COLOR_TEMP: (
                self.set_value,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    0.5,
                ),
            ),
            Z2MLight.CLICK: self.click,
            Z2MLight.CLICK_BRIGHTNESS_UP: (
                self.click,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.UP,
                ),
            ),
            Z2MLight.CLICK_COLOR_TEMP_UP: (
                self.click,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.UP,
                ),
            ),
            Z2MLight.CLICK_BRIGHTNESS_DOWN: (
                self.click,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.DOWN,
                ),
            ),
            Z2MLight.CLICK_COLOR_TEMP_DOWN: (
                self.click,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.DOWN,
                ),
            ),
            Z2MLight.HOLD: self.hold,
            Z2MLight.HOLD_BRIGHTNESS_UP: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.UP,
                ),
            ),
            Z2MLight.HOLD_COLOR_TEMP_UP: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.UP,
                ),
            ),
            Z2MLight.HOLD_BRIGHTNESS_DOWN: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.DOWN,
                ),
            ),
            Z2MLight.HOLD_BRIGHTNESS_TOGGLE: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_BRIGHTNESS,
                    StepperDir.TOGGLE,
                ),
            ),
            Z2MLight.HOLD_COLOR_TEMP_DOWN: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.DOWN,
                ),
            ),
            Z2MLight.HOLD_COLOR_TEMP_TOGGLE: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.TOGGLE,
                ),
            ),
            Z2MLight.XYCOLOR_FROM_CONTROLLER: self.xycolor_from_controller,
            Z2MLight.COLORTEMP_FROM_CONTROLLER: self.colortemp_from_controller,
            Z2MLight.BRIGHTNESS_FROM_CONTROLLER_LEVEL: self.brightness_from_controller_level,
            Z2MLight.BRIGHTNESS_FROM_CONTROLLER_ANGLE: self.brightness_from_controller_angle,
        }

    async def before_action(self, action: str, *args: Any, **kwargs: Any) -> bool:
        to_return = not (action == "hold" and self.hold_attribute is not None)
        return await super().before_action(action, *args, **kwargs) and to_return

    async def _ha_mqtt_call(self, topic: str, payload: str) -> None:
        await self.call_service("mqtt.publish", topic=topic, payload=payload)

    async def _mqtt_plugin_call(self, topic: str, payload: str) -> None:
        await self.call_service(
            "mqtt.publish", topic=topic, payload=payload, namespace="mqtt"
        )

    async def _mqtt_call(self, payload: dict[str, Any]) -> None:
        await self._mqtt_fn[self.entity.mode](
            f"{self.entity.topic_prefix}/{self.entity.name}/set", json.dumps(payload)
        )

    async def _on(self, **attributes: Any) -> None:
        await self._mqtt_call({"state": "ON", **attributes})

    @action
    async def on(self, attributes: Optional[dict[str, float]] = None) -> None:
        attributes = attributes or {}
        await self._on(**attributes)

    async def _off(self) -> None:
        await self._mqtt_call({"state": "OFF"})

    @action
    async def off(self) -> None:
        await self._off()

    async def _toggle(self, **attributes: Any) -> None:
        await self._mqtt_call({"state": "TOGGLE", **attributes})

    @action
    async def toggle(self, attributes: Optional[dict[str, float]] = None) -> None:
        attributes = attributes or {}
        await self._toggle(**attributes)

    async def _set_value(self, attribute: str, fraction: float) -> None:
        fraction = max(0, min(fraction, 1))
        min_ = self.MIN_MAX_ATTR[attribute].min
        max_ = self.MIN_MAX_ATTR[attribute].max
        value = (max_ - min_) * fraction + min_
        await self._on(**{attribute: value})

    @action
    async def set_value(self, attribute: str, fraction: float) -> None:
        await self._set_value(attribute, fraction)

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

    @lru_cache(maxsize=None)
    def get_stepper(self, attribute: str, steps: float, *, tag: str) -> InvertStepper:
        previous_direction = StepperDir.DOWN
        return InvertStepper(self.MIN_MAX_ATTR[attribute], steps, previous_direction)

    async def _change_light_state(
        self,
        *,
        attribute: str,
        direction: str,
        stepper: InvertStepper,
        transition: Optional[float],
        use_onoff: bool,
        mode: str,
    ) -> None:
        onoff_cmd = (
            "_onoff" if use_onoff and attribute == self.ATTRIBUTE_BRIGHTNESS else ""
        )
        stepper_output = stepper.step(stepper.steps, direction)
        kwargs = {}
        if transition is not None:
            kwargs["transition"] = transition
        await self._mqtt_call(
            {
                f"{attribute}_{mode}{onoff_cmd}": stepper_output.next_value,
                **kwargs,
            }
        )

    @action
    async def click(
        self,
        attribute: str,
        direction: str,
        steps: Optional[float] = None,
        transition: Optional[float] = None,
        use_onoff: Optional[bool] = None,
    ) -> None:
        attribute = self.get_option(attribute, self.ATTRIBUTES_LIST, "`click` action")
        direction = self.get_option(
            direction, [StepperDir.UP, StepperDir.DOWN], "`click` action"
        )
        steps = steps if steps is not None else self.click_steps
        stepper = self.get_stepper(attribute, steps, tag="click")
        await self._change_light_state(
            attribute=attribute,
            direction=direction,
            stepper=stepper,
            transition=transition if transition is not None else self.transition,
            use_onoff=use_onoff if use_onoff is not None else self.use_onoff,
            mode="step",
        )

    async def _hold(
        self,
        attribute: str,
        direction: str,
        steps: Optional[float] = None,
        use_onoff: Optional[bool] = None,
    ) -> None:
        attribute = self.get_option(attribute, self.ATTRIBUTES_LIST, "`hold` action")
        direction = self.get_option(
            direction,
            [StepperDir.UP, StepperDir.DOWN, StepperDir.TOGGLE],
            "`hold` action",
        )
        steps = steps if steps is not None else self.hold_steps
        stepper = self.get_stepper(attribute, steps, tag="hold")
        direction = stepper.get_direction(steps, direction)
        self.hold_attribute = attribute
        await self._change_light_state(
            attribute=attribute,
            direction=direction,
            stepper=stepper,
            transition=None,
            use_onoff=use_onoff if use_onoff is not None else self.use_onoff,
            mode="move",
        )

    @action
    async def hold(
        self,
        attribute: str,
        direction: str,
        steps: Optional[float] = None,
        use_onoff: Optional[bool] = None,
    ) -> None:
        await self._hold(attribute, direction, steps, use_onoff)

    @action
    async def release(self) -> None:
        if self.hold_attribute is None:
            return
        await self._mqtt_call({f"{self.hold_attribute}_move": "stop"})
        self.hold_attribute = None

    @action
    async def xycolor_from_controller(self, extra: Optional[EventData] = None) -> None:
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
            await self._on(color={"x": xy_color["x"], "y": xy_color["y"]})

    @action
    async def colortemp_from_controller(
        self, extra: Optional[EventData] = None
    ) -> None:
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
    async def brightness_from_controller_level(
        self, extra: Optional[EventData] = None
    ) -> None:
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

    @action
    async def brightness_from_controller_angle(
        self,
        steps: Optional[float] = None,
        use_onoff: Optional[bool] = None,
        extra: Optional[EventData] = None,
    ) -> None:
        if extra is None:
            self.log("No event data present", level="WARNING")
            return
        if isinstance(self.integration, Z2MIntegration):
            if "action_rotation_angle" not in extra:
                self.log(
                    "`action_rotation_angle` is not present in the MQTT payload",
                    level="WARNING",
                )
                return
            angle = extra["action_rotation_angle"]
            direction = StepperDir.UP if angle > 0 else StepperDir.DOWN
            await self._hold(
                self.ATTRIBUTE_BRIGHTNESS, direction, steps=steps, use_onoff=use_onoff
            )
