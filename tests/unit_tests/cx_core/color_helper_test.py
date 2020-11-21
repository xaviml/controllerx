import pytest
from cx_core.color_helper import Colors, get_color_wheel

from tests.test_utils import wrap_exetuction


@pytest.mark.parametrize(
    "colors, error_expected",
    [
        ("default_color_wheel", False),
        ("non_existing", True),
        ([(0.2, 0.3), (0.4, 0.5)], False),
        (0, True),
    ],
)
def test_get_color_wheel(colors: Colors, error_expected: bool):
    with wrap_exetuction(error_expected=error_expected, exception=ValueError):
        colors = get_color_wheel(colors)
