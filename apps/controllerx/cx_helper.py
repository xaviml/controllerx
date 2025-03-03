import importlib
import os
import pkgutil
from typing import Any


def _import_modules(file_dir: str, package: str) -> None:
    pkg_dir = os.path.dirname(file_dir)
    for _, name, ispkg in pkgutil.iter_modules([pkg_dir]):
        if ispkg:
            _import_modules(pkg_dir + "/" + name + "/__init__.py", package + "." + name)
        else:
            importlib.import_module("." + name, package)


def _all_subclasses(cls: type[Any]) -> list[type[Any]]:
    return list(
        set(type.__subclasses__(cls)).union(
            [s for c in type.__subclasses__(cls) for s in _all_subclasses(c)]
        )
    )


def get_classes(file_: str, package_: str, class_: type[Any]) -> list[type[Any]]:
    _import_modules(file_, package_)
    subclasses = _all_subclasses(class_)
    subclasses = [cls_ for cls_ in subclasses if f"{package_}." in cls_.__module__]
    return subclasses


def get_instances(file_: str, package_: str, class_: type[Any]) -> list[Any]:
    classes = get_classes(file_, package_, class_)
    return [cls_() for cls_ in classes]
