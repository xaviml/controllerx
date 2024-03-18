from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Union

import pytest
from appdaemon.adapi import ADAPI
from cx_const import ActionEvent
from cx_core import integration as integration_module
from cx_core.action_type import ActionsMapping
from cx_core.action_type.base import ActionType
from cx_core.controller import Controller, action
from pytest import MonkeyPatch
from pytest_mock.plugin import MockerFixture

from tests.test_utils import IntegrationMock, fake_fn, wrap_execution

INTEGRATION_TEST_NAME = "test"
CONTROLLER_NAME = "test_controller"


@pytest.fixture
def sut_before_init(fake_controller: Controller, mocker: MockerFixture) -> Controller:
    fake_controller.args = {
        "controller": CONTROLLER_NAME,
        "integration": INTEGRATION_TEST_NAME,
    }
    integration_mock = IntegrationMock("test", fake_controller, mocker)
    mocker.patch.object(
        fake_controller, "get_integration", return_value=integration_mock
    )
    return fake_controller


@pytest.fixture
async def sut(sut_before_init: Controller) -> Controller:
    await sut_before_init.initialize()
    return sut_before_init


async def test_action_decorator(sut: Controller, mocker: MockerFixture) -> None:
    stub_action = mocker.stub()
    before_action_spy = mocker.spy(sut, "before_action")

    @action
    async def fake_action(self: Controller) -> None:
        stub_action()

    # SUT
    await fake_action(sut)

    before_action_spy.assert_called_once_with("fake_action")
    stub_action.assert_called_once()


