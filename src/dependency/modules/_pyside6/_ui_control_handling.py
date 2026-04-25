#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from typing import Any, TypeVar

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QTextEdit

from .config import log

PlaceholderType = TypeVar("PlaceholderType", bound=QObject)


class UICH:
    @classmethod
    def get_widget_instance(
            cls,
            ui: QWidget,
            _type: type[PlaceholderType],
            name: str
    ) -> PlaceholderType | None:
        """
        获取部件实例
        :param ui:
        :param _type:
        :param name:
        :return:
        """
        _t = ui.findChild(_type, name=name)
        log.info(f"get_widget_instance\\type={_type.__name__}&try={'True' if _t else 'False'}&{name=}")
        return _t

    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> Any: ...

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: Any
    ) -> Any: ...


class UICHTextEdit(UICH):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> str | None:
        _t = cls.get_widget_instance(ui=ui, _type=QTextEdit, name=name)
        if _t is None:
            log.warning(f"TE\\get_value\\widget not found\\{name=}")
            return None
        t = _t.toPlainText()
        log.debug(f"TE\\get_value\\value={t}")
        return t

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: str
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QTextEdit, name=name)
        if _t is None:
            log.warning(f"TE\\set_value\\widget not found\\{name=}")
            return False

        if not isinstance(value, str):
            log.warning(f"TE\\set_value\\value type not str\\value_type={type(value).__name__}")
            return False

        _t.setText(value)
        log.debug(f"TE\\set_value\\value={value}")
        return True

