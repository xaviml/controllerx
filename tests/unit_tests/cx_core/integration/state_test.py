from typing import Optional

import pytest
from appdaemon.plugins.hass.hassapi import Hass
from cx_core.controller import Controller
from cx_core.integration.state import StateIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize("attribute", ["sensor", "entity_id", None])
async def test_listen_changes(
    fake_controller: Controller, mocker: MockerFixture, attribute: Optional[str]
) -> None:
    kwargs = {}
    if attribute is not None:
        kwargs["attribute"] = attribute
    controller_id = "controller_id"
    state_event_mock = mocker.patch.object(Hass, "listen_state")
    state_integration = StateIntegration(fake_controller, kwargs)

    await state_integration.listen_changes(controller_id)

    state_event_mock.assert_called_once_with(
        fake_controller,
        state_integration.state_callback,
        controller_id,
        attribute=attribute,
    )


async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
) -> None:
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    state_integration = StateIntegration(fake_controller, {})

    await state_integration.state_callback("test", None, "old_state", "new_state", {})

    handle_action_patch.assert_called_once_with("new_state", previous_state="old_state")
