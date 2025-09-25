#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._get_package import *
from ._music import Music
from ._sound import Sound
from ._image import Image
from ._font import Font
from ._key_mapping import Key, MouseButton
from ._window import Window

log = Log(
    log_sign="pygame",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="w"
)

__varsion__ = "1.1.0"
__author__ = "702361946@qq.com"
__license__ = "MIT"
__all__ = [
    "Music",
    "Sound",
    "Image",
    "Font",
    "Key",
    "MouseButton",
    "Window"
]
