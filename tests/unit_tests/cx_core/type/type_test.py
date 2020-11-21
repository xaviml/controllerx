from typing import Type

from cx_const import TypeActionsMapping
from cx_core import type as type_module
from cx_core.type_controller import TypeController
import pytest
from pytest_mock.plugin import MockerFixture
from tests.test_utils import get_classes


def check_mapping(mapping: TypeActionsMapping) -> None:
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
    type_module.__file__, type_module.__package__, TypeController
)


@pytest.mark.parametrize("controller_type", controller_types)
def test_type_actions_mapping(
    mocker: MockerFixture, controller_type: Type[TypeController]
):
    controller = controller_type()  # type: ignore
    # mocker.patch.object(TypeController, "initialize")
    mappings = controller.get_type_actions_mapping()
    check_mapping(mappings)
