import pytest

from tests.utils import hass_mock
from core import MediaPlayerController, ReleaseHoldController
from core.stepper import Stepper
from core.stepper.circular_stepper import CircularStepper
from core.stepper.minmax_stepper import MinMaxStepper


@pytest.fixture
def sut(hass_mock, mocker):
    c = MediaPlayerController()
    c.args = {}
    c.delay = 0
    c.media_player = "test"
    c.on_hold = False
    mocker.patch.object(ReleaseHoldController, "initialize")
    c.args["media_player"] = "media_player.test"
    c.initialize()
    return c


def test_initialize(sut):
    sut.initialize()
    assert sut.media_player == "media_player.test"


@pytest.mark.asyncio
async def test_play_pause(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.play_pause()
    called_service_patch.assert_called_once_with(
        "media_player/media_play_pause", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_previous_track(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.previous_track()
    called_service_patch.assert_called_once_with(
        "media_player/media_previous_track", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_next_track(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.next_track()
    called_service_patch.assert_called_once_with(
        "media_player/media_next_track", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_volume_up(sut, mocker, monkeypatch):
    async def fake_get_entity_state(entity, attribute=None):
        return 0.5

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.volume_up()
    called_service_patch.assert_called_once_with(
        "media_player/volume_set", entity_id=sut.media_player, volume_level=0.6
    )


@pytest.mark.asyncio
async def test_volume_down(sut, mocker, monkeypatch):
    async def fake_get_entity_state(entity, attribute=None):
        return 0.5

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.volume_down()
    called_service_patch.assert_called_once_with(
        "media_player/volume_set", entity_id=sut.media_player, volume_level=0.4
    )


@pytest.mark.asyncio
async def test_hold(sut, mocker):
    direction = "test_direction"
    mocker.patch.object(sut, "prepare_volume_change")
    super_hold_patch = mocker.patch.object(ReleaseHoldController, "hold")
    await sut.hold(direction)
    super_hold_patch.assert_called_once_with(direction)


@pytest.mark.parametrize(
    "direction_input, volume_level, expected_volume_level",
    [(Stepper.UP, 0, 0.1), (Stepper.DOWN, 0.5, 0.4),],
)
@pytest.mark.asyncio
async def test_hold_loop(
    sut, mocker, monkeypatch, direction_input, volume_level, expected_volume_level
):
    called_service_patch = mocker.patch.object(sut, "call_service")
    sut.volume_level = volume_level
    output = await sut.hold_loop(direction_input)
    called_service_patch.assert_called_once_with(
        "media_player/volume_set",
        entity_id=sut.media_player,
        volume_level=expected_volume_level,
    )
