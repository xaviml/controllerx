import pytest

from core import integration as integration_module
from core.controller import Controller, ReleaseHoldController

from tests.utils import IntegrationMock, hass_mock


class FakeReleaseHoldController(ReleaseHoldController):
    def hold_loop(self):
        pass


@pytest.fixture
def sut(hass_mock):
    c = FakeReleaseHoldController()
    c.args = {}
    c.delay = 0
    return c


def test_initialize(sut, monkeypatch):
    monkeypatch.setattr(Controller, "initialize", lambda self: None)
    monkeypatch.setattr(sut, "default_delay", lambda: 500)
    monkeypatch.setattr(sut, "sleep", lambda time: None)
    # SUT
    sut.initialize()

    assert sut.delay == 500


@pytest.mark.asyncio
async def test_release(sut):
    sut.on_hold = True

    # SUT
    await sut.release()

    # Checks
    assert sut.on_hold == False


@pytest.mark.parametrize(
    "on_hold_input,expected_calls", [(False, 1), (True, 1),],
)
@pytest.mark.asyncio
async def test_hold(sut, monkeypatch, mocker, on_hold_input, expected_calls):
    sut.on_hold = on_hold_input

    async def fake_hold_loop():
        return True

    hold_loop_patch = mocker.patch.object(sut, "hold_loop")
    monkeypatch.setattr(sut, "hold_loop", fake_hold_loop)

    # SUT
    await sut.hold()

    # Checks
    hold_loop_patch.call_count == expected_calls
