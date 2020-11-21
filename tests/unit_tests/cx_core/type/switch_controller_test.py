import pytest
from cx_core import SwitchController
from cx_core.type_controller import Entity
from pytest_mock.plugin import MockerFixture

ENTITY_NAME = "switch.test"


@pytest.fixture
@pytest.mark.asyncio
async def sut():
    c = SwitchController()  # type: ignore
    c.entity = Entity(ENTITY_NAME)
    return c


@pytest.mark.asyncio
async def test_turn_on(sut: SwitchController, mocker: MockerFixture):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.on()
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_on", entity_id=ENTITY_NAME
    )


@pytest.mark.asyncio
async def test_turn_off(sut: SwitchController, mocker: MockerFixture):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.off()
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_off", entity_id=ENTITY_NAME
    )


@pytest.mark.asyncio
async def test_toggle(sut: SwitchController, mocker: MockerFixture):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.toggle()
    called_service_patch.assert_called_once_with(
        "homeassistant/toggle", entity_id=ENTITY_NAME
    )
