from core.feature_support.cover import CoverSupport
import pytest


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        ("1", {CoverSupport.OPEN,},),
        (
            "15",
            {
                CoverSupport.OPEN,
                CoverSupport.CLOSE,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.STOP,
            },
        ),
        (
            "149",
            {
                CoverSupport.SET_TILT_POSITION,
                CoverSupport.OPEN_TILT,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.OPEN,
            },
        ),
        (0, set()),
        ("0", set()),
    ],
)
def test_init(number, expected_supported_features):
    cover_support = CoverSupport(number)
    assert cover_support.supported_features == expected_supported_features
