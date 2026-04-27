#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from typing import Any, TypeVar, Callable

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QTextEdit

from .config import log

QObjectType = TypeVar("QObjectType", bound=QObject)
QWidgetType = TypeVar("QWidgetType", bound=QWidget)


class UICH:
    @classmethod
    def get_widget_instance(
            cls,
            ui: QWidget,
            _type: type[QObjectType],
            name: str
    ) -> QObjectType | None:
        """
        获取部件实例
        :param ui:
        :param _type:
        :param name:
        :return:
        """
        _t = ui.findChild(_type, name=name)
        log.info(f"{cls.__name__}\\get_widget_instance\\type={_type.__name__}&try={'True' if _t else 'False'}&{name=}")
        return _t

    @classmethod
    def safe_widget_call(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
            func: Callable[[QWidgetType], Any],
            default: Any = None
    ) -> Any:
        widget = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if widget is None:
            log.warning(f"{cls.__name__}: widget not found, {name=}")
            return default
        return func(widget)

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
    ) -> bool: ...

    @classmethod
    def get_tool_tip(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
    ) -> str | None:
        return cls.safe_widget_call(
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x:x.toolTip()
        )

    @classmethod
    def set_tool_tip(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
            tool_tip: str
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_tool_tip\\widget not found\\{name=}")
            return False

        if not isinstance(tool_tip, str):
            log.warning(f"{cls.__name__}\\set_tool_tip\\value type not str\\value_type={type(tool_tip).__name__}")
            return False

        _t.setToolTip(tool_tip)
        return True

    @classmethod
    def get_status_tip(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
    ) -> str | None:
        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_status_tip\\widget not found\\{name=}")
            return None
        return _t.statusTip()

    @classmethod
    def set_status_tip(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
            status_tip: str
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_status_tip\\widget not found\\{name=}")
            return False
        if not isinstance(status_tip, str):
            log.warning(f"{cls.__name__}\\set_status_tip\\value type not str\\value_type={type(status_tip).__name__}")
            return False

        _t.setStatusTip(status_tip)
        return True

    @classmethod
    def get_whats_this(
            cls
            ,ui: QWidget,
            _type: type[QWidgetType],
            name: str
    ) -> str | None:
        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_whats_this\\widget not found\\{name=}")
            return None
        return _t.whatsThis()

    @classmethod
    def set_whats_this(
            cls,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str,
            whats_this: str
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_whats_this\\widget not found\\{name=}")
            return False
        if not isinstance(whats_this, str):
            log.warning(f"{cls.__name__}\\set_whats_this\\value type not str\\value_type={type(whats_this).__name__}")
            return False

        _t.setWhatsThis(whats_this)
        return True



class UICHTextEdit(UICH):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> str | None:
        _t = cls.get_widget_instance(ui=ui, _type=QTextEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_value\\widget not found\\{name=}")
            return None
        t = _t.toPlainText()
        log.debug(f"{cls.__name__}\\get_value\\value={t}")
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
            log.warning(f"{cls.__name__}\\set_value\\widget not found\\{name=}")
            return False

        if not isinstance(value, str):
            log.warning(f"{cls.__name__}\\set_value\\value type not str\\value_type={type(value).__name__}")
            return False

        _t.setText(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
        return True

