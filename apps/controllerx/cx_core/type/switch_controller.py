from typing import Type

from cx_const import Switch, TypeActionsMapping
from cx_core.controller import action
from cx_core.feature_support import FeatureSupport
from cx_core.type_controller import Entity, TypeController


class SwitchController(TypeController[Entity, FeatureSupport]):
    """
    This is the main class that controls the switches for different devices.
    Type of actions:
        - On/Off/Toggle
    Parameters taken:
        - controller (required): Inherited from Controller
        - switch (required): Switch entity name
    """

    domains = [
        "alert",
        "automation",
        "cover",
        "input_boolean",
        "light",
        "media_player",
        "script",
        "switch",
    ]
    entity_arg = "switch"

    def get_type_actions_mapping(self) -> TypeActionsMapping:
        return {
            Switch.ON: self.on,
            Switch.OFF: self.off,
            Switch.TOGGLE: self.toggle,
        }

    def _get_entity_type(self) -> Type[Entity]:
        return Entity

    def _get_feature_support_type(self) -> Type[FeatureSupport]:
        return FeatureSupport

    @action
    async def on(self) -> None:
        await self.call_service("homeassistant/turn_on", entity_id=self.entity.name)

    @action
    async def off(self) -> None:
        await self.call_service("homeassistant/turn_off", entity_id=self.entity.name)

    @action
    async def toggle(self) -> None:
        await self.call_service("homeassistant/toggle", entity_id=self.entity.name)
