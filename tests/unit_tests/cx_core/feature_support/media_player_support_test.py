from typing import List

import pytest
from cx_core.feature_support import FeatureSupport
from cx_core.feature_support.media_player import MediaPlayerSupport
from cx_core.type_controller import Entity, TypeController


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        (1, [MediaPlayerSupport.PAUSE]),
        (4, [MediaPlayerSupport.VOLUME_SET]),
        (
            57,
            [
                MediaPlayerSupport.NEXT_TRACK,
                MediaPlayerSupport.PREVIOUS_TRACK,
                MediaPlayerSupport.VOLUME_MUTE,
                MediaPlayerSupport.PAUSE,
            ],
        ),
        (
            149,
            [
                MediaPlayerSupport.TURN_ON,
                MediaPlayerSupport.PREVIOUS_TRACK,
                MediaPlayerSupport.VOLUME_SET,
                MediaPlayerSupport.PAUSE,
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
