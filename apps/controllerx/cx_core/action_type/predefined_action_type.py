import inspect
from typing import Optional

from cx_const import ActionFunctionWithParams, PredefinedActionsMapping, TypeAction
from cx_core.action_type.base import ActionType
from cx_core.integration import EventData


def _get_action(action_value: TypeAction) -> ActionFunctionWithParams:
    if isinstance(action_value, tuple):
        return action_value
    else:
        return (action_value, tuple())


class PredefinedActionType(ActionType):
    action_key: str
    predefined_actions_mapping: PredefinedActionsMapping

    def _raise_action_key_not_found(
        self, action_key: str, predefined_actions: PredefinedActionsMapping
    ) -> None:
        raise ValueError(
            f"`{action_key}` is not one of the predefined actions. "
            f"Available actions are: {list(predefined_actions.keys())}."
            "See more in: https://xaviml.github.io/controllerx/advanced/custom-controllers"
        )

    def initialize(self, **kwargs) -> None:
        self.action_key = kwargs["action"]
        self.predefined_actions_mapping = (
            self.controller.get_predefined_actions_mapping()
        )
        if not self.predefined_actions_mapping:
            raise ValueError(
                f"Cannot use predefined actions for `{self.controller.__class__.__name__}` class."
            )
        if (
            not self.controller.contains_templating(self.action_key)
            and self.action_key not in self.predefined_actions_mapping
        ):
            self._raise_action_key_not_found(
                self.action_key, self.predefined_actions_mapping
            )

    async def run(self, extra: Optional[EventData] = None) -> None:
        action_key = await self.controller.render_value(self.action_key)
        if action_key not in self.predefined_actions_mapping:
            self._raise_action_key_not_found(
                action_key, self.predefined_actions_mapping
            )
        action, args = _get_action(self.predefined_actions_mapping[action_key])
        if "extra" in set(inspect.signature(action).parameters):
            await action(*args, extra=extra)
        else:
            await action(*args)

    def __str__(self) -> str:
        return f"Predefined ({self.action_key})"
