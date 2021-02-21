from typing import Dict

import pytest
from cx_core.controller import Controller
from cx_core.integration.lutron_caseta import LutronIntegration
from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "serial": 28786608,
                "type": "FourGroupRemote",
                "button_number": 4,
                "device_name": "Shade Remote",
                "area_name": "Upstairs Hall",
                "action": "press",
            },
            "button_4_press",
        ),
        (
            {
                "serial": 28786608,
                "type": "FourGroupRemote",
                "button_number": 0,
                "device_name": "Shade Remote",
                "area_name": "Upstairs Hall",
                "action": "hold",
            },
            "button_0_hold",
        ),
    ],
)
@pytest.mark.asyncio
async def test_callback(
    fake_controller: Controller,
    mocker: MockerFixture,
    data: Dict,
    expected: str,
):
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    lutron_integration = LutronIntegration(fake_controller, {})
    await lutron_integration.callback("test", data, {})
    handle_action_patch.assert_called_once_with(expected, extra=data)
