#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import pygame

from ._get_package import *

log: Log


class Sound(object):
    def __init__(
            self,
            *,
            store_sound_file_path: str = "sound",
            volume: float = 1.0,
            raise_error: bool = True,
            log: Log = log
    ):
        self.log: Log = log
        self.file_path: str = os.path.join(
            os.getcwd(),
            store_sound_file_path
        )

        self.sounds: dict[str, dict[str, str | pygame.mixer.Sound | None]] = {}
        """
        {
            "x.sound_name": {
                "path": "sound_path",
                "sound": pygame.mixer.Sound
            }
        }
        """

        self.volume: float = volume
        self.raise_error: bool = raise_error

    def init_sound(self, sounds: list[str] | str) -> list[bool]: ...

    def play(self, sound_name: str) -> bool: ...

    def stop(self, sound_name: str) -> bool: ...

    def set_volume(self, sound_name: str, volume: float) -> bool: ...
