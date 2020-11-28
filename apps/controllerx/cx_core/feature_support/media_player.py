from cx_core.feature_support import FeatureSupport


class MediaPlayerSupport(FeatureSupport):
    PAUSE = 1
    SEEK = 2
    VOLUME_SET = 4
    VOLUME_MUTE = 8
    PREVIOUS_TRACK = 16
    NEXT_TRACK = 32
    TURN_ON = 128
    TURN_OFF = 256
    PLAY_MEDIA = 512
    VOLUME_STEP = 1024
    SELECT_SOURCE = 2048
    STOP = 4096
    CLEAR_PLAYLIST = 8192
    PLAY = 16384
    SHUFFLE_SET = 32768
    SELECT_SOUND_MODE = 65536

    features = [
        PAUSE,
        SEEK,
        VOLUME_SET,
        VOLUME_MUTE,
        PREVIOUS_TRACK,
        NEXT_TRACK,
        TURN_ON,
        TURN_OFF,
        PLAY_MEDIA,
        VOLUME_STEP,
        SELECT_SOURCE,
        STOP,
        CLEAR_PLAYLIST,
        PLAY,
        SHUFFLE_SET,
        SELECT_SOUND_MODE,
    ]
