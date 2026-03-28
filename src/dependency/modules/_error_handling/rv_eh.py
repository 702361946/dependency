#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from __future__ import annotations

from typing import Any, TypeVar, Generic

T = TypeVar("T")


class ReturnValue(Generic[T]):
    """
    返回bool&value
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