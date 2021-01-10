from typing import TYPE_CHECKING, Dict, List, Type

from cx_const import ActionEvent, CustomAction, CustomActions
from cx_core.action_type.base import ActionType
from cx_core.action_type.call_service_action_type import CallServiceActionType
from cx_core.action_type.delay_action_type import DelayActionType
from cx_core.action_type.predefined_action_type import PredefinedActionType
from cx_core.action_type.scene_action_type import SceneActionType

if TYPE_CHECKING:
    from cx_core import Controller

ActionsMapping = Dict[ActionEvent, List[ActionType]]

action_type_mapping: Dict[str, Type[ActionType]] = {
    "action": PredefinedActionType,
    "service": CallServiceActionType,
    "scene": SceneActionType,
    "delay": DelayActionType,
}


def parse_actions(controller: "Controller", data: CustomActions) -> List[ActionType]:
    actions: CustomActions
    if isinstance(data, (list, tuple)):
        actions = list(data)
    else:
        actions = [data]

    return [_parse_action(controller, action) for action in actions]


def _parse_action(controller: "Controller", action: CustomAction) -> ActionType:
    if isinstance(action, str):
        return PredefinedActionType(controller, {"action": action})
    try:
        return next(
            action_type(controller, action)
            for key in action
            for action_type_key, action_type in action_type_mapping.items()
            if key == action_type_key
        )
    except StopIteration:
        raise ValueError(
            f"Not able to parse `{action}`. Available keys are: {list(action_type_mapping.keys())}"
        )
