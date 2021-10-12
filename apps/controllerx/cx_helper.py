import importlib
import os
import pkgutil


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
