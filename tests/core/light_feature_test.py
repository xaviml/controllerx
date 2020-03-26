import pytest

from core import light_features


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        ("1", {light_features.SUPPORT_BRIGHTNESS,},),
        (
            "57",
            {
                light_features.SUPPORT_BRIGHTNESS,
                light_features.SUPPORT_FLASH,
                light_features.SUPPORT_COLOR,
                light_features.SUPPORT_TRANSITION,
            },
        ),
        (
            "149",
            {
                light_features.SUPPORT_BRIGHTNESS,
                light_features.SUPPORT_EFFECT,
                light_features.SUPPORT_COLOR,
                light_features.SUPPORT_WHITE_VALUE,
            },
        ),
        (0, set()),
        ("0", set()),
    ],
)
def test_decode(number, expected_supported_features):
    light_support = light_features.decode(number)
    assert set(light_support) == expected_supported_features
