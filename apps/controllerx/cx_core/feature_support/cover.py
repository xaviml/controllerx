from typing import Optional
from cx_core.controller import Controller
from cx_core.feature_support import FeatureSupport

SUPPORT_OPEN = 1
SUPPORT_CLOSE = 2
SUPPORT_SET_POSITION = 4
SUPPORT_STOP = 8
SUPPORT_OPEN_TILT = 16
SUPPORT_CLOSE_TILT = 32
SUPPORT_STOP_TILT = 64
SUPPORT_SET_TILT_POSITION = 128


class CoverSupport(FeatureSupport):

    OPEN = 1
    CLOSE = 2
    SET_COVER_POSITION = 4
    STOP = 8
    OPEN_TILT = 16
    CLOSE_TILT = 32
    STOP_TILT = 64
    SET_TILT_POSITION = 128

    def __init__(self, entity: Optional[str], controller: Optional[Controller]) -> None:
        super().__init__(
            entity,
            controller,
            [
                CoverSupport.OPEN,
                CoverSupport.CLOSE,
                CoverSupport.SET_COVER_POSITION,
                CoverSupport.STOP,
                CoverSupport.OPEN_TILT,
                CoverSupport.CLOSE_TILT,
                CoverSupport.STOP_TILT,
                CoverSupport.SET_TILT_POSITION,
            ],
        )
