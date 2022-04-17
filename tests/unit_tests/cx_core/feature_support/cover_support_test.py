from typing import List

import pytest
from cx_core.feature_support import FeatureSupport
from cx_core.feature_support.cover import CoverSupport
from cx_core.type_controller import Entity, TypeController


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        (1, [CoverSupport.OPEN]),
        (
            15,
            [
                CoverSupport.OPEN,
                CoverSupport.CLOSE,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.STOP,
            ],
        ),
        (
            149,
            [
                CoverSupport.SET_TILT_POSITION,
                CoverSupport.OPEN_TILT,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.OPEN,
            ],
        ),
    ],
)
async def test_is_supported(
    fake_type_controller: TypeController[Entity],
    number: int,
    expected_supported_features: List[int],
) -> None:
    feature_support = FeatureSupport(fake_type_controller)
    feature_support._supported_features = number
    for expected_supported_feature in expected_supported_features:
        assert await feature_support.is_supported(expected_supported_feature)
