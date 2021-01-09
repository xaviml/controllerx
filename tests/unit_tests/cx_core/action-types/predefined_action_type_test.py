import pytest
from cx_const import ActionFunctionWithParams, TypeAction
from cx_core.action_type.predefined_action_type import _get_action

from tests.test_utils import fake_fn


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (fake_fn, (fake_fn, tuple())),
        ((fake_fn, tuple()), (fake_fn, tuple())),
        ((fake_fn, ("test",)), (fake_fn, ("test",))),
    ],
)
def test_get_action(
    test_input: TypeAction,
    expected: ActionFunctionWithParams,
):
    output = _get_action(test_input)
    assert output == expected
