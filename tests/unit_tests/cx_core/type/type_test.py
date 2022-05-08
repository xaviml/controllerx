from typing import Optional, Type

import pytest
from cx_const import PredefinedActionsMapping
from cx_core import type as type_module
from cx_core.controller import Controller
from cx_core.type_controller import Entity, TypeController
from cx_helper import get_classes
from pytest_mock.plugin import MockerFixture


def check_mapping(mapping: Optional[PredefinedActionsMapping]) -> None:
    if mapping is None:
        return
    for v in mapping.values():
        if not (callable(v) or isinstance(v, tuple)):
            raise ValueError("The value mapping should be a callable or a tuple")
        if isinstance(v, tuple):
            if len(v) == 0:
                raise ValueError(
                    "The tuple should contain at least 1 element, the function"
                )
            fn, *_ = v
            if not callable(fn):
                raise ValueError("The first element of the tuple should be a callable")


controller_types = get_classes(
    type_module.__file__, type_module.__package__, Controller
)


@pytest.mark.parametrize("controller_type", controller_types)
def test_predefined_actions_mapping(
    mocker: MockerFixture, controller_type: Type[TypeController[Entity]]
) -> None:
    controller = controller_type(**{})
    mappings = controller.get_predefined_actions_mapping()
    check_mapping(mappings)
