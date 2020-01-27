import sys

sys.path.append("apps/controllerx")
import pytest
from controllerx import Controller
from collections import defaultdict
import time


@pytest.fixture
def controller(monkeypatch):
    monkeypatch.setattr(Controller, "__init__", lambda self: None)
    monkeypatch.setattr(Controller, "listen_event", lambda self, callback, entity: None)
    monkeypatch.setattr(Controller, "listen_state", lambda self, callback, entity: None)
    monkeypatch.setattr(Controller, "log", lambda self, message, level: None)
    c = Controller()
    c.args = {"action_delta": 300}
    c.action_times = defaultdict(lambda: 0)
    c.action_delta = 0
    return c


@pytest.mark.asyncio
async def test_initialize_sensor_and_event_throws_error(controller, monkeypatch):
    """
    When initialized and no sensor nor event attribute,
    it throws value error.
    """
    controller.args["sensor"] = "test"
    controller.args["event_id"] = "test"
    with pytest.raises(ValueError) as e:
        controller.initialize()
    assert str(e.value) == "'event_id' and 'sensor' cannot be used together"


@pytest.mark.asyncio
async def test_initialize_no_actions_mapping_throws_error(controller, monkeypatch):
    """
    When initialized and not action mapping, it should throw value error.
    """
    monkeypatch.setattr(Controller, "get_actions_mapping", lambda self: ("type", None))
    with pytest.raises(ValueError) as e:
        controller.initialize()
    assert str(e.value) == "This controller does not support type actions."


@pytest.mark.asyncio
async def test_initialize_include_actions_1(controller, monkeypatch):
    """
    When initialized and `actions` contains 2 out of 3 actions,
    only 2 actions will be registered.
    """
    actions_mapping = {
        "action1": "function1",
        "action2": "function2",
        "action3": "function3",
    }
    controller.args["sensor"] = "test"
    controller.args["actions"] = ["action1", "action3"]
    monkeypatch.setattr(
        Controller, "get_actions_mapping", lambda self: ("type", actions_mapping)
    )
    controller.initialize()
    assert list(controller.actions_mapping.keys()) == ["action1", "action3"]


@pytest.mark.asyncio
async def test_initialize_include_actions_2(controller, monkeypatch):
    """
    When initialized and no `actions` attribute,
    all actions will be registered.
    """
    actions_mapping = {
        "action1": "function1",
        "action2": "function2",
        "action3": "function3",
    }
    controller.args["sensor"] = "test"
    monkeypatch.setattr(
        Controller, "get_actions_mapping", lambda self: ("type", actions_mapping)
    )
    controller.initialize()
    assert list(controller.actions_mapping.keys()) == ["action1", "action2", "action3"]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("sensor1, sensor2", ["sensor1", "sensor2"]),
        ("sensor1,sensor2", ["sensor1", "sensor2"]),
        (["sensor1", "sensor2"], ["sensor1", "sensor2"]),
    ],
)
def test_get_list(controller, monkeypatch, test_input, expected):
    output = controller.get_list(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["event_id"], ("event", "events_mapping")),
        (["event_id", "sensor"], ("event", "events_mapping")),
        (["sensor"], ("state", "actions_mapping")),
        ([], (None, None)),
    ],
)
def test_get_actions_mapping(controller, monkeypatch, test_input, expected):
    monkeypatch.setattr(
        Controller, "get_event_actions_mapping", lambda self: "events_mapping"
    )
    monkeypatch.setattr(
        Controller, "get_state_actions_mapping", lambda self: "actions_mapping"
    )
    controller.args = {test: "test" for test in test_input}
    output = controller.get_actions_mapping()
    assert output == expected


@pytest.mark.parametrize(
    "test_input,expected", [("existing_action", 1000), ("non_existing_action", 0)],
)
@pytest.mark.asyncio
async def test_handle_action_called_with_existing_action(
    controller, monkeypatch, test_input, expected
):
    monkeypatch.setattr(time, "time", lambda: 1)
    action = "existing_action"
    controller.actions_mapping = {action: lambda: None}
    controller.action_times[action] = 1000

    # SUT
    await controller.handle_action(test_input)

    # Checks
    assert controller.action_times[test_input] == expected


@pytest.fixture
def controller_handle_action(controller, monkeypatch, mocker):
    monkeypatch.setattr(time, "time", lambda: 1)
    mocked_action = mocker.stub(name="fake_action")

    async def fake_action():
        mocked_action()

    action = "existing_action"
    controller.actions_mapping = {action: None}
    controller.get_action = lambda self: (fake_action,)
    return controller, mocked_action


@pytest.mark.asyncio
async def test_handle_action_action_called(controller_handle_action):
    controller, mocked_action = controller_handle_action
    # controller.action_times[action] = 1000

    # SUT
    await controller.handle_action("existing_action")

    # Checks
    mocked_action.assert_called()


@pytest.mark.asyncio
async def test_handle_action_action_called_once(controller_handle_action):
    controller, mocked_action = controller_handle_action

    # SUT
    await controller.handle_action("existing_action")
    controller.action_times["existing_action"] = 1000
    await controller.handle_action("existing_action")

    # Checks
    mocked_action.assert_called_once()


@pytest.mark.asyncio
async def test_handle_action_action_not_called(controller_handle_action):
    controller, mocked_action = controller_handle_action
    controller.action_times["existing_action"] = 1000

    # SUT
    await controller.handle_action("existing_action")

    # Checks
    mocked_action.assert_not_called()


def fake_action():
    pass


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (fake_action, (fake_action,)),
        ((fake_action,), (fake_action,)),
        ((fake_action, "test"), (fake_action, "test")),
    ],
)
def test_get_action(controller, monkeypatch, test_input, expected):
    output = controller.get_action(test_input)
    assert output == expected
