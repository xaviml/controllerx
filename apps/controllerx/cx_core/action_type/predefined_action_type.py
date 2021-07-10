import inspect
from typing import Any, Dict, Optional, Tuple

from cx_const import (
    ActionFunction,
    ActionFunctionWithParams,
    ActionParams,
    PredefinedActionsMapping,
    TypeAction,
)
from cx_core.action_type.base import ActionType
from cx_core.integration import EventData


def _get_action(action_value: TypeAction) -> ActionFunctionWithParams:
    if isinstance(action_value, tuple):
        return action_value
    else:
        return (action_value, tuple())


def _get_arguments(
    action: ActionFunction,
    args: ActionParams,
    predefined_action_kwargs: Dict[str, Any],
    extra: Optional[EventData],
) -> Tuple[ActionParams, Dict[str, Any]]:
    action_parameters = inspect.signature(action).parameters
    action_parameters_without_extra = {
        key: param for key, param in action_parameters.items() if key != "extra"
    }
    action_parameters_without_default = {
        key: param
        for key, param in action_parameters.items()
        if param.default is inspect.Signature.empty
    }
    action_args: Dict[str, Any] = dict(
        zip(action_parameters_without_extra.keys(), args)
    )  # ControllerX args
    action_positional_args = set(action_args.keys())
    action_args.update(predefined_action_kwargs)  # User args
    action_args.update({"extra": extra} if "extra" in action_parameters else {})
    action_args = {
        key: value for key, value in action_args.items() if key in action_parameters
    }

    if len(set(action_parameters_without_default).difference(action_args)) != 0:
        error_msg = [
            f"`{action.__name__}` action is missing some parameters. Parameters available:"
        ]
        for key, param in action_parameters_without_extra.items():
            if hasattr(param.annotation, "__name__"):
                attr_msg = f"   {key}: {param.annotation.__name__}"
            else:
                attr_msg = f"   {key}:"
            if param.default is not inspect.Signature.empty:
                attr_msg += f" [default: {param.default}]"
            if key in action_args:
                attr_msg += f" (value given: {action_args[key]})"
            elif param.default is inspect.Signature.empty:
                attr_msg += " (missing)"
            error_msg.append(attr_msg)
        raise ValueError("\n".join(error_msg))

    positional = tuple(
        value for key, value in action_args.items() if key in action_positional_args
    )
    action_args = {
        key: value
        for key, value in action_args.items()
        if key not in action_positional_args
    }
    return positional, action_args


class PredefinedActionType(ActionType):
    predefined_action_key: str
    predefined_action_kwargs: Dict[str, Any]
    predefined_actions_mapping: PredefinedActionsMapping

    def _raise_action_key_not_found(
        self, predefined_action_key: str, predefined_actions: PredefinedActionsMapping
    ) -> None:
        raise ValueError(
            f"`{predefined_action_key}` is not one of the predefined actions. "
            f"Available actions are: {list(predefined_actions.keys())}."
            "See more in: https://xaviml.github.io/controllerx/advanced/custom-controllers"
        )

    def initialize(self, **kwargs) -> None:
        self.predefined_action_key = kwargs.pop("action")
        self.predefined_action_kwargs = kwargs
        self.predefined_actions_mapping = (
            self.controller.get_predefined_actions_mapping()
        )
        if not self.predefined_actions_mapping:
            raise ValueError(
                f"Cannot use predefined actions for `{self.controller.__class__.__name__}` class."
            )
        if (
            not self.controller.contains_templating(self.predefined_action_key)
            and self.predefined_action_key not in self.predefined_actions_mapping
        ):
            self._raise_action_key_not_found(
                self.predefined_action_key, self.predefined_actions_mapping
            )

    async def run(self, extra: Optional[EventData] = None) -> None:
        action_key = await self.controller.render_value(self.predefined_action_key)
        if action_key not in self.predefined_actions_mapping:
            self._raise_action_key_not_found(
                action_key, self.predefined_actions_mapping
            )
        action, args = _get_action(self.predefined_actions_mapping[action_key])
        positional, action_args = _get_arguments(
            action, args, self.predefined_action_kwargs, extra
        )
        await action(*positional, **action_args)

    def __str__(self) -> str:
        return f"Predefined ({self.predefined_action_key})"
