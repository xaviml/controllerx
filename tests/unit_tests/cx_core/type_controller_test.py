from typing import Any, Dict, List, Optional, Type, Union

import pytest
from cx_core.controller import Controller
from cx_core.type_controller import Entity, TypeController
from pytest import MonkeyPatch
from pytest_mock.plugin import MockerFixture

from tests.test_utils import fake_fn, wrap_execution

ENTITY_ARG = "my_entity"
ENTITY_NAME = "domain_1.test"
DEFAULT_ATTR_TEST = "my_default"


class MyEntity(Entity):
    attr_test: str

    def __init__(
        self,
        name: str,
        entities: Optional[List[str]] = None,
        attr_test: str = DEFAULT_ATTR_TEST,
    ) -> None:
        super().__init__(name, entities)
        self.attr_test = attr_test


class MyTypeController(TypeController[MyEntity]):
    domains = ["domain_1", "domain_2"]
    entity_arg = ENTITY_ARG

    def _get_entity_type(self) -> Type[MyEntity]:
        return MyEntity


@pytest.fixture
def sut_before_init(mocker: MockerFixture) -> MyTypeController:
    controller = MyTypeController(**{})
    controller.args = {ENTITY_ARG: ENTITY_NAME}
    mocker.patch.object(controller, "get_state", fake_fn(None, async_=True))
    mocker.patch.object(Controller, "init")
    return controller


@pytest.fixture
async def sut(sut_before_init: MyTypeController) -> MyTypeController:
    await sut_before_init.init()
    return sut_before_init


@pytest.mark.parametrize(
    "args, error_expected",
    [
        ({ENTITY_ARG: ENTITY_NAME}, False),
        ({ENTITY_ARG: {"name": ENTITY_NAME, "attr_test": "my_attr"}}, False),
        ({ENTITY_ARG: {"name": ENTITY_NAME}}, False),
        ({ENTITY_ARG: "non_existing_domain.my_entity"}, True),
        ({}, True),
    ],
)
async def test_init(
    sut_before_init: MyTypeController, args: Dict[str, Any], error_expected: bool
) -> None:
    sut_before_init.args = args

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await sut_before_init.init()

    if not error_expected:
        assert sut_before_init.entity.name == ENTITY_NAME
        if isinstance(args[ENTITY_ARG], dict):
            assert sut_before_init.entity.attr_test == args[ENTITY_ARG].get(
                "attr_test", DEFAULT_ATTR_TEST
            )


@pytest.mark.parametrize(
    "entity, domains, entities, error_expected",
    [
        ("light.kitchen", ["light"], None, False),
        ("light1.kitchen", ["light"], None, True),
        ("media_player.kitchen", ["light"], None, True),
        ("media_player.bedroom", ["media_player"], None, False),
        ("group.all_lights", ["light"], ["light.light1", "light.light2"], False),
        ("group.all_lights", ["light"], ["light1.light1", "light2.light2"], True),
        ("group.all", ["media_player"], ["media_player.test", "light.test"], True),
        (
            "group.all",
            ["switch", "input_boolean"],
            ["switch.switch1", "input_boolean.input_boolean1"],
            False,
        ),
        ("switch.switch1", ["switch", "input_boolean"], None, False),
        ("switch.switch1", ["binary_sensor", "input_boolean"], None, True),
        (
            "group.all",
            ["switch", "input_boolean"],
            ["light.light1", "input_boolean.input_boolean1"],
            True,
        ),
        (
            "{{ to_render }}",
            ["light"],
            None,
            False,
        ),
    ],
)
async def test_check_domain(
    sut: MyTypeController,
    monkeypatch: MonkeyPatch,
    entity: str,
    domains: List[str],
    entities: List[str],
    error_expected: bool,
) -> None:
    sut.domains = domains
    my_entity = MyEntity(entity, entities=entities)
    monkeypatch.setattr(sut, "get_state", fake_fn(to_return=entities, async_=True))

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        sut._check_domain(my_entity)


@pytest.mark.parametrize(
    "entity_input, entities, update_supported_features, expected_calls",
    [
        ("entity.test", None, False, 1),
        ("entity.test", "entity.test", True, 2),
        ("group.lights", ["entity.test"], False, 1),
        ("group.lights", ["entity.test"], True, 2),
        ("group.lights", [], True, None),
    ],
)
async def test_get_entity_state(
    sut: MyTypeController,
    mocker: MockerFixture,
    monkeypatch: MonkeyPatch,
    entity_input: str,
    entities: Union[str, List[str]],
    update_supported_features: bool,
    expected_calls: int,
) -> None:
    sut.update_supported_features = update_supported_features
    stub_get_state = mocker.stub()

    async def fake_get_state(
        entity: str, attribute: Optional[str] = None
    ) -> Union[str, List[str]]:
        stub_get_state(entity, attribute=attribute)
        return entities

    monkeypatch.setattr(sut, "get_state", fake_get_state)

    sut.entity = MyEntity(entity_input)
    with wrap_execution(error_expected=expected_calls is None, exception=ValueError):
        await sut.get_entity_state(attribute="attribute_test")

    if expected_calls is not None:
        if expected_calls == 1:
            stub_get_state.assert_called_once_with(
                entity_input, attribute="attribute_test"
            )
        elif expected_calls == 2:
            stub_get_state.call_count == 2
            stub_get_state.assert_any_call(entity_input, attribute="entity_id")
            stub_get_state.assert_any_call("entity.test", attribute="attribute_test")
