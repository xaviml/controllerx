import pytest

from core import MediaPlayerController, ReleaseHoldController
from tests.utils import hass_mock
from core.stepper import Stepper
from core.stepper.minmax_stepper import MinMaxStepper
from core.stepper.circular_stepper import CircularStepper


@pytest.fixture
def sut(hass_mock):
    c = MediaPlayerController()
    c.args = {}
    c.delay = 0
    c.media_player = "test"
    c.on_hold = False
    return c


def test_initialize(sut, mocker):
    mocker.patch.object(ReleaseHoldController, "initialize")
    sut.args["media_player"] = "media_player.test"
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
async def test_volume_up(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.volume_up()
    called_service_patch.assert_called_once_with(
        "media_player/volume_up", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_volume_down(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.volume_down()
    called_service_patch.assert_called_once_with(
        "media_player/volume_down", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_hold(sut, mocker):
    direction = "test_direction"
    super_hold_patch = mocker.patch.object(ReleaseHoldController, "hold")
    await sut.hold(direction)
    super_hold_patch.assert_called_once_with(direction)
    assert sut.hold_loop_times == 0


@pytest.mark.parametrize(
    "direction_input, hold_loop_times, expected_called_with, expected_output",
    [
        (Stepper.UP, 0, "media_player/volume_up", False),
        (Stepper.DOWN, 0, "media_player/volume_down", False),
        (Stepper.DOWN, 10, "media_player/volume_down", True),
    ],
)
@pytest.mark.asyncio
async def test_hold_loop(
    sut, mocker, direction_input, hold_loop_times, expected_called_with, expected_output
):
    called_service_patch = mocker.patch.object(sut, "call_service")
    sut.hold_loop_times = hold_loop_times
    output = await sut.hold_loop(direction_input)
    called_service_patch.assert_called_once_with(
        expected_called_with, entity_id=sut.media_player
    )
    assert sut.hold_loop_times == hold_loop_times + 1
    assert output == expected_output
