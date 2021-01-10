import importlib
import os
import pkgutil
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, Generator, Optional

import pytest
from _pytest._code.code import ExceptionInfo
from mock import MagicMock
from pytest_mock.plugin import MockerFixture

if TYPE_CHECKING:
    from cx_core.controller import Controller


class IntegrationMock:
    def __init__(self, name: str, controller: "Controller", mocker: MockerFixture):
        self.name = name
        self.controller = controller
        self.get_default_actions_mapping = MagicMock(
            name="get_default_actions_mapping", return_value={}
        )
        self.listen_changes = mocker.stub(name="listen_changes")


def fake_fn(to_return=None, async_: bool = False) -> Callable:
    async def inner_fake_async_fn(*args, **kwargs):
        return to_return

    def inner_fake_fn(*args, **kwargs):
        return to_return

    return inner_fake_async_fn if async_ else inner_fake_fn


def get_controller(module_name, class_name) -> Optional["Controller"]:
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name, None)
    return class_() if class_ is not None else None


def _import_modules(file_dir, package):
    pkg_dir = os.path.dirname(file_dir)
    for (_, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        if ispkg:
            _import_modules(pkg_dir + "/" + name + "/__init__.py", package + "." + name)
        else:
            importlib.import_module("." + name, package)


def _all_subclasses(cls):
    return list(
        set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
        )
    )


def get_classes(file_, package_, class_, instantiate=False):
    _import_modules(file_, package_)
    subclasses = _all_subclasses(class_)
    subclasses = [
        cls_() if instantiate else cls_
        for cls_ in subclasses
        if f"{package_}." in cls_.__module__
    ]
    return subclasses


@contextmanager
def wrap_exetuction(
    *, error_expected: bool, exception=Exception
) -> Generator[Optional[ExceptionInfo], None, None]:
    if error_expected:
        with pytest.raises(exception) as err_info:
            yield err_info
    else:
        yield None
