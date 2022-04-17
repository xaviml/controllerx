import importlib
import os
import pkgutil
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

import pytest
from mock import MagicMock
from pytest import ExceptionInfo
from pytest_mock.plugin import MockerFixture
from typing_extensions import Literal

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


def _import_modules(file_dir: str, package: str) -> None:
    pkg_dir = os.path.dirname(file_dir)
    for (_, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        if ispkg:
            _import_modules(pkg_dir + "/" + name + "/__init__.py", package + "." + name)
        else:
            importlib.import_module("." + name, package)


def _all_subclasses(cls: Type[Any]) -> List[Type[Any]]:
    return list(
        set(type.__subclasses__(cls)).union(
            [s for c in type.__subclasses__(cls) for s in _all_subclasses(c)]
        )
    )


@overload
def get_classes(
    file_: str, package_: str, class_: Type[T], instantiate: Literal[False] = False
) -> List[Type[T]]:
    ...


@overload
def get_classes(
    file_: str, package_: str, class_: Type[T], instantiate: Literal[True]
) -> List[T]:
    ...


def get_classes(
    file_: str, package_: str, class_: Type[T], instantiate: bool = False
) -> Union[List[T], List[Type[T]]]:
    _import_modules(file_, package_)
    subclasses = _all_subclasses(class_)
    subclasses = [cls_ for cls_ in subclasses if f"{package_}." in cls_.__module__]
    return (
        [cls_() for cls_ in subclasses]
        if instantiate
        else [cls_ for cls_ in subclasses]
    )


@contextmanager
def wrap_execution(
    *, error_expected: bool, exception: Type[Exception] = Exception
) -> Generator[Optional[ExceptionInfo[Any]], None, None]:
    if error_expected:
        with pytest.raises(exception) as err_info:
            yield err_info
    else:
        yield None
