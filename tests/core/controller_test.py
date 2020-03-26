from collections import defaultdict

import appdaemon.plugins.hass.hassapi as hass
import pytest
from tests.utils import IntegrationMock, fake_controller, hass_mock

from core import integration as integration_module
from core.controller import Controller, action


@pytest.fixture
def sut(fake_controller):
    return fake_controller


@pytest.mark.asyncio
async def test_action_decorator(sut, mocker):
    stub_action = mocker.stub()
    before_action_spy = mocker.spy(sut, "before_action")

    @action
    async def fake_action(self):
        stub_action()

    # SUT
    await fake_action(sut)

    before_action_spy.assert_called_once_with("fake_action")
    stub_action.assert_called_once()


@pytest.mark.parametrize(
    "controller_input, actions_input, actions_filter, actions_ouput",
    [
        (["controller_id"], ["action1", "action2"], ["action1"], ["action1"]),
        (
            ["controller1", "controller2"],
            ["action1", "action2"],
            None,
            ["action1", "action2"],
        ),
        (
            ["controller"],
            ["action1", "action2"],
            ["action1", "action2"],
            ["action1", "action2"],
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["action1", "action2"],
            ["action1", "action2"],
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["action1", "non_existing_action"],
            ["action1"],
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["non_existing_action"],
            [],
        ),
    ],
)
def test_initialize(
    sut,
    mocker,
    monkeypatch,
    controller_input,
    actions_input,
    actions_filter,
    actions_ouput,
):
    actions = {action: action for action in actions_input}
    type_actions = {action: lambda: None for action in actions_input}
    sut.args["controller"] = controller_input
    sut.args["integration"] = "test"
    if actions_filter:
        sut.args["actions"] = actions_filter
    integration_mock = IntegrationMock("test", sut, mocker)
    monkeypatch.setattr(sut, "get_integration", lambda integration: integration_mock)
    monkeypatch.setattr(sut, "get_actions_mapping", lambda integration: actions)
    monkeypatch.setattr(sut, "get_type_actions_mapping", lambda: type_actions)
    check_ad_version = mocker.patch.object(sut, "check_ad_version")
    get_actions_mapping = mocker.spy(sut, "get_actions_mapping")

    # SUT
    sut.initialize()

    # Checks
    check_ad_version.assert_called_once()
    get_actions_mapping.assert_called_once()
    for controller_id in controller_input:
        integration_mock.listen_changes.assert_any_call(controller_id)
    assert integration_mock.listen_changes.call_count == len(controller_input)
    assert list(sut.actions_mapping.keys()) == actions_ouput


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("sensor1, sensor2", ["sensor1", "sensor2"]),
        ("sensor1,sensor2", ["sensor1", "sensor2"]),
        (["sensor1", "sensor2"], ["sensor1", "sensor2"]),
    ],
)
def test_get_list(sut, monkeypatch, test_input, expected):
    output = sut.get_list(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "option,options,expect_an_error",
    [
        ("option1", ["option1", "option2", "option3"], False),
        ("option4", ["option1", "option2", "option3"], True),
    ],
)
def test_get_option(sut, option, options, expect_an_error):
    if expect_an_error:
        with pytest.raises(ValueError) as e:
            sut.get_option(option, options)
    else:
        sut.get_option(option, options)


@pytest.mark.parametrize(
    "integration_input, integration_name_expected, args_expected",
    [
        ("z2m", "z2m", {}),
        ({"name": "zha"}, "zha", {}),
        (
            {"name": "deconz", "attr1": "value1", "attr2": "value2"},
            "deconz",
            {"attr1": "value1", "attr2": "value2"},
        ),
    ],
)
def test_get_integration(
    sut, mocker, integration_input, integration_name_expected, args_expected
):
    get_integrations_spy = mocker.spy(integration_module, "get_integrations")

    # SUT
    integration = sut.get_integration(integration_input)

    # Checks
    get_integrations_spy.assert_called_once_with(sut, args_expected)
    assert integration.name == integration_name_expected


def test_check_ad_version_throwing_error(sut, monkeypatch):
    monkeypatch.setattr(sut, "get_ad_version", lambda: "3.0.0")
    with pytest.raises(ValueError) as e:
        sut.check_ad_version()
    assert str(e.value) == "Please upgrade to AppDaemon 4.x"


def test_get_actions_mapping_happyflow(sut, monkeypatch, mocker):
    integration_mock = IntegrationMock("integration-test", sut, mocker)
    monkeypatch.setattr(
        integration_mock, "get_actions_mapping", lambda: "this_is_mapping"
    )

    mapping = sut.get_actions_mapping(integration_mock)

    assert mapping == "this_is_mapping"


def test_get_actions_mapping_throwing_error(sut, monkeypatch, mocker):
    integration_mock = IntegrationMock("integration-test", sut, mocker)
    monkeypatch.setattr(integration_mock, "get_actions_mapping", lambda: None)

    with pytest.raises(ValueError) as e:
        sut.get_actions_mapping(integration_mock)

    assert str(e.value) == "This controller does not support integration-test."


@pytest.mark.parametrize(
    "actions_input,action_called,action_called_times,action_delta,expected_calls",
    [
        (["action1", "action2"], "action1", 1, 300, 1),
        (["action1", "action2"], "action3", 1, 300, 0),
        (["action1", "action2"], "action2", 3, 300, 1),
        (["action1", "action2"], "action2", 3, 0, 3),
    ],
)
@pytest.mark.asyncio
async def test_handle_action(
    sut,
    mocker,
    actions_input,
    action_called,
    action_called_times,
    action_delta,
    expected_calls,
):
    sut.action_delta = action_delta
    sut.action_times = defaultdict(lambda: 0)
    actions = {}
    mocked_actions = {}
    for action in actions_input:
        mocked_action = mocker.stub(name=f"fake_action_{action}")

        async def fake_action():
            mocked_actions[action_called]()

        actions[action] = fake_action
        mocked_actions[action] = mocked_action
    if action_called not in mocked_actions:
        mocked_actions[action_called] = mocker.stub(name=f"fake_action_{action_called}")
    sut.actions_mapping = actions

    # SUT
    for _ in range(action_called_times):
        await sut.handle_action(action_called)
    assert mocked_actions[action_called].call_count == expected_calls


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
def test_get_action(sut, test_input, expected):
    output = sut.get_action(test_input)
    assert output == expected
