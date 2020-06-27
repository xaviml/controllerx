from typing import Optional
from cx_core.controller import Controller
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

    def __init__(self, entity: Optional[str], controller: Optional[Controller]) -> None:
        super().__init__(
            entity,
            controller,
            [
                MediaPlayerSupport.PAUSE,
                MediaPlayerSupport.SEEK,
                MediaPlayerSupport.VOLUME_SET,
                MediaPlayerSupport.VOLUME_MUTE,
                MediaPlayerSupport.PREVIOUS_TRACK,
                MediaPlayerSupport.NEXT_TRACK,
                MediaPlayerSupport.TURN_ON,
                MediaPlayerSupport.TURN_OFF,
                MediaPlayerSupport.PLAY_MEDIA,
                MediaPlayerSupport.VOLUME_STEP,
                MediaPlayerSupport.SELECT_SOURCE,
                MediaPlayerSupport.STOP,
                MediaPlayerSupport.CLEAR_PLAYLIST,
                MediaPlayerSupport.PLAY,
                MediaPlayerSupport.SHUFFLE_SET,
                MediaPlayerSupport.SELECT_SOUND_MODE,
            ],
        )
