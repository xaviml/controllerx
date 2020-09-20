import importlib
import os
import pkgutil


class IntegrationMock:
    def __init__(self, name, controller, mocker):
        self.name = name
        self.controller = controller
        self.get_actions_mapping = mocker.stub(name="get_actions_mapping")
        self.listen_changes = mocker.stub(name="listen_changes")
        super().__init__()


def fake_fn(async_=False, to_return=None):
    async def inner_fake_async_fn(*args, **kwargs):
        return to_return

    def inner_fake_fn(*args, **kwargs):
        return to_return

    return inner_fake_async_fn if async_ else inner_fake_fn


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


def get_instances(file_, package_, class_):
    _import_modules(
        file_, package_,
    )
    subclasses = _all_subclasses(class_)
    devices = [
        cls_()
        for cls_ in subclasses
        if len(cls_.__subclasses__()) == 0 and package_ in cls_.__module__
    ]
    return devices
