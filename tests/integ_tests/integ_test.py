import asyncio
import glob
from collections.abc import Awaitable, Callable, Iterator
from pathlib import Path
from typing import Any, Literal

import pytest
import yaml
from appdaemon.adapi import ADAPI
from cx_core.type_controller import TypeController
from pytest_mock.plugin import MockerFixture

from tests.test_utils import get_controller


def get_integ_tests() -> list[tuple[str, str, dict[str, Any]]]:
    configs = []
    test_yaml_files = glob.glob("**/*_test.yaml", recursive=True)
    for test_yaml_file in test_yaml_files:
        config_filepath = Path(test_yaml_file).parent / "config.yaml"
        with open(test_yaml_file) as f:
            data = yaml.full_load(f)
        configs.append((str(config_filepath), str(test_yaml_file), data))
    return configs


def read_config_yaml(file_name: str) -> dict[str, Any]:
    with open(file_name) as f:
        data = yaml.full_load(f)
    return list(data.values())[0]


def get_fake_get_state(
    entity_state: str | None, entity_state_attributes: dict[str, str]
) -> Callable[[str, str | None], Awaitable[Any | dict[str, Any] | None]]:
    async def inner(
        entity_id: str | None = None,
        attribute: str | Literal["all"] | None = None,
        default: Any | None = None,
        namespace: str | None = None,
        copy: bool = True,
        **kwargs: dict[str, Any],
    ) -> Any | dict[str, Any] | None:
        if attribute is not None and attribute in entity_state_attributes:
            return entity_state_attributes[attribute]
        return entity_state

    return inner


integration_tests = get_integ_tests()


class ExtraIterator:
    iterator: Iterator[dict[str, Any] | None]
    current: dict[str, Any] | None = None

    def __init__(self, iterator: Iterator[dict[str, Any] | None]) -> None:
        self.iterator = iterator

    def __next__(self) -> dict[str, Any] | None:
        try:
            self.current = next(self.iterator)
        except StopIteration:
            # Once iterator is finished, we will return always current
            # which is the last element from the iterator
            pass
        finally:
            return self.current


def _get_extra(
    data: dict[str, Any] | list[dict[str, Any]] | None,
) -> ExtraIterator:
    if data is None:
        return ExtraIterator(iter([None]))
    if isinstance(data, list):
        return ExtraIterator(iter(data))
    elif isinstance(data, dict):
        return ExtraIterator(iter([data]))


@pytest.mark.parametrize("config_file, test_yaml_file, data", integration_tests)
async def test_integ_configs(
    mocker: MockerFixture, config_file: str, test_yaml_file: str, data: dict[str, Any]
) -> None:
    entity_state_attributes = data.get("entity_state_attributes", {})
    entity_state: str | None = data.get("entity_state", None)
    previous_state = data.get("previous_state", None)
    fired_actions = data.get("fired_actions", [])
    render_template_response = data.get("render_template_response")
    extras: ExtraIterator = _get_extra(data.get("extra"))
    expected_calls = data.get("expected_calls", [])
    expected_calls_count = data.get("expected_calls_count", len(expected_calls))

    if "supported_features" not in entity_state_attributes:
        entity_state_attributes["supported_features"] = 0b1111111111
    if "entity_id" not in entity_state_attributes:
        entity_state_attributes["entity_id"] = "my_entity"
    config = read_config_yaml(config_file)
    controller = get_controller(config["module"], config["class"])
    if controller is None:
        raise ValueError(f"`{config['class']}` class controller does not exist")
    controller.args = config

    if render_template_response is not None:
        mocker.patch.object(
            controller, "_render_template", return_value=render_template_response
        )

    if isinstance(controller, TypeController):
        fake_get_state = get_fake_get_state(entity_state, entity_state_attributes)
        mocker.patch.object(controller, "get_state", fake_get_state)
    call_service_stub = mocker.patch.object(ADAPI, "call_service")

    await controller.initialize()
    for idx, action in enumerate(fired_actions):
        if any(isinstance(action, type_) for type_ in (str, int)):
            coroutine = controller.handle_action(
                action, previous_state=previous_state, extra=next(extras)
            )
            if idx == len(fired_actions) - 1:
                await coroutine
            else:
                asyncio.create_task(coroutine)
        elif isinstance(action, float):
            await asyncio.sleep(action)

    pending: set[asyncio.Task[Any]] = asyncio.all_tasks()
    # We exclude the current function we are executing
    pending = {
        task
        for task in pending
        if task._coro.__name__ != "test_integ_configs"  # type: ignore[attr-defined]
    }
    if pending:  # Finish pending tasks if any
        await asyncio.wait(pending)
    assert call_service_stub.call_count == expected_calls_count
    calls = [
        mocker.call(controller, call["service"], **call.get("data", {}))
        for call in expected_calls
    ]
    call_service_stub.assert_has_calls(calls)
