from typing import Any, Dict, Optional, Tuple

import pytest
from cx_const import ActionFunctionWithParams, ActionParams, TypeAction
from cx_core.action_type.predefined_action_type import _get_action, _get_arguments
from cx_core.integration import EventData

from tests.test_utils import fake_fn, wrap_execution


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
) -> None:
    output = _get_action(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "action_args, user_args, expected",
    [
        (
            ("test", 42),
            {},
            (("test", 42), {}),
        ),
        (
            ("test",),
            {},
            (("test",), {}),
        ),
        (
            ("test",),
            {"b": 42},
            (("test",), {"b": 42}),
        ),
        (
            ("test",),
            {"a": "test2"},
            (("test2",), {}),
        ),
        (
            ("test", 42),
            {"a": "test2", "b": 100},
            (("test2", 100), {}),
        ),
        (
            tuple(),
            {"a": "test2"},
            (tuple(), {"a": "test2"}),
        ),
        (
            tuple(),
            {"a": "test", "b": 42},
            (tuple(), {"a": "test", "b": 42}),
        ),
        (
            ("test",),
            {"c": 42},
            (("test",), {}),
        ),
        (
            ("test", 42, "fake"),
            {},
            (("test", 42), {}),
        ),
        (
            tuple(),
            {},
            None,
        ),
        (
            tuple(),
            {"b": 42},
            None,
        ),
    ],
)
def test_get_arguments_general(
    action_args: ActionParams,
    user_args: Dict[str, Any],
    expected: Optional[Tuple[ActionParams, Dict[str, Any]]],
) -> None:
    async def test_fn(a: str, b: int = 2) -> None:
        pass

    with wrap_execution(error_expected=expected is None, exception=ValueError):
        output = _get_arguments(test_fn, action_args, user_args, None)

    if expected is not None:
        assert expected == output


@pytest.mark.parametrize(
    "action_args, user_args, extra, expected",
    [
        (
            ("test", 42),
            {},
            {"test": "extra"},
            (("test", 42), {"extra": {"test": "extra"}}),
        ),
        (
            ("test", 42),
            {"extra": {"fake": "extra"}},
            {"test": "extra"},
            (("test", 42), {"extra": {"test": "extra"}}),
        ),  # User cannot override "extra"
        (
            ("test", 42, {"fake": "extra"}),
            {},
            {"test": "extra"},
            (("test", 42), {"extra": {"test": "extra"}}),
        ),  # args cannot override extra
    ],
)
def test_get_arguments_with_extra(
    action_args: ActionParams,
    user_args: Dict[str, Any],
    extra: Optional[EventData],
    expected: Optional[Tuple[ActionParams, Dict[str, Any]]],
) -> None:
    async def test_fn(a: str, b: int, extra: Optional[EventData] = None) -> None:
        pass

    with wrap_execution(error_expected=expected is None, exception=ValueError):
        output = _get_arguments(test_fn, action_args, user_args, extra)

    if expected is not None:
        assert expected == output
