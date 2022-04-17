from typing import Any, Dict, Optional

import pytest
from cx_core import CoverController
from cx_core.controller import Controller
from cx_core.feature_support.cover import CoverSupport
from cx_core.type_controller import TypeController
from pytest import MonkeyPatch
from pytest_mock.plugin import MockerFixture

from tests.test_utils import fake_fn, wrap_execution

ENTITY_NAME = "cover.test"


@pytest.fixture
async def sut_before_init(mocker: MockerFixture) -> CoverController:
    controller = CoverController(**{})
    mocker.patch.object(controller, "get_state", fake_fn(None, async_=True))
    mocker.patch.object(TypeController, "init")
    return controller


@pytest.fixture
async def sut(mocker: MockerFixture) -> CoverController:
    controller = CoverController(**{})
    mocker.patch.object(controller, "get_state", fake_fn(None, async_=True))
    mocker.patch.object(Controller, "init")
    controller.args = {"cover": ENTITY_NAME}
    await controller.init()
    return controller


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
async def test_init(
    sut_before_init: CoverController,
    open_position: int,
    close_position: int,
    error_expected: bool,
) -> None:
    sut_before_init.args = {
        "open_position": open_position,
        "close_position": close_position,
    }

    with wrap_execution(error_expected=error_expected, exception=ValueError):
        await sut_before_init.init()

    if not error_expected:
        assert sut_before_init.open_position == open_position
        assert sut_before_init.close_position == close_position


@pytest.mark.parametrize(
    "supported_features, expected_service",
    [
        (CoverSupport.OPEN, "cover/open_cover"),
        (CoverSupport.SET_COVER_POSITION, "cover/set_cover_position"),
        (
            CoverSupport.OPEN | CoverSupport.SET_COVER_POSITION,
            "cover/set_cover_position",
        ),
        (CoverSupport.CLOSE, None),
        (0, None),
    ],
)
async def test_open(
    sut: CoverController,
    mocker: MockerFixture,
    supported_features: int,
    expected_service: Optional[str],
) -> None:
    sut.feature_support._supported_features = supported_features
    called_service_patch = mocker.patch.object(sut, "call_service")

    await sut.open()

    if expected_service is not None:
        expected_attributes: Dict[str, Any]
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
        (CoverSupport.CLOSE, "cover/close_cover"),
        (CoverSupport.SET_COVER_POSITION, "cover/set_cover_position"),
        (
            CoverSupport.OPEN | CoverSupport.SET_COVER_POSITION,
            "cover/set_cover_position",
        ),
        (CoverSupport.OPEN, None),
        (0, None),
    ],
)
async def test_close(
    sut: CoverController,
    mocker: MockerFixture,
    supported_features: int,
    expected_service: Optional[str],
) -> None:
    sut.feature_support._supported_features = supported_features
    called_service_patch = mocker.patch.object(sut, "call_service")

    await sut.close()

    if expected_service is not None:
        expected_attributes: Dict[str, Any]
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


async def test_stop(sut: CoverController, mocker: MockerFixture) -> None:
    called_service_patch = mocker.patch.object(sut, "call_service")

    await sut.stop()

    called_service_patch.assert_called_once_with(
        "cover/stop_cover", entity_id=ENTITY_NAME
    )


@pytest.mark.parametrize(
    "cover_state, stop_expected",
    [("opening", True), ("closing", True), ("open", False), ("close", False)],
)
async def test_toggle(
    sut: CoverController,
    monkeypatch: MonkeyPatch,
    mocker: MockerFixture,
    cover_state: str,
    stop_expected: bool,
) -> None:
    called_service_patch = mocker.patch.object(sut, "call_service")
    open_patch = mocker.patch.object(sut, "open")
    monkeypatch.setattr(
        sut, "get_entity_state", fake_fn(async_=True, to_return=cover_state)
    )

    await sut.toggle(open_patch)

    if stop_expected:
        called_service_patch.assert_called_once_with(
            "cover/stop_cover", entity_id=ENTITY_NAME
        )
        open_patch.assert_not_called()
    else:
        open_patch.assert_called_once()
