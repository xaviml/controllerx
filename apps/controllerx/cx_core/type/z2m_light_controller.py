import asyncio
import json
from typing import Any, Dict, List, Optional, Set, Type

from cx_const import PredefinedActionsMapping, StepperDir, Z2MLight
from cx_core.controller import action
from cx_core.stepper import MinMax, Stepper
from cx_core.type_controller import Entity, TypeController

DEFAULT_CLICK_STEPS = 70
DEFAULT_HOLD_STEPS = 70
DEFAULT_TRANSITION = 0.5

Mode = str
# Once the minimum supported version of Python is 3.8,
# we can declare the Mode as a Literal
# ColorMode = Literal["ha", "mqtt"]


class Z2MLightEntity(Entity):
    mode: Mode

    def __init__(
        self,
        name: str,
        entities: Optional[List[str]] = None,
        color_mode: Mode = "ha",
    ) -> None:
        super().__init__(name, entities)
        self.color_mode = color_mode


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

    _supported_color_modes: Optional[Set[str]]

    async def init(self) -> None:
        self.click_steps = self.args.get("click_steps", DEFAULT_CLICK_STEPS)
        self.hold_steps = self.args.get("hold_steps", DEFAULT_HOLD_STEPS)
        self.transition = self.args.get("transition", DEFAULT_TRANSITION)
        self.use_onoff = self.args.get("use_onoff", False)

        await super().init()

    def _get_entity_type(self) -> Type[Z2MLightEntity]:
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
            Z2MLight.HOLD_COLOR_TEMP_DOWN: (
                self.hold,
                (
                    Z2MLightController.ATTRIBUTE_COLOR_TEMP,
                    StepperDir.DOWN,
                ),
            ),
        }

    async def _mqtt_call(self, payload: Dict[str, Any]) -> None:
        await self.call_service(
            "mqtt.publish",
            topic=f"zigbee2mqtt/{self.entity.name}/set",
            payload=json.dumps(payload),
        )

    async def _on(self, **attributes: Any) -> None:
        await self._mqtt_call({"state": "ON", **attributes})

    @action
    async def on(self, attributes: Optional[Dict[str, float]] = None) -> None:
        attributes = attributes or {}
        await self._on(**attributes)

    async def _off(self) -> None:
        await self._mqtt_call({"state": "OFF"})

    @action
    async def off(self) -> None:
        await self._off()

    async def _toggle(self) -> None:
        await self._mqtt_call({"state": "TOGGLE"})

    @action
    async def toggle(self) -> None:
        await self._toggle()

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

    async def _change_light_state(
        self,
        *,
        attribute: str,
        direction: str,
        steps: float,
        transition: float,
        use_onoff: bool,
        mode: str,
    ) -> None:
        attribute = self.get_option(attribute, self.ATTRIBUTES_LIST, "`click` action")
        direction = self.get_option(
            direction, [StepperDir.UP, StepperDir.DOWN], "`click` action"
        )

        onoff_cmd = (
            "_onoff" if use_onoff and attribute == self.ATTRIBUTE_BRIGHTNESS else ""
        )
        await self._mqtt_call(
            {
                f"{attribute}_{mode}{onoff_cmd}": Stepper.apply_sign(steps, direction),
                "transition": transition,
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
        await self._change_light_state(
            attribute=attribute,
            direction=direction,
            steps=steps if steps is not None else self.click_steps,
            transition=transition if transition is not None else self.transition,
            use_onoff=use_onoff if use_onoff is not None else self.use_onoff,
            mode="step",
        )

    @action
    async def hold(
        self,
        attribute: str,
        direction: str,
        steps: Optional[float] = None,
        use_onoff: Optional[bool] = None,
    ) -> None:
        await self._change_light_state(
            attribute=attribute,
            direction=direction,
            steps=steps if steps is not None else self.click_steps,
            transition=self.transition,
            use_onoff=use_onoff if use_onoff is not None else self.use_onoff,
            mode="move",
        )

    @action
    async def release(self) -> None:
        await asyncio.gather(
            *[
                self._mqtt_call({f"{attribute}_move": "stop"})
                for attribute in self.ATTRIBUTES_LIST
            ]
        )
