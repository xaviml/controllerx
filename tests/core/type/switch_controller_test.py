import pytest

from cx_core import SwitchController
from cx_core.controller import TypeController


@pytest.fixture
@pytest.mark.asyncio
async def sut(hass_mock, mocker):
    c = SwitchController()
    mocker.patch.object(TypeController, "initialize")
    c.args = {"switch": "switch.test"}
    await c.initialize()
    return c


@pytest.mark.asyncio
async def test_initialize(sut):
    await sut.initialize()
    assert sut.switch == "switch.test"


@pytest.mark.asyncio
async def test_turn_on(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.on()
    called_service_patch.assert_called_once_with("switch/turn_on", entity_id=sut.switch)


@pytest.mark.asyncio
async def test_turn_off(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.off()
    called_service_patch.assert_called_once_with(
        "switch/turn_off", entity_id=sut.switch
    )


@pytest.mark.asyncio
async def test_toggle(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.toggle()
    called_service_patch.assert_called_once_with("switch/toggle", entity_id=sut.switch)
