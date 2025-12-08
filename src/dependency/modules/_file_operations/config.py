import time
from typing import Any
from logging import Logger

from ._get_package import Log, log_path

log: Log = Log(
    log_sign="file_load",
    log_output_to_file_path=f"{log_path}file_load.log",
)

def check_log(_log: Log | Logger) -> bool:
    """
    :param _log:
    """
    if not isinstance(_log, Log) and not isinstance(_log, Logger):
        raise TypeError("log type not Log or Logger")

    return True

class BaseClass:
    """
    基础类
    """
    def __init__(self, _log: Log | Logger = log):
        check_log(_log)
        self.log: Log = _log
        self.generation_time = time.time()

    def load(self, file_path: str, *args, **kwargs) -> Any:
        pass

    def dump(self, v: Any, file_path: str, *args, **kwargs) -> Any:
        pass
