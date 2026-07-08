#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from typing import Protocol, runtime_checkable


@runtime_checkable
class LogProtocol(Protocol):
    """
    日志协议类
    """

    def info(self, message: str, *args, **kwargs) -> None:
        """记录信息级别日志"""
        ...

    def debug(self, message: str, *args, **kwargs) -> None:
        """记录调试级别日志"""
        ...

    def warning(self, message: str, *args, **kwargs) -> None:
        """记录警告级别日志"""
        ...

    def error(self, message: str, *args, **kwargs) -> None:
        """记录错误级别日志"""
        ...

    def critical(self, message: str, *args, **kwargs) -> None: ...
