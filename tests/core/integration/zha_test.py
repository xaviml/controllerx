import pytest

from tests.test_utils import hass_mock, fake_controller
from cx_core.integration.zha import ZHAIntegration


@pytest.mark.parametrize(
    "command, args, expected_called_with",
    [
        ("test_command", [0, 1, 2], "test_command_0_1_2"),
        ("testcommand", [0, 2], "testcommand_0_2"),
        ("testcommand", [], "testcommand"),
        ("testcommand", ["string"], "testcommand_string"),
        ("release", [1, 2, 3], "release"),
        ("stop", [1, 2, 3], "stop"),
        (
            "hold",
            {"press_type": "hold", "command_id": 0, "args": [3, 0, 0, 0]},
            "hold_3_0_0_0",
        ),
        (
            "button_double",
            {"press_type": "double", "command_id": 0, "args": [2, 0, 0, 0]},
            "button_double_2_0_0_0",
        ),
        (
            "button_single",
            {"press_type": "single", "command_id": 0, "args": [1, 0, 0, 0]},
            "button_single_1_0_0_0",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_integrations(
    fake_controller, mocker, command, args, expected_called_with,
):
    data = {"command": command, "args": args}
    handle_action_patch = mocker.patch.object(fake_controller, "handle_action")
    zha_integration = ZHAIntegration(fake_controller, {})
    await zha_integration.callback("test", data, None)

    handle_action_patch.assert_called_once_with(expected_called_with)
