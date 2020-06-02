from collections import defaultdict

import appdaemon.plugins.hass.hassapi as hass
import pytest

from core import integration as integration_module
from core.controller import action
from tests.test_utils import (
    IntegrationMock,
    fake_async_function,
    fake_controller,
    hass_mock,
)


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
    "controller_input, actions_input, included_actions, excluded_actions, actions_ouput, expect_an_error",
    [
        (
            ["controller_id"],
            ["action1", "action2"],
            ["action1"],
            None,
            ["action1"],
            False,
        ),
        (
            ["controller1", "controller2"],
            ["action1", "action2"],
            None,
            None,
            ["action1", "action2"],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2"],
            ["action1", "action2"],
            None,
            ["action1", "action2"],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["action1", "action2"],
            None,
            ["action1", "action2"],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["action1", "non_existing_action"],
            None,
            ["action1"],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["non_existing_action"],
            None,
            [],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            ["action1"],
            ["action2"],
            [],
            True,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            None,
            ["action2"],
            ["action1", "action3"],
            False,
        ),
        (
            ["controller"],
            ["action1", "action2", "action3"],
            None,
            ["action1", "action2", "action3"],
            [],
            False,
        ),
    ],
)
@pytest.mark.asyncio
async def test_initialize(
    sut,
    mocker,
    monkeypatch,
    controller_input,
    actions_input,
    included_actions,
    excluded_actions,
    actions_ouput,
    expect_an_error,
):
    actions = {action: action for action in actions_input}
    type_actions = {action: lambda: None for action in actions_input}
    sut.args["controller"] = controller_input
    sut.args["integration"] = "test"
    if included_actions:
        sut.args["actions"] = included_actions
    if excluded_actions:
        sut.args["excluded_actions"] = excluded_actions
    integration_mock = IntegrationMock("test", sut, mocker)
    monkeypatch.setattr(sut, "get_integration", lambda integration: integration_mock)
    monkeypatch.setattr(sut, "get_actions_mapping", lambda integration: actions)
    monkeypatch.setattr(sut, "get_type_actions_mapping", lambda: type_actions)
    check_ad_version = mocker.patch.object(sut, "check_ad_version")
    get_actions_mapping = mocker.spy(sut, "get_actions_mapping")

    # SUT
    if expect_an_error:
        with pytest.raises(ValueError) as e:
            await sut.initialize()
    else:
        await sut.initialize()

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
        (0.0, []),
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
    "integration_input, integration_name_expected, args_expected, error_expected",
    [
        ("z2m", "z2m", {}, False),
        ({"name": "zha"}, "zha", {}, False),
        (
            {"name": "deconz", "attr1": "value1", "attr2": "value2"},
            "deconz",
            {"attr1": "value1", "attr2": "value2"},
            False,
        ),
        ({"test": "no name"}, "z2m", {}, True),
        (0.0, None, {}, True),
    ],
)
def test_get_integration(
    sut,
    mocker,
    integration_input,
    integration_name_expected,
    args_expected,
    error_expected,
):
    get_integrations_spy = mocker.spy(integration_module, "get_integrations")

    # SUT
    if error_expected:
        with pytest.raises(ValueError) as e:
            integration = sut.get_integration(integration_input)
    else:
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
    sut.actions_mapping = {action: None for action in actions_input}
    call_action_patch = mocker.patch.object(sut, "call_action")

    # SUT
    for _ in range(action_called_times):
        await sut.handle_action(action_called)

    # Checks
    assert call_action_patch.call_count == expected_calls


@pytest.mark.parametrize(
    "delay,handle,cancel_timer_called,run_in_called,action_timer_callback_called",
    [
        (0, None, False, False, True),
        (1, None, False, True, False),
        (1, 1234, True, True, False),
    ],
)
@pytest.mark.asyncio
async def test_call_action(
    sut,
    monkeypatch,
    mocker,
    delay,
    handle,
    cancel_timer_called,
    run_in_called,
    action_timer_callback_called,
):
    action_key = "test"
    sut.actions_key_mapping = {"test": "test_action"}
    sut.action_delay = {action_key: delay}
    sut.action_delay_handles = {action_key: handle}

    monkeypatch.setattr(sut, "cancel_timer", fake_async_function())
    monkeypatch.setattr(sut, "run_in", fake_async_function())
    monkeypatch.setattr(sut, "action_timer_callback", fake_async_function())
    cancel_timer_patch = mocker.patch.object(sut, "cancel_timer")
    run_in_patch = mocker.patch.object(sut, "run_in")
    action_timer_callback_patch = mocker.patch.object(sut, "action_timer_callback")

    # SUT
    await sut.call_action(action_key)

    # Checks
    if cancel_timer_called:
        cancel_timer_patch.assert_called_once_with(handle)
    if run_in_called:
        run_in_patch.assert_called_once_with(
            sut.action_timer_callback, delay, action_key=action_key
        )
    if action_timer_callback_called:
        action_timer_callback_patch.assert_called_once_with({"action_key": action_key})


def fake_action():
    pass


@pytest.mark.parametrize(
    "test_input, expected, error_expected",
    [
        (fake_action, (fake_action,), False),
        ((fake_action,), (fake_action,), False),
        ((fake_action, "test"), (fake_action, "test"), False),
        ("not-list-or-function", (), True),
    ],
)
def test_get_action(sut, test_input, expected, error_expected):
    if error_expected:
        with pytest.raises(ValueError) as e:
            output = sut.get_action(test_input)
        assert (
            str(e.value)
            == "The action value from the action mapping should be a list or a function"
        )
    else:
        output = sut.get_action(test_input)
        assert output == expected


@pytest.mark.parametrize(
    "service, attributes",
    [("test_service", {"attr1": 0.0, "attr2": "test"}), ("test_service", {}),],
)
@pytest.mark.asyncio
async def test_call_service(sut, mocker, service, attributes):

    call_service_stub = mocker.patch.object(hass.Hass, "call_service")

    # SUT
    await sut.call_service(service, **attributes)

    # Checker
    call_service_stub.assert_called_once_with(sut, service, **attributes)
