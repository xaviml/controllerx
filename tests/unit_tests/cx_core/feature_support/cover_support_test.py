import pytest
from cx_core.feature_support import FeatureSupport, SupportedFeatures
from cx_core.feature_support.cover import CoverSupport


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        (1, {CoverSupport.OPEN}),
        (
            15,
            {
                CoverSupport.OPEN,
                CoverSupport.CLOSE,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.STOP,
            },
        ),
        (
            149,
            {
                CoverSupport.SET_TILT_POSITION,
                CoverSupport.OPEN_TILT,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.OPEN,
            },
        ),
        (0, set()),
    ],
)
def test_decode(number: int, expected_supported_features: SupportedFeatures):
    supported_features = FeatureSupport.decode(number, CoverSupport.features)
    assert supported_features == expected_supported_features
