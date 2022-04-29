from typing import Any

import pytest
from cx_core import ReleaseHoldController
from cx_core.controller import Controller
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from tests.test_utils import fake_fn


class FakeReleaseHoldController(ReleaseHoldController):
    async def hold_loop(self, *args: Any) -> bool:
        return False

    def default_delay(self) -> int:
        return 500


@pytest.fixture
def sut_before_init(mocker: MockerFixture) -> FakeReleaseHoldController:
    controller = FakeReleaseHoldController(**{})
    controller.args = {}
    mocker.patch.object(Controller, "init")
    mocker.patch.object(controller, "sleep")
    return controller


@pytest.fixture
async def sut(sut_before_init: FakeReleaseHoldController) -> FakeReleaseHoldController:
    await sut_before_init.init()
    return sut_before_init


async def test_init(
    sut_before_init: FakeReleaseHoldController, mocker: MockerFixture
) -> None:
    await sut_before_init.init()
    assert sut_before_init.delay == 500


async def test_release(sut: FakeReleaseHoldController) -> None:
    sut.on_hold = True
    await sut.release()
    assert not sut.on_hold


async def test_hold(
    sut: FakeReleaseHoldController,
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
) -> None:
    monkeypatch.setattr(sut, "hold_loop", fake_fn(to_return=True, async_=True))
    hold_loop_patch = mocker.patch.object(sut, "hold_loop")

    await sut.hold()

    hold_loop_patch.assert_called_once()


@pytest.mark.parametrize(
    "action, on_hold_input, hold_release_toogle, continue_call",
    [
        ("hold", False, False, True),
        ("hold", True, False, False),
        ("hold", False, True, True),
        ("hold", True, True, False),
        ("release", True, True, True),
        ("release", True, False, True),
        ("release", False, True, True),
        ("release", False, False, True),
    ],
)
async def test_before_action(
    sut: FakeReleaseHoldController,
    action: str,
    on_hold_input: bool,
    hold_release_toogle: bool,
    continue_call: bool,
) -> None:
    sut.on_hold = on_hold_input
    sut.hold_release_toggle = hold_release_toogle
    output = await sut.before_action(action)
    assert output == continue_call
