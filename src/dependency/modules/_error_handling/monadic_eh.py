#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from __future__ import annotations
from collections.abc import Callable
from typing import Any


class MEH:
    """
    monadic error handling class
    """
    def __init__(
            self,
            *,
            v: Any = None,
            ok: bool = True,
            e: Any = None,
    ):
        self.v: Any = v
        self.ok: bool = ok
        self.e: Any = e

    @classmethod
    def unit_ok(
            cls,
            v: Any,
            **kwargs
    ) -> MEH:
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
    ) -> MEH:
        """
        失败
        :param e:
        :param kwargs:
        :return:
        """
        return cls(ok=False, e=e, **kwargs)

    def bind(
            self,
            func: Callable[[Any], MEH],
    ) -> MEH:
        """

        :param func:func返回必须为MEH实例
        :return:
        """
        if not self.ok:
            return self

        return func(self.v)

    def map(
            self,
            func: Callable[[Any], Any],
    ) -> MEH:
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
