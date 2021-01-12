import pytest
from _pytest.monkeypatch import MonkeyPatch
from cx_core import ReleaseHoldController
from cx_core.controller import Controller
from pytest_mock import MockerFixture

from tests.test_utils import fake_fn


class FakeReleaseHoldController(ReleaseHoldController):
    def hold_loop(self):
        pass

    def default_delay(self) -> int:
        return 500


@pytest.fixture
def sut_before_init(mocker: MockerFixture) -> FakeReleaseHoldController:
    controller = FakeReleaseHoldController()  # type: ignore
    controller.args = {}
    mocker.patch.object(Controller, "init")
    mocker.patch.object(controller, "sleep")
    return controller


@pytest.fixture
@pytest.mark.asyncio
async def sut(sut_before_init: FakeReleaseHoldController) -> FakeReleaseHoldController:
    await sut_before_init.init()
    return sut_before_init


@pytest.mark.asyncio
async def test_init(sut_before_init: FakeReleaseHoldController, mocker: MockerFixture):
    await sut_before_init.init()
    assert sut_before_init.delay == 500


@pytest.mark.asyncio
async def test_release(sut: FakeReleaseHoldController):
    sut.on_hold = True
    await sut.release()
    assert not sut.on_hold


@pytest.mark.parametrize(
    "on_hold_input, hold_release_toogle, expected_calls",
    [(False, False, 1), (True, False, 0), (False, True, 1), (True, True, 0)],
)
@pytest.mark.asyncio
async def test_hold(
    sut: FakeReleaseHoldController,
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    on_hold_input: bool,
    hold_release_toogle: bool,
    expected_calls: int,
):
    sut.on_hold = on_hold_input
    sut.hold_release_toggle = hold_release_toogle
    monkeypatch.setattr(sut, "hold_loop", fake_fn(to_return=True, async_=True))
    hold_loop_patch = mocker.patch.object(sut, "hold_loop")

    await sut.hold()

    assert hold_loop_patch.call_count == expected_calls
