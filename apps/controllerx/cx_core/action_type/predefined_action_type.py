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

    def initialize(self, **kwargs) -> None:
        self.action_key = kwargs["action"]
        self.predefined_actions_mapping = (
            self.controller.get_predefined_actions_mapping()
        )
        if not self.predefined_actions_mapping:
            raise ValueError(
                f"Cannot use predefined actions for `{self.controller.__class__.__name__}` class."
            )
        if self.action_key not in self.predefined_actions_mapping:
            raise ValueError(
                f"`{self.action_key}` is not one of the predefined actions. "
                f"Available actions are: {list(self.predefined_actions_mapping.keys())}."
                "See more in: https://xaviml.github.io/controllerx/advanced/custom-controllers"
            )

    async def run(self, extra: Optional[EventData] = None) -> None:
        action, args = _get_action(self.predefined_actions_mapping[self.action_key])
        if "extra" in set(inspect.signature(action).parameters):
            await action(*args, extra=extra)
        else:
            await action(*args)

    def __str__(self) -> str:
        return f"Predefined ({self.action_key})"
