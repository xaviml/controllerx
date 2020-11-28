from cx_core.feature_support import FeatureSupport


class CoverSupport(FeatureSupport):

    OPEN = 1
    CLOSE = 2
    SET_COVER_POSITION = 4
    STOP = 8
    OPEN_TILT = 16
    CLOSE_TILT = 32
    STOP_TILT = 64
    SET_TILT_POSITION = 128

    features = [
        OPEN,
        CLOSE,
        SET_COVER_POSITION,
        STOP,
        OPEN_TILT,
        CLOSE_TILT,
        STOP_TILT,
        SET_TILT_POSITION,
    ]
