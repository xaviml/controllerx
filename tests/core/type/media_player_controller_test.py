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


@pytest.mark.parametrize(
    "direction_input, source_list, active_source, expected_calls, expected_source",
    [
        (Stepper.UP, "radio1,radio2,radio3", "radio1", 1, "radio2"),
        (Stepper.UP, "radio1,radio2,radio3", "radio3", 1, "radio1"),
        (Stepper.DOWN, "radio1,radio2,radio3", "radio1", 1, "radio3"),
        (Stepper.UP, "radio1", "radio1", 1, "radio1"),
        (Stepper.DOWN, "radio1", "radio1", 1, "radio1"),
        (Stepper.UP, "radio1,radio2,radio3", None, 1, "radio1"),
        (Stepper.DOWN, "radio1,radio2,radio3", None, 1, "radio1"),
        (Stepper.UP, "", None, 0, None),
        (Stepper.DOWN, "", None, 0, None),
    ],
)
@pytest.mark.asyncio
async def test_change_source_list(
    sut,
    mocker,
    monkeypatch,
    direction_input,
    source_list,
    active_source,
    expected_calls,
    expected_source,
):
    called_service_patch = mocker.patch.object(sut, "call_service")

    async def fake_get_entity_state(entity, attribute=None):
        if active_source is None:
            return {"attributes": {"source_list": source_list}}
        else:
            return {"attributes": {"source_list": source_list, "source": active_source}}

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    # SUT
    output = await sut.change_source_list(direction_input)

    # Checks
    assert called_service_patch.call_count == expected_calls
    if expected_calls > 0:
        called_service_patch.assert_called_once_with(
            "media_player/select_source",
            entity_id=sut.media_player,
            source=expected_source,
        )
