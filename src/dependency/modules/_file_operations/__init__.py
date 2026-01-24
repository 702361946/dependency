#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from .config import ReturnValue, BaseClass
from ._path import PathTools
from ._file import File, FileBaseClass
from ._interpreter import Interpreter
from .f_csv import CSV
from .f_ini import Ini
from .f_json import Json
from .f_toml import Toml

__version__ = "0.0.1"
__author__ = "702361946@qq.com"
__license__ = "MIT"
__all__ = [
    'BaseClass',
    'ReturnValue',
    "PathTools",
    'File',
    'FileBaseClass',
    "Interpreter",
    'CSV',
    "Ini",
    'Json',
    'Toml',
]
