#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._music import *
from ._sound import *
from ._image import *

log = Log(
    log_sign="pygame",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="w"
)
