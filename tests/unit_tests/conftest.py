from typing import Optional

import pytest
from cx_core import Controller, LightController
from cx_core.action_type.base import ActionType
from cx_core.integration import EventData


@pytest.fixture
def fake_controller() -> Controller:
    c = Controller(**{})
    c.args = {}
    return c


@pytest.fixture
def fake_type_controller() -> LightController:
    c = LightController(**{})
    c.args = {}
    return c


class FakeActionType(ActionType):
    async def run(self, extra: Optional[EventData] = None) -> None:
        return None


@pytest.fixture
def fake_action_type(fake_controller: Controller) -> ActionType:
    return FakeActionType(fake_controller, {})
