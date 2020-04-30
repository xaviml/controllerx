import pytest

from core.controller import TypeController
from tests.test_utils import fake_async_function, hass_mock
from core import CoverController


@pytest.fixture
@pytest.mark.asyncio
async def sut(hass_mock, mocker):
    c = CoverController()
    mocker.patch.object(TypeController, "initialize")
    c.args = {"cover": "cover.test"}
    await c.initialize()
    return c


@pytest.mark.asyncio
async def test_initialize(sut):
    await sut.initialize()
    assert sut.cover == "cover.test"


@pytest.mark.asyncio
async def test_open(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.open()
    called_service_patch.assert_called_once_with(
        "cover/open_cover", entity_id=sut.cover
    )


@pytest.mark.asyncio
async def test_close(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.close()
    called_service_patch.assert_called_once_with(
        "cover/close_cover", entity_id=sut.cover
    )


@pytest.mark.asyncio
async def test_stop(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.stop()
    called_service_patch.assert_called_once_with(
        "cover/stop_cover", entity_id=sut.cover
    )


@pytest.mark.parametrize(
    "cover_state, stop_expected",
    [("opening", True), ("closing", True), ("open", False), ("close", False)],
)
@pytest.mark.asyncio
async def test_toggle(sut, monkeypatch, mocker, cover_state, stop_expected):
    called_service_patch = mocker.patch.object(sut, "call_service")
    open_patch = mocker.patch.object(sut, "open")
    monkeypatch.setattr(sut, "get_entity_state", fake_async_function(cover_state))
    await sut.toggle(open_patch)
    if stop_expected:
        called_service_patch.assert_called_once_with(
            "cover/stop_cover", entity_id=sut.cover
        )
    else:
        open_patch.assert_called_once()
