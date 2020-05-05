from core.feature_support.light import LightSupport
import pytest


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        ("1", {LightSupport.BRIGHTNESS,},),
        (
            "57",
            {
                LightSupport.BRIGHTNESS,
                LightSupport.FLASH,
                LightSupport.COLOR,
                LightSupport.TRANSITION,
            },
        ),
        (
            "149",
            {
                LightSupport.BRIGHTNESS,
                LightSupport.EFFECT,
                LightSupport.COLOR,
                LightSupport.WHITE_VALUE,
            },
        ),
        (0, set()),
        ("0", set()),
    ],
)
def test_init(number, expected_supported_features):
    light_support = LightSupport(number)
    assert light_support.supported_features == expected_supported_features