@pytest.mark.parametrize(
    "controller_input, actions_input, included_actions, excluded_actions, actions_output, error_expected",
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
async def test_initialize(
    sut_before_init: Controller,
    mocker: MockerFixture,
    controller_input: Union[str, List[str]],
    actions_input: List[str],
    included_actions: Optional[List[str]],
    excluded_actions: Optional[List[str]],
    actions_output: List[str],
    error_expected: bool,
) -> None:
    actions = {action: action for action in actions_input}
    predefined_actions = {action: lambda: None for action in actions_input}
    sut_before_init.args["controller"] = controller_input
    integration_mock = IntegrationMock(INTEGRATION_TEST_NAME, sut_before_init, mocker)
    mocker.patch.object(
        sut_before_init, "get_integration", return_value=integration_mock
    )
    if included_actions:
        sut_before_init.args["actions"] = included_actions
    if excluded_actions:
        sut_before_init.args["excluded_actions"] = excluded_actions
    mocker.patch.object(
        sut_before_init, "get_default_actions_mapping", return_value=actions
    )
    mocker.patch.object(
        sut_before_init,
        "get_predefined_actions_mapping",
        return_value=predefined_actions,
    )
    get_default_actions_mapping = mocker.spy(
        sut_before_init, "get_default_actions_mapping"
    )

    # SUT
    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await sut_before_init.initialize()

    # Checks
    if not error_expected:
        get_default_actions_mapping.assert_called_once()
        for controller_id in controller_input:
            integration_mock.listen_changes_stub.assert_any_call(controller_id)
        assert integration_mock.listen_changes_stub.call_count == len(controller_input)
        assert list(sut_before_init.actions_mapping.keys()) == actions_output


@pytest.mark.parametrize(
    "mapping, merge_mapping, actions_output, error_expected",
    [
        (["action1"], None, ["action1"], False),
        (["action1", "action2"], None, ["action1", "action2"], False),
        (None, ["action1"], ["action1", "action2", "action3"], False),
        (None, ["action1", "action2"], ["action1", "action2", "action3"], False),
        (None, None, ["action1", "action2", "action3"], False),
        (["action1"], ["action1"], None, True),
    ],
)
async def test_merge_mapping(
    sut_before_init: Controller,
    mocker: MockerFixture,
    mapping: List[str],
    merge_mapping: List[str],
    actions_output: List[str],
    error_expected: bool,
) -> None:
    actions_input = ["action1", "action2", "action3"]
    actions = {action: action for action in actions_input}
    predefined_actions = {action: lambda: None for action in actions_input}
    if mapping:
        sut_before_init.args["mapping"] = {item: item for item in mapping}
    if merge_mapping:
        sut_before_init.args["merge_mapping"] = {item: item for item in merge_mapping}

    mocker.patch.object(
        sut_before_init, "get_default_actions_mapping", return_value=actions
    )
    mocker.patch.object(
        sut_before_init,
        "get_predefined_actions_mapping",
        return_value=predefined_actions,
    )

    # SUT
    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await sut_before_init.initialize()

    # Checks
    if not error_expected:
        assert list(sut_before_init.actions_mapping.keys()) == actions_output


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("sensor1 ", ["sensor1 "]),
        ("sensor1, sensor2", ["sensor1, sensor2"]),
        ("sensor1,sensor2", ["sensor1,sensor2"]),
        ("sensor number 1, sensor number 2", ["sensor number 1, sensor number 2"]),
        (["sensor1", "sensor2"], ["sensor1", "sensor2"]),
        (["sensor 1", "sensor 2"], ["sensor 1", "sensor 2"]),
        (1002, [1002]),
        ([1002, 2002], [1002, 2002]),
    ],
)
def test_get_list(
    sut: Controller, test_input: Union[List[str], str], expected: List[str]
) -> None:
    output = sut.get_list(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "actions, custom, default, expected",
    [
        (
            {"action1", "action2", "action3"},
            None,
            0,
            {"action1": 0, "action2": 0, "action3": 0},
        ),
        (
            {"action1", "action2", "action3"},
            {"action1": 10},
            0,
            {"action1": 10, "action2": 0, "action3": 0},
        ),
        (
            {"action1", "action2", "action3"},
            10,
            0,
            {"action1": 10, "action2": 10, "action3": 10},
        ),
        (
            {"action1", "action2", "action3"},
            None,
            "restart",
            {"action1": "restart", "action2": "restart", "action3": "restart"},
        ),
        (
            {"action1", "action2", "action3"},
            "single",
            "restart",
            {"action1": "single", "action2": "single", "action3": "single"},
        ),
        (
            {"action1", "action2", "action3"},
            {"action2": "single", "action3": "another"},
            "restart",
            {"action1": "restart", "action2": "single", "action3": "another"},
        ),
    ],
)
def test_get_mapping_per_action(
    sut: Controller,
    actions: Set[ActionEvent],
    custom: Optional[Dict[ActionEvent, Any]],
    default: Any,
    expected: Dict[ActionEvent, Any],
) -> None:
    actions_mapping: ActionsMapping = {action: [] for action in actions}
    output = sut.get_mapping_per_action(actions_mapping, custom=custom, default=default)
    assert output == expected


@pytest.mark.parametrize(
    "mapping, expected",
    [
        (["toggle", "another"], []),
        (["toggle$1"], ["toggle"]),
        (["toggle", "toggle$1"], ["toggle"]),
        (["toggle", "toggle$2"], ["toggle"]),
        (["1001$1"], [1001]),
        ([1001], []),
        ([1001, "1001$1"], [1001]),
        ([1001, "1001$2"], [1001]),
        ([1001, "1001$2", 1002], [1001]),
        (["toggle", "toggle$1", "toggle$2"], ["toggle"]),
        (["toggle", "toggle$1", "toggle$2", "another$3"], ["toggle", "another"]),
    ],
)
def test_get_multiple_click_actions(
    fake_action_type: ActionType,
    sut: Controller,
    mapping: List[ActionEvent],
    expected: List[str],
) -> None:
    actions_mapping: ActionsMapping = {key: [fake_action_type] for key in mapping}
    output = sut.get_multiple_click_actions(actions_mapping)
    assert output == set(expected)


