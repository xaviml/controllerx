from tests.test_utils import fake_fn, wrap_exetuction
from typing import Any, Dict, List, Type

import pytest
from cx_core.controller import Controller
from cx_core.feature_support import FeatureSupport
from cx_core.type_controller import Entity, TypeController
from pytest_mock.plugin import MockerFixture
from _pytest.monkeypatch import MonkeyPatch

ENTITY_ARG = "my_entity"
ENTITY_NAME = "domain_1.test"
DEFAULT_ATTR_TEST = "my_default"


class MyEntity(Entity):
    attr_test: str

    def __init__(self, name: str, attr_test: str = DEFAULT_ATTR_TEST) -> None:
        super().__init__(name)
        self.attr_test = attr_test


class MyFeatureSupport(FeatureSupport):
    features = [1, 2, 3, 4]


class MyTypeController(TypeController[MyEntity, MyFeatureSupport]):

    domains = ["domain_1", "domain_2"]
    entity_arg = ENTITY_ARG

    def _get_entity_type(self) -> Type[MyEntity]:
        return MyEntity

    def _get_feature_support_type(self) -> Type[MyFeatureSupport]:
        return MyFeatureSupport


@pytest.fixture
def sut_before_init(mocker: MockerFixture) -> MyTypeController:
    controller = MyTypeController()  # type: ignore
    controller.args = {ENTITY_ARG: ENTITY_NAME}
    mocker.patch.object(Controller, "initialize")
    return controller


@pytest.fixture
@pytest.mark.asyncio
async def sut(sut_before_init: MyTypeController) -> MyTypeController:
    await sut_before_init.initialize()
    return sut_before_init


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "args, error_expected",
    [
        ({ENTITY_ARG: ENTITY_NAME}, False),
        ({ENTITY_ARG: {"name": ENTITY_NAME, "attr_test": "my_attr"}}, False),
        ({ENTITY_ARG: {"name": ENTITY_NAME}}, False),
        ({ENTITY_ARG: "non_existing_domain.my_entity"}, True),
    ],
)
async def test_initialize(
    sut_before_init: MyTypeController, args: Dict[str, Any], error_expected: bool
):
    sut_before_init.args = args

    with wrap_exetuction(error_expected=error_expected, exception=ValueError):
        await sut_before_init.initialize()

    if not error_expected:
        assert sut_before_init.entity.name == ENTITY_NAME
        if isinstance(args[ENTITY_ARG], dict):
            assert sut_before_init.entity.attr_test == args[ENTITY_ARG].get(
                "attr_test", DEFAULT_ATTR_TEST
            )


@pytest.mark.parametrize(
    "entity, domains, entities, error_expected",
    [
        ("light.kitchen", ["light"], [], False),
        ("light1.kitchen", ["light"], [], True),
        ("media_player.kitchen", ["light"], [], True),
        ("media_player.bedroom", ["media_player"], [], False),
        ("group.all_lights", ["light"], ["light.light1", "light.light2"], False),
        ("group.all_lights", ["light"], ["light1.light1", "light2.light2"], True),
        ("group.all", ["media_player"], ["media_player.test", "light.test"], True),
        (
            "group.all",
            ["switch", "input_boolean"],
            ["switch.switch1", "input_boolean.input_boolean1"],
            False,
        ),
        ("switch.switch1", ["switch", "input_boolean"], [], False),
        ("switch.switch1", ["binary_sensor", "input_boolean"], [], True),
        (
            "group.all",
            ["switch", "input_boolean"],
            ["light.light1", "input_boolean.input_boolean1"],
            True,
        ),
    ],
)
@pytest.mark.asyncio
async def test_check_domain(
    sut: MyTypeController,
    monkeypatch: MonkeyPatch,
    entity: str,
    domains: List[str],
    entities: List[str],
    error_expected: bool,
):
    sut.domains = domains
    expected_error_message = ""
    if error_expected:
        if entities == []:
            expected_error_message = (
                f"'{entity}' must be from one of the following domains "
                f"{domains} (e.g. {domains[0]}.bedroom)"
            )

        else:
            expected_error_message = (
                f"All entities from '{entity}' must be from one of the "
                f"following domains {domains} (e.g. {domains[0]}.bedroom)"
            )

    monkeypatch.setattr(sut, "get_state", fake_fn(to_return=entities, async_=True))

    with wrap_exetuction(
        error_expected=error_expected, exception=ValueError
    ) as err_info:
        await sut.check_domain(entity)

    if err_info is not None:
        assert str(err_info.value) == expected_error_message


@pytest.mark.parametrize(
    "entity_input, entities, expected_calls",
    [
        ("light.kitchen", ["entity.test"], 1),
        ("group.lights", ["entity.test"], 2),
        ("group.lights", [], None),
    ],
)
@pytest.mark.asyncio
async def test_get_entity_state(
    sut: MyTypeController,
    mocker: MockerFixture,
    monkeypatch: MonkeyPatch,
    entity_input: str,
    entities: List[str],
    expected_calls: int,
):
    stub_get_state = mocker.stub()

    async def fake_get_state(entity, attribute=None):
        stub_get_state(entity, attribute=attribute)
        return entities

    monkeypatch.setattr(sut, "get_state", fake_get_state)

    with wrap_exetuction(error_expected=expected_calls is None, exception=ValueError):
        await sut.get_entity_state(entity_input, "attribute_test")

    if expected_calls is not None:
        if expected_calls == 1:
            stub_get_state.assert_called_once_with(
                entity_input, attribute="attribute_test"
            )
        elif expected_calls == 2:
            stub_get_state.call_count == 2
            stub_get_state.assert_any_call(entity_input, attribute="entity_id")
            stub_get_state.assert_any_call("entity.test", attribute="attribute_test")
