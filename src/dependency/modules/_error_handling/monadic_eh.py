#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from __future__ import annotations
from collections.abc import Callable
from typing import Any, TypeVar, Generic, cast

T = TypeVar("T")
U = TypeVar("U")      # 用于 map/bind 的输出类型推断
V = TypeVar("V")      # 用于 unit_ok 的值类型推断


class MEH(Generic[T]):
    """
    monadic error handling class
    """
    def __init__(
            self,
            *,
            v: T | None = None,
            ok: bool = True,
            e: Any = None,
    ):
        self.v: Any = v
        self.ok: bool = ok
        self.e: Any = e

    @classmethod
    def unit_ok(
            cls,
            v: V,
            **kwargs
    ) -> MEH[V]:
        """
        成功
        :param v:
        :param kwargs:
        :return:
        """
        return cls(ok=True, v=v, **kwargs)

    @classmethod
    def unit_err(
            cls,
            e: Any,
            **kwargs
    ) -> MEH[Any]:
        """
        失败
        :param e:
        :param kwargs:
        :return:
        """
        return cls(ok=False, e=e, **kwargs)

    def bind(
            self,
            func: Callable[[T], MEH[U]],
    ) -> MEH[U]:
        """

        :param func:func返回必须为MEH实例
        :return:
        """
        if not self.ok:
            return self

        return func(self.v)

    def map(
            self,
            func: Callable[[T], U],
    ) -> MEH[U]:
        """

        :param func:
        :return:
        """
        if not self.ok:
            return self

        try:
            v = func(self.v)
        except Exception as e:
            return MEH.unit_err(e)

        if not isinstance(v, MEH):
            return MEH.unit_ok(v)
        raise TypeError('The parameter "func" passed to the map method cannot return an MEH type')

    def map_no_raise(
            self,
            func: Callable[[T], U],
    ) -> MEH[U]:
        if not self.ok:
            return self

        try:
            v = func(self.v)
        except Exception as e:
            return MEH.unit_err(e)

        if not isinstance(v, MEH):
            return v
        return MEH.unit_ok(v)

    def bind_no_arg_func(
            self,
            func: Callable[[], MEH[U]],
    ) -> MEH[U]:
        if not self.ok:
            return self

        return func()

    def map_no_arg_func(
            self,
            func: Callable[[], U],
    ) -> MEH[U]:
        """

        :param func:
        :return:
        """
        if not self.ok:
            return self

        try:
            v = func()
        except Exception as e:
            return MEH.unit_err(e)

        if not isinstance(v, MEH):
            return MEH.unit_ok(v)
        raise TypeError('The parameter "func" passed to the map method cannot return an MEH type')

    def map_no_raise_no_arg_func(
            self,
            func: Callable[[], U],
    ) -> MEH[U]:
        """

        :param func:
        :return:
        """
        if not self.ok:
            return self

        try:
            v = func()
        except Exception as e:
            return MEH.unit_err(e)

        if not isinstance(v, MEH):
            return MEH.unit_ok(v)
        return MEH.unit_ok(v)

    def unwrap(self) -> T | Any:
        """
        强制解包
        """
        return self.v if self.ok else self.e

    def get(self, default: Any = None) -> T | U | None:
        if self.ok:
            return self.v
        return default

    def __call__(self, default: Any = None) -> T | U | None:
        return self.get(default=default)

    def __bool__(self):
        return self.ok