@pytest.mark.parametrize(
    "option, options, error_expected",
    [
        ("option1", ["option1", "option2", "option3"], False),
        ("option4", ["option1", "option2", "option3"], True),
    ],
)
def test_get_option(
    sut: Controller, option: str, options: List[str], error_expected: bool
) -> None:
    with wrap_execution(error_expected=error_expected, exception=ValueError):
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
    fake_controller: Controller,
    mocker: MockerFixture,
    integration_input: Union[str, Dict[str, Any]],
    integration_name_expected: str,
    args_expected: Dict[str, Any],
    error_expected: bool,
) -> None:
    get_integrations_spy = mocker.spy(integration_module, "get_integrations")

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        integration = fake_controller.get_integration(integration_input)

    if not error_expected:
        get_integrations_spy.assert_called_once_with(fake_controller, args_expected)
        assert integration.name == integration_name_expected


def test_get_default_actions_mapping_happyflow(
    sut: Controller, monkeypatch: MonkeyPatch, mocker: MockerFixture
) -> None:
    integration_mock = IntegrationMock("integration-test", sut, mocker)
    monkeypatch.setattr(
        integration_mock, "get_default_actions_mapping", lambda: {1001: "test"}
    )

    mapping = sut.get_default_actions_mapping(integration_mock)  # type:ignore[arg-type]

    assert mapping == {1001: "test"}


def test_get_default_actions_mapping_throwing_error(
    sut: Controller, mocker: MockerFixture
) -> None:
    integration_mock = IntegrationMock("integration-test", sut, mocker)
    mocker.patch.object(
        integration_mock, "get_default_actions_mapping", return_value=None
    )

    with pytest.raises(ValueError) as e:
        sut.get_default_actions_mapping(integration_mock)  # type: ignore[arg-type]

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
async def test_handle_action(
    sut: Controller,
    mocker: MockerFixture,
    actions_input: List[ActionEvent],
    action_called: str,
    action_called_times: int,
    action_delta: int,
    expected_calls: int,
    fake_action_type: ActionType,
) -> None:
    sut.action_delta = {action_called: action_delta}
    sut.action_times = defaultdict(int)

    sut.actions_mapping = {action: [fake_action_type] for action in actions_input}
    sut.previous_states = defaultdict(lambda: None)
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
        (1, "1234", True, True, False),
    ],
)
async def test_call_action(
    sut: Controller,
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    delay: int,
    handle: Optional[str],
    cancel_timer_called: bool,
    run_in_called: bool,
    action_timer_callback_called: bool,
) -> None:
    action_key = "test"
    sut.action_delay = {action_key: delay}
    action_delay_handles: Dict[ActionEvent, Optional[str]] = {action_key: handle}
    sut.action_delay_handles = action_delay_handles

    monkeypatch.setattr(sut, "cancel_timer", fake_fn(async_=True))
    monkeypatch.setattr(sut, "run_in", fake_fn(async_=True))
    monkeypatch.setattr(sut, "action_timer_callback", fake_fn(async_=True))
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
            sut.action_timer_callback, delay, action_key=action_key, extra=None
        )
    if action_timer_callback_called:
        action_timer_callback_patch.assert_called_once_with(
            {"action_key": action_key, "extra": None}
        )


@pytest.mark.parametrize(
    "service, attributes",
    [("test_service", {"attr1": 0.0, "attr2": "test"}), ("test_service", {})],
)
async def test_call_service(
    sut: Controller, mocker: MockerFixture, service: str, attributes: Dict[str, Any]
) -> None:
    call_service_stub = mocker.patch.object(ADAPI, "call_service")
    await sut.call_service(service, **attributes)
    call_service_stub.assert_called_once_with(sut, service, **attributes)


@pytest.mark.parametrize(
    "template, expected",
    [
        ("test", False),
        ("{{ to_render }}", True),
        ("{{ to_render }}_test", True),
        ("test_{{ to_render }}_test", True),
        (" {{ to_render }} ", True),
        ("{{ to_render", False),
        ("{ { to_render } }", False),
    ],
)
def test_render_value(sut: Controller, template: str, expected: bool) -> None:
    output = sut.contains_templating(template)
    assert output == expected
