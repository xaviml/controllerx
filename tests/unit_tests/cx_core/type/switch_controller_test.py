import pytest
from cx_core import SwitchController
from cx_core.type_controller import Entity
from pytest_mock.plugin import MockerFixture

from tests.test_utils import fake_fn

ENTITY_NAME = "switch.test"


@pytest.fixture
async def sut(mocker: MockerFixture) -> SwitchController:
    c = SwitchController(**{})
    mocker.patch.object(c, "get_state", fake_fn(None, async_=True))
    c.entity = Entity(name=ENTITY_NAME)
    return c


async def test_turn_on(sut: SwitchController, mocker: MockerFixture) -> None:
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.on()
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_on", entity_id=ENTITY_NAME
    )


async def test_turn_off(sut: SwitchController, mocker: MockerFixture) -> None:
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.off()
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_off", entity_id=ENTITY_NAME
    )


async def test_toggle(sut: SwitchController, mocker: MockerFixture) -> None:
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.toggle()
    called_service_patch.assert_called_once_with(
        "homeassistant/toggle", entity_id=ENTITY_NAME
    )
