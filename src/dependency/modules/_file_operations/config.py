#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from __future__ import annotations

import time
from typing import Any
from logging import Logger
from typing import Generic, TypeVar

from ._get_package import Log, log_path

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

T = TypeVar("T")


class ReturnValue(Generic[T]):
    """
    专为返回bool, v值的func设的检查类
    """
    __slots__ = ("ok", "v")
    def __init__(self, ok: bool = False, v: Any | ReturnValue[Any] = None):
        if isinstance(v, ReturnValue):
            self.ok = v.ok
            self.v = v.v
        else:
            self.ok = ok
            self.v = v

    def __call__(self, default: Any = None) -> Any:
        """
        rv()->rv.get()
        """
        return self.get(default=default)

    def get(self, default: Any = None) -> Any:
        if self.ok:
            return self.v
        return default

    def unwrap(self) -> Any:
        """
        强制解包
        """
        return self.v if self.ok else None

    def __bool__(self) -> bool:
        return self.ok


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
