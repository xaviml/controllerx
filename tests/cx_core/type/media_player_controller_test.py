import pytest

from cx_core import MediaPlayerController, ReleaseHoldController
from cx_core.feature_support.media_player import MediaPlayerSupport
from cx_core.stepper import Stepper
from tests.test_utils import fake_async_function


@pytest.fixture
@pytest.mark.asyncio
async def sut(monkeypatch, hass_mock, mocker):
    c = MediaPlayerController()
    c.args = {}
    c.delay = 0
    c.media_player = "test"
    c.on_hold = False
    mocker.patch.object(ReleaseHoldController, "initialize")
    c.args["media_player"] = "media_player.test"
    monkeypatch.setattr(c, "get_entity_state", fake_async_function("0"))
    await c.initialize()
    return c


@pytest.mark.asyncio
async def test_initialize(sut):
    await sut.initialize()
    assert sut.media_player == "media_player.test"


@pytest.mark.asyncio
async def test_play_pause(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.play_pause()
    called_service_patch.assert_called_once_with(
        "media_player/media_play_pause", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_play(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.play()
    called_service_patch.assert_called_once_with(
        "media_player/media_play", entity_id=sut.media_player
    )


@pytest.mark.asyncio
async def test_pause(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.pause()
    called_service_patch.assert_called_once_with(
        "media_player/media_pause", entity_id=sut.media_player
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
    sut.supported_features._supported_features = [MediaPlayerSupport.VOLUME_SET]

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
    sut.supported_features._supported_features = [MediaPlayerSupport.VOLUME_SET]

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
    "direction_input, volume_set_support, volume_level, expected_volume_level",
    [
        (Stepper.UP, True, 0, 0.1),
        (Stepper.DOWN, True, 0.5, 0.4),
        (Stepper.UP, False, None, None),
        (Stepper.DOWN, False, None, None),
    ],
)
@pytest.mark.asyncio
async def test_hold_loop(
    sut,
    mocker,
    monkeypatch,
    direction_input,
    volume_set_support,
    volume_level,
    expected_volume_level,
):
    called_service_patch = mocker.patch.object(sut, "call_service")
    sut.supported_features._supported_features = (
        [MediaPlayerSupport.VOLUME_SET] if volume_set_support else []
    )
    sut.volume_level = volume_level
    await sut.hold_loop(direction_input)
    if volume_set_support:
        called_service_patch.assert_called_once_with(
            "media_player/volume_set",
            entity_id=sut.media_player,
            volume_level=expected_volume_level,
        )
    else:
        called_service_patch.assert_called_once_with(
            f"media_player/volume_{direction_input}", entity_id=sut.media_player,
        )


@pytest.mark.parametrize(
    "direction_input, source_list, active_source, expected_calls, expected_source",
    [
        (Stepper.UP, ["radio1", "radio2", "radio3"], "radio1", 1, "radio2"),
        (Stepper.UP, ["radio1", "radio2", "radio3"], "radio3", 1, "radio1"),
        (Stepper.DOWN, ["radio1", "radio2", "radio3"], "radio1", 1, "radio3"),
        (Stepper.UP, ["radio1"], "radio1", 1, "radio1"),
        (Stepper.DOWN, ["radio1"], "radio1", 1, "radio1"),
        (Stepper.UP, ["radio1", "radio2", "radio3"], None, 1, "radio1"),
        (Stepper.DOWN, ["radio1", "radio2", "radio3"], None, 1, "radio1"),
        (Stepper.UP, [], None, 0, None),
        (Stepper.DOWN, [], None, 0, None),
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
    await sut.change_source_list(direction_input)

    # Checks
    assert called_service_patch.call_count == expected_calls
    if expected_calls > 0:
        called_service_patch.assert_called_once_with(
            "media_player/select_source",
            entity_id=sut.media_player,
            source=expected_source,
        )
