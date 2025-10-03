#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

from ._os_name_get import os_name, work_directory
from ._json import Json
from ._log import Log, log_path
from ._log_template import LogTemplate

__varsion__ = "0.1.0"
__author__ = "702361946@qq.com"
__license__ = "MIT"
__all__ = [
    "os_name",
    "Log",
    "LogTemplate",
    "Json",
    "log_path",
    "work_directory",
    "__varsion__",
    "__author__",
    "__license__"
]
