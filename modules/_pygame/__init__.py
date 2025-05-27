#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._get_package import *
from ._music import Music
from ._sound import Sound
from ._image import Image
from ._font import Font
from._window import Window

log = Log(
    log_sign="pygame",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="w"
)
