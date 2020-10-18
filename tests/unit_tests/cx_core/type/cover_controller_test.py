from cx_core.feature_support.cover import CoverSupport
import pytest

from cx_core.controller import TypeController
from cx_core import CoverController
from tests.test_utils import fake_fn


@pytest.fixture
@pytest.mark.asyncio
async def sut(hass_mock, mocker):
    c = CoverController()  # type: ignore
    mocker.patch.object(TypeController, "initialize")
    c.cover = "cover.test"
    c.open_position = 100
    c.close_position = 0
    return c


@pytest.mark.parametrize(
    "open_position, close_position, error_expected",
    [
        (100, 0, False),
        (50, 40, False),
        (50, 50, False),
        (40, 50, True),
        (0, 100, True),
    ],
)
@pytest.mark.asyncio
async def test_initialize(
    sut, monkeypatch, open_position, close_position, error_expected
):
    sut.args = {
        "cover": "cover.test2",
        "open_position": open_position,
        "close_position": close_position,
    }
    monkeypatch.setattr(sut, "get_entity_state", fake_fn(async_=True, to_return="0"))
    if error_expected:
        with pytest.raises(ValueError):
            await sut.initialize()
    else:
        await sut.initialize()
        assert sut.cover == "cover.test2"


@pytest.mark.parametrize(
    "supported_features, expected_service",
    [
        ({CoverSupport.OPEN}, "cover/open_cover"),
        ({CoverSupport.SET_COVER_POSITION}, "cover/set_cover_position"),
        (
            {CoverSupport.OPEN, CoverSupport.SET_COVER_POSITION},
            "cover/set_cover_position",
        ),
        ({CoverSupport.CLOSE}, None),
        ({}, None),
    ],
)
@pytest.mark.asyncio
async def test_open(sut, mocker, supported_features, expected_service):
    sut.supported_features = CoverSupport(sut.cover, sut, False)
    sut.supported_features._supported_features = set(supported_features)
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.open()
    if expected_service is not None:
        if expected_service == "cover/open_cover":
            expected_attributes = {"entity_id": "cover.test"}
        elif expected_service == "cover/set_cover_position":
            expected_attributes = {"entity_id": "cover.test", "position": 100}
        else:
            expected_attributes = {}
        called_service_patch.assert_called_once_with(
            expected_service, **expected_attributes
        )
    else:
        assert called_service_patch.call_count == 0


@pytest.mark.parametrize(
    "supported_features, expected_service",
    [
        ({CoverSupport.CLOSE}, "cover/close_cover"),
        ({CoverSupport.SET_COVER_POSITION}, "cover/set_cover_position"),
        (
            {CoverSupport.OPEN, CoverSupport.SET_COVER_POSITION},
            "cover/set_cover_position",
        ),
        ({CoverSupport.OPEN}, None),
        ({}, None),
    ],
)
@pytest.mark.asyncio
async def test_close(sut, mocker, supported_features, expected_service):
    sut.supported_features = CoverSupport(sut.cover, sut, False)
    sut.supported_features._supported_features = set(supported_features)
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.close()
    if expected_service is not None:
        if expected_service == "cover/close_cover":
            expected_attributes = {"entity_id": "cover.test"}
        elif expected_service == "cover/set_cover_position":
            expected_attributes = {"entity_id": "cover.test", "position": 0}
        else:
            expected_attributes = {}
        called_service_patch.assert_called_once_with(
            expected_service, **expected_attributes
        )
    else:
        assert called_service_patch.call_count == 0


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
    monkeypatch.setattr(
        sut, "get_entity_state", fake_fn(async_=True, to_return=cover_state)
    )
    await sut.toggle(open_patch)
    if stop_expected:
        called_service_patch.assert_called_once_with(
            "cover/stop_cover", entity_id=sut.cover
        )
    else:
        open_patch.assert_called_once()
