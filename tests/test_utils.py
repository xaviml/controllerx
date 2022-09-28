import importlib
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Callable, Generator, Optional, Type, TypeVar
from unittest.mock import MagicMock

import pytest
from pytest import ExceptionInfo
from pytest_mock.plugin import MockerFixture

if TYPE_CHECKING:
    from cx_core.controller import Controller

T = TypeVar("T")


class IntegrationMock:
    def __init__(self, name: str, controller: "Controller", mocker: MockerFixture):
        self.name = name
        self.controller = controller
        self.get_default_actions_mapping = MagicMock(
            name="get_default_actions_mapping", return_value={}
        )
        self.listen_changes_stub = mocker.stub(name="listen_changes")

    async def listen_changes(self, controller_id: str) -> None:
        self.listen_changes_stub(controller_id)


def fake_fn(
    to_return: Optional[Any] = None, async_: bool = False
) -> Callable[..., Any]:
    async def inner_fake_async_fn(*args: Any, **kwargs: Any) -> Optional[Any]:
        return to_return

    def inner_fake_fn(*args: Any, **kwargs: Any) -> Optional[Any]:
        return to_return

    return inner_fake_async_fn if async_ else inner_fake_fn


def get_controller(module_name: str, class_name: str) -> Optional["Controller"]:
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name, None)
    return class_() if class_ is not None else None


@contextmanager
def wrap_execution(
    *, error_expected: bool = True, exception: Type[Exception] = Exception
) -> Generator[Optional[ExceptionInfo[Any]], None, None]:
    if error_expected:
        with pytest.raises(exception) as err_info:
            yield err_info
    else:
        yield None
