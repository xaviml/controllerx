import pytest

from cx_core.color_helper import get_color_wheel


@pytest.mark.parametrize(
    "colors, error_expected",
    [
        ("default_color_wheel", None),
        ("non_existing", ValueError),
        ([(0.2, 0.3), (0.4, 0.5)], None),
        (0, ValueError),
    ],
)
def test_get_color_wheel(colors, error_expected):

    # SUT
    if error_expected:
        with pytest.raises(error_expected):
            colors = get_color_wheel(colors)
    else:
        colors = get_color_wheel(colors)
