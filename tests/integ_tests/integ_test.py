import asyncio
import glob
import importlib
from pathlib import Path

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


def get_controller(module_name, class_name):
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_()


def get_fake_entity_states(entity_state, entity_state_attributes):
    async def inner(entity_id, attribute=None):
        if attribute is not None and attribute in entity_state_attributes:
            return entity_state_attributes[attribute]
        return entity_state

    return inner


integration_tests = get_integ_tests()


@pytest.mark.asyncio
@pytest.mark.parametrize("config_file, data", integration_tests)
async def test_example_config(hass_mock, mocker, config_file, data):
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
    tasks = []
    for idx, action in enumerate(fired_actions):
        if isinstance(action, str):
            if idx == len(fired_actions) - 1:
                await controller.handle_action(action)
            else:
                task = asyncio.ensure_future(controller.handle_action(action))
                tasks.append(task)
        elif isinstance(action, int):
            await asyncio.sleep(action / 1000)

    if tasks:  # Finish pending tasks if any
        await asyncio.wait(tasks)
    assert call_service_stub.call_count == expected_calls_count
    calls = [mocker.call(call["service"], **call["data"]) for call in expected_calls]
    call_service_stub.assert_has_calls(calls)
