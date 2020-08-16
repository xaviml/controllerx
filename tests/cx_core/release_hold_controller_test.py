import pytest

from cx_core.controller import Controller, ReleaseHoldController
from tests.test_utils import fake_async_function


class FakeReleaseHoldController(ReleaseHoldController):
    def hold_loop(self):
        pass


@pytest.fixture
def sut(hass_mock):
    c = FakeReleaseHoldController()
    c.args = {}
    c.delay = 0
    c.hold_release_toggle = False
    return c


@pytest.mark.asyncio
async def test_initialize(sut, monkeypatch):
    monkeypatch.setattr(Controller, "initialize", fake_async_function())
    monkeypatch.setattr(sut, "default_delay", lambda: 500)
    monkeypatch.setattr(sut, "sleep", lambda time: None)
    # SUT
    await sut.initialize()

    assert sut.delay == 500


@pytest.mark.asyncio
async def test_release(sut):
    sut.on_hold = True

    # SUT
    await sut.release()

    # Checks
    assert not sut.on_hold


@pytest.mark.parametrize(
    "on_hold_input, hold_release_toogle, expected_calls",
    [(False, False, 1), (True, False, 0), (False, True, 1), (True, True, 0)],
)
@pytest.mark.asyncio
async def test_hold(
    sut, monkeypatch, mocker, on_hold_input, hold_release_toogle, expected_calls
):
    sut.on_hold = on_hold_input
    sut.hold_release_toggle = hold_release_toogle

    async def fake_hold_loop():
        return True

    monkeypatch.setattr(sut, "hold_loop", fake_hold_loop)
    hold_loop_patch = mocker.patch.object(sut, "hold_loop")

    # SUT
    await sut.hold()

    # Checks
    assert hold_loop_patch.call_count == expected_calls
