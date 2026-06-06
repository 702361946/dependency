#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from __future__ import annotations

import time
from typing import Any
from logging import Logger

from ._get_package import Log, log_path
from modules._error_handling import ReturnValue

log: Log = Log(
    log_sign="file_load",
    log_output_to_file_path=f"{log_path}file_load.log",
)

def check_log(_log: Log | Logger) -> ReturnValue[Exception | None]:
    """
    :param _log:
    """
    if not isinstance(_log, Log) and not isinstance(_log, Logger):
        return ReturnValue(False, TypeError("log type not Log or Logger"))

    return ReturnValue(True, None)


class BaseClass:
    """
    基础类
    """
    def __init__(self, _log: Log | Logger = log):
        if not check_log(_log).ok:
            self.log: Log = log
        else:
            self.log: Log = _log
        self.generation_time = time.time()

    def load(self, file_path: str, *args, **kwargs) -> ReturnValue[Any]:
        pass

    def dump(self, v: Any, file_path: str, *args, **kwargs) -> ReturnValue[Any]:
        pass
