import pytest

from tests.utils import IntegrationMock, hass_mock
from core.controller import Controller
from core.integration.zha import ZHAIntegration


@pytest.fixture
def controller(hass_mock):
    c = Controller()
    c.args = {}
    return c


@pytest.mark.parametrize(
    "command, args, expected_called_with",
    [
        ("test_command", [0, 1, 2], "test_command_0_1_2"),
        ("testcommand", [0, 2], "testcommand_0_2"),
        ("testcommand", [], "testcommand"),
        ("testcommand", ["string"], "testcommand_string"),
        ("release", [1, 2, 3], "release"),
        ("stop", [1, 2, 3], "stop"),
    ],
)
@pytest.mark.asyncio
async def test_get_integrations(
    controller, mocker, command, args, expected_called_with
):
    data = {"command": command, "args": args}
    handle_action_patch = mocker.patch.object(controller, "handle_action")
    zha_integration = ZHAIntegration(controller)
    await zha_integration.callback("test", data, None)

    handle_action_patch.assert_called_once_with(expected_called_with)
