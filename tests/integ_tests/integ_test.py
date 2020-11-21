import asyncio
import glob
from pathlib import Path
from typing import Any, Dict

from pytest_mock.plugin import MockerFixture
from tests.test_utils import get_controller

import pytest
import yaml


def get_integ_tests():
    configs = []
    test_yaml_files = glob.glob("**/*_test.yaml", recursive=True)
    for yaml_file in test_yaml_files:
        config_filepath = Path(yaml_file).parent / "config.yaml"
        with open(yaml_file) as f:
            data = yaml.full_load(f)
        configs.append((str(config_filepath), data))
    return configs


def read_config_yaml(file_name):
    with open(file_name) as f:
        data = yaml.full_load(f)
    return list(data.values())[0]


def get_fake_entity_states(entity_state, entity_state_attributes):
    async def inner(entity_id, attribute=None):
        if attribute is not None and attribute in entity_state_attributes:
            return entity_state_attributes[attribute]
        return entity_state

    return inner


integration_tests = get_integ_tests()


@pytest.mark.asyncio
@pytest.mark.parametrize("config_file, data", integration_tests)
async def test_integ_configs(
    mocker: MockerFixture, config_file: str, data: Dict[str, Any]
):
    entity_state_attributes = data.get("entity_state_attributes", {})
    entity_state = data.get("entity_state", None)
    fired_actions = data.get("fired_actions", [])
    expected_calls = data.get("expected_calls", [])
    expected_calls_count = data.get("expected_calls_count", len(expected_calls))

    config = read_config_yaml(config_file)
    controller = get_controller(config["module"], config["class"])
    controller.args = config

    fake_entity_states = get_fake_entity_states(entity_state, entity_state_attributes)
    mocker.patch.object(controller, "get_entity_state", fake_entity_states)
    call_service_stub = mocker.patch.object(controller, "call_service")

    await controller.initialize()
    for idx, action in enumerate(fired_actions):
        if any(isinstance(action, type_) for type_ in (str, int)):
            if idx == len(fired_actions) - 1:
                await controller.handle_action(action)
            else:
                asyncio.ensure_future(controller.handle_action(action))
        elif isinstance(action, float):
            await asyncio.sleep(action)

    pending = asyncio.Task.all_tasks()
    # We exclude the current function we are executing
    pending = {
        task for task in pending if task._coro.__name__ != "test_integ_configs"  # type: ignore
    }
    if pending:  # Finish pending tasks if any
        await asyncio.wait(pending)
    assert call_service_stub.call_count == expected_calls_count
    calls = [
        mocker.call(call["service"], **call.get("data", {})) for call in expected_calls
    ]
    call_service_stub.assert_has_calls(calls)
