#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Callable

from PySide6.QtCore import QObject, QDate, QTime, QDateTime, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QDateTimeEdit,
    QDateEdit,
    QTimeEdit,
    QDial,
    QKeySequenceEdit,
    QSlider,
    QScrollBar
)

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
            log.warning(f"{cls.__name__}\\safe_widget_call\\widget not found\\{name=}")
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
            func=lambda x: x.toolTip()
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
            log.warning(f"{cls.__name__}\\set_tool_tip\\value type not str\\{type(tool_tip).__name__=}")
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
            log.warning(f"{cls.__name__}\\set_status_tip\\value type not str\\{type(status_tip).__name__=}")
            return False

        _t.setStatusTip(status_tip)
        return True

    @classmethod
    def get_whats_this(
            cls,
            ui: QWidget,
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
            log.warning(f"{cls.__name__}\\set_whats_this\\value type not str\\{type(whats_this).__name__=}")
            return False

        _t.setWhatsThis(whats_this)
        return True


class UICHValue(UICH, ABC):
    @classmethod
    @abstractmethod
    def get_maximum(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | float | None: ...

    @classmethod
    @abstractmethod
    def set_maximum(
            cls,
            ui: QWidget,
            name: str,
            value: int | float
    ) -> bool: ...

    @classmethod
    @abstractmethod
    def get_minimum(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | float | None: ...

    @classmethod
    @abstractmethod
    def set_minimum(
            cls,
            ui: QWidget,
            name: str,
            value: int | float
    ) -> bool: ...


class UICHDateTimeEdit(UICH):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> Any:
        return cls.get_datetime(ui=ui, _type=QDateTimeEdit, name=name)

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: QDateTime
    ) -> bool:
        return cls.set_datetime(ui=ui, _type=QDateTimeEdit, name=name, datetime=value)

    @classmethod
    def get_date(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit]
    ) -> QDate | None:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\get_date\\{_type} is not a supported type")
                return None
        except TypeError as e:
            log.error(f"{cls.__name__}\\get_date\\{e}")
            return None

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_date\\widget not found\\{name=}")
            return None

        t = _t.date()
        log.debug(f"{cls.__name__}\\get_date\\value={t}")
        return t

    @classmethod
    def set_date(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit],
            date: QDate
    ) -> bool:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\set_date\\{_type} is not a supported type")
                return False
        except TypeError as e:
            log.error(f"{cls.__name__}\\set_date\\{e}")
            return False

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_date\\widget not found\\{name=}")
            return False
        if not isinstance(date, QDate):
            log.warning(f"{cls.__name__}\\set_date\\value type not QDate\\{type(date).__name__=}")
            return False

        _t.setDate(date)
        log.debug(f"{cls.__name__}\\set_date\\value={date}")
        return True

    @classmethod
    def get_time(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit],
    ) -> QTime | None:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\get_time\\{_type} is not a supported type")
                return None
        except TypeError as e:
            log.error(f"{cls.__name__}\\get_time\\{e}")
            return None

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_time\\widget not found\\{name=}")
            return None

        t = _t.time()
        log.debug(f"{cls.__name__}\\get_time\\value={t}")
        return t

    @classmethod
    def set_time(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit],
            time: QTime | None
    ) -> bool:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\set_time\\{_type} is not a supported type")
                return False
        except TypeError as e:
            log.error(f"{cls.__name__}\\set_time\\{e}")
            return False

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_time\\widget not found\\{name=}")
            return False
        if not isinstance(time, QTime):
            log.warning(f"{cls.__name__}\\set_time\\value type not QTime\\{type(time).__name__=}")
            return False

        _t.setTime(time)
        log.debug(f"{cls.__name__}\\set_time\\value={time}")
        return True

    @classmethod
    def get_datetime(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit],
    ) -> QDateTime | None:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\get_datetime\\{_type} is not a supported type")
                return None
        except TypeError as e:
            log.error(f"{cls.__name__}\\get_datetime\\{e}")
            return None

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_datetime\\widget not found\\{name=}")
            return None

        t = _t.dateTime()
        log.debug(f"{cls.__name__}\\get_datetime\\value={t}")
        return t

    @classmethod
    def set_datetime(
            cls,
            ui: QWidget,
            name: str,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit],
            datetime: QDateTime
    ) -> bool:
        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\set_datetime\\{_type} is not a supported type")
                return False
        except TypeError as e:
            log.error(f"{cls.__name__}\\set_datetime\\{e}")
            return False

        _t = cls.get_widget_instance(ui=ui, _type=_type, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_datetime\\widget not found\\{name=}")
            return False
        if not isinstance(datetime, QDateTime):
            log.warning(f"{cls.__name__}\\set_datetime\\value type not QDateTime\\{type(datetime).__name__=}")
            return False

        _t.setDateTime(datetime)
        log.debug(f"{cls.__name__}\\set_datetime\\value={datetime}")
        return True


class UICHDateEdit(UICHDateTimeEdit):
    @classmethod
    def get_date(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QDate | None:
        return super().get_date(ui=ui, name=name, _type=QDateEdit)

    @classmethod
    def set_date(
            cls,
            ui: QWidget,
            name: str,
            date: QDate,
            *args,
            **kwargs
    ) -> bool:
        return super().set_date(ui=ui, name=name, date=date, _type=QDateEdit)

    @classmethod
    def get_time(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QTime | None:
        log.warning(f"{cls.__name__}\\get_time\\QDateEdit generally does not handle this content")
        return super().get_time(ui=ui, name=name, _type=QDateEdit)

    @classmethod
    def set_time(
            cls,
            ui: QWidget,
            name: str,
            time: QTime | None,
            *args,
            **kwargs
    ) -> bool:
        log.warning(f"{cls.__name__}\\set_time\\QDateEdit does not handle this content")
        return super().set_time(ui=ui, name=name, time=time, _type=QDateEdit)

    @classmethod
    def get_datetime(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QDateTime | None:
        log.warning(f"{cls.__name__}\\get_datetime\\QDateEdit does not handle this content")
        return super().get_datetime(ui=ui, name=name, _type=QDateEdit)

    @classmethod
    def set_datetime(
            cls,
            ui: QWidget,
            name: str,
            datetime: QDateTime,
            *args,
            **kwargs
    ) -> bool:
        log.warning(f"{cls.__name__}\\set_datetime\\QDateEdit does not handle this content")
        return super().set_datetime(ui=ui, name=name, datetime=datetime, _type=QDateEdit)


class UICHTimeEdit(UICHDateTimeEdit):
    @classmethod
    def get_date(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QDate | None:
        log.warning(f"{cls.__name__}\\get_date\\QTimeEdit does not handle this content")
        return super().get_date(ui=ui, name=name, _type=QTimeEdit)

    @classmethod
    def set_date(
            cls,
            ui: QWidget,
            name: str,
            date: QDate,
            *args,
            **kwargs
    ) -> bool:
        log.warning(f"{cls.__name__}\\set_date\\QTimeEdit does not handle this content")
        return super().set_date(ui=ui, name=name, date=date, _type=QTimeEdit)

    @classmethod
    def get_time(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QTime | None:
        return super().get_time(ui=ui, name=name, _type=QTimeEdit)

    @classmethod
    def set_time(
            cls,
            ui: QWidget,
            name: str,
            time: QTime | None,
            *args,
            **kwargs
    ) -> bool:
        return super().set_time(ui=ui, name=name, time=time, _type=QTimeEdit)

    @classmethod
    def get_datetime(
            cls,
            ui: QWidget,
            name: str,
            *args,
            **kwargs
    ) -> QDateTime | None:
        log.warning(f"{cls.__name__}\\get_datetime\\QTimeEdit does not handle this content")
        return super().get_datetime(ui=ui, name=name, _type=QTimeEdit)

    @classmethod
    def set_datetime(
            cls,
            ui: QWidget,
            name: str,
            datetime: QDateTime,
            *args,
            **kwargs
    ) -> bool:
        log.warning(f"{cls.__name__}\\set_datetime\\QTimeEdit does not handle this content")
        return super().set_datetime(ui=ui, name=name, datetime=datetime, _type=QTimeEdit)


class UICHLineEdit(UICH):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> Any:
        _t = cls.get_widget_instance(ui=ui, _type=QLineEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_value\\widget not found\\{name=}")
            return None
        t = _t.text()
        log.debug(f"{cls.__name__}\\get_value\\value={t}")
        return t

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: str | None
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QLineEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_value\\widget not found\\{name=}")
            return False

        if not isinstance(value, str) and value is not None:
            log.warning(f"{cls.__name__}\\set_value\\value type not str\\{type(value).__name__=}")
            return False

        _t.setText(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
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
            log.warning(f"{cls.__name__}\\set_value\\value type not str\\{type(value).__name__=}")
            return False

        _t.setText(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
        return True


class UICHSpinBox(UICHValue):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_value\\widget not found\\{name=}")
            return None

        t = _t.value()
        log.debug(f"{cls.__name__}\\get_value\\value={t}")
        return t

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: int
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_value\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_value\\value type not int\\{type(value).__name__=}")
            return False

        _t.setValue(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
        return True

    @classmethod
    def get_maximum(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum\\widget not found\\{name=}")
            return None

        t = _t.maximum()
        log.debug(f"{cls.__name__}\\get_maximum\\value={t}")
        return t

    @classmethod
    def set_maximum(
            cls,
            ui: QWidget,
            name: str,
            value: int
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMaximum(value)
        log.debug(f"{cls.__name__}\\set_maximum\\value={value}")
        return True

    @classmethod
    def get_minimum(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_minimum\\widget not found\\{name=}")
            return None

        t = _t.minimum()
        log.debug(f"{cls.__name__}\\get_minimum\\value={t}")
        return t

    @classmethod
    def set_minimum(
            cls,
            ui: QWidget,
            name: str,
            value: int
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_minimum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMinimum(value)
        log.debug(f"{cls.__name__}\\set_minimum\\value={value}")
        return True


class UICHDoubleSpinBox(UICHValue):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> float | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_value\\widget not found\\{name=}")
            return None

        t = _t.value()
        log.debug(f"{cls.__name__}\\get_value\\value={t}")
        return t

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: float
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_value\\widget not found\\{name=}")
            return False
        if not isinstance(value, float):
            log.warning(f"{cls.__name__}\\set_value\\value type not float\\{type(value).__name__=}")
            return False

        _t.setValue(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
        return True

    @classmethod
    def get_maximum(
            cls,
            ui: QWidget,
            name: str,
    ) -> float | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum\\widget not found\\{name=}")
            return None

        t = _t.maximum()
        log.debug(f"{cls.__name__}\\get_maximum\\value={t}")
        return t

    @classmethod
    def set_maximum(
            cls,
            ui: QWidget,
            name: str,
            value: float
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum\\widget not found\\{name=}")
            return False
        if not isinstance(value, float):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not float\\{type(value).__name__=}")
            return False

        _t.setMaximum(value)
        log.debug(f"{cls.__name__}\\set_maximum\\value={value}")
        return True

    @classmethod
    def get_minimum(
            cls,
            ui: QWidget,
            name: str,
    ) -> float | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_minimum\\widget not found\\{name=}")
            return None

        t = _t.minimum()
        log.debug(f"{cls.__name__}\\get_minimum\\value={t}")
        return t

    @classmethod
    def set_minimum(
            cls,
            ui: QWidget,
            name: str,
            value: float
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDoubleSpinBox, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_minimum\\widget not found\\{name=}")
            return False
        if not isinstance(value, float):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not float\\{type(value).__name__=}")
            return False

        _t.setMinimum(value)
        log.debug(f"{cls.__name__}\\set_minimum\\value={value}")
        return True


class UICHQDial(UICHValue):
    @classmethod
    def get_value(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_value\\widget not found\\{name=}")
            return None
        t = _t.value()
        log.debug(f"{cls.__name__}\\get_value\\value={t}")
        return t

    @classmethod
    def set_value(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_value\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_value\\value type not int\\{type(value).__name__=}")
            return False
        _t.setValue(value)
        log.debug(f"{cls.__name__}\\set_value\\value={value}")
        return True

    @classmethod
    def get_maximum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum\\widget not found\\{name=}")
            return None
        t = _t.maximum()
        log.debug(f"{cls.__name__}\\get_maximum\\value={t}")
        return t

    @classmethod
    def set_maximum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int\\{type(value).__name__=}")
            return False
        _t.setMaximum(value)
        log.debug(f"{cls.__name__}\\set_maximum\\value={value}")
        return True

    @classmethod
    def get_minimum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_minimum\\widget not found\\{name=}")
            return None
        t = _t.minimum()
        log.debug(f"{cls.__name__}\\get_minimum\\value={t}")
        return t

    @classmethod
    def set_minimum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_minimum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int\\{type(value).__name__=}")
            return False
        _t.setMinimum(value)
        log.debug(f"{cls.__name__}\\set_minimum\\value={value}")
        return True

    @classmethod
    def get_notches_visible(cls, ui: QWidget, name: str) -> bool | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_notches_visible\\widget not found\\{name=}")
            return None
        t = _t.notchesVisible()
        log.debug(f"{cls.__name__}\\get_notches_visible\\value={t}")
        return t

    @classmethod
    def set_notches_visible(cls, ui: QWidget, name: str, visible: bool) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_notches_visible\\widget not found\\{name=}")
            return False
        if not isinstance(visible, bool):
            log.warning(f"{cls.__name__}\\set_notches_visible\\value type not bool\\{type(visible).__name__=}")
            return False
        _t.setNotchesVisible(visible)
        log.debug(f"{cls.__name__}\\set_notches_visible\\value={visible}")
        return True

    @classmethod
    def get_wrapping(cls, ui: QWidget, name: str) -> bool | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_wrapping\\widget not found\\{name=}")
            return None
        t = _t.wrapping()
        log.debug(f"{cls.__name__}\\get_wrapping\\value={t}")
        return t

    @classmethod
    def set_wrapping(cls, ui: QWidget, name: str, wrapping: bool) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_wrapping\\widget not found\\{name=}")
            return False
        if not isinstance(wrapping, bool):
            log.warning(f"{cls.__name__}\\set_wrapping\\value type not bool\\{type(wrapping).__name__=}")
            return False
        _t.setWrapping(wrapping)
        log.debug(f"{cls.__name__}\\set_wrapping\\value={wrapping}")
        return True

    @classmethod
    def get_notch_target(cls, ui: QWidget, name: str) -> float | None:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_notch_target\\widget not found\\{name=}")
            return None
        t = _t.notchTarget()
        log.debug(f"{cls.__name__}\\get_notch_target\\value={t}")
        return t

    @classmethod
    def set_notch_target(cls, ui: QWidget, name: str, target: float) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QDial, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_notch_target\\widget not found\\{name=}")
            return False
        if not isinstance(target, (int, float)):
            log.warning(f"{cls.__name__}\\set_notch_target\\value type not float\\{type(target).__name__=}")
            return False
        _t.setNotchTarget(float(target))
        log.debug(f"{cls.__name__}\\set_notch_target\\value={target}")
        return True


class UICHQKeySequenceEdit(UICH):
    @classmethod
    def get_value(
            cls,
            ui: QWidget,
            name: str,
    ) -> QKeySequence | None:
        return cls.get_key_sequence(ui=ui, name=name)

    @classmethod
    def set_value(
            cls,
            ui: QWidget,
            name: str,
            value: QKeySequence | None
    ) -> bool:
        if value is None:
            return cls.clear(ui=ui, name=name)
        return cls.set_key_sequence(ui=ui, name=name, key_sequence=value)

    @classmethod
    def get_key_sequence(
            cls,
            ui: QWidget,
            name: str,
    ) -> QKeySequence | None:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_key_sequence\\widget not found\\{name=}")
            return None

        t = _t.keySequence()
        if t.isEmpty():
            log.debug(f"{cls.__name__}\\get_key_sequence\\value is empty")
            return None

        log.debug(f"{cls.__name__}\\get_key_sequence\\value={t.toString()}")
        return t

    @classmethod
    def set_key_sequence(
            cls,
            ui: QWidget,
            name: str,
            key_sequence: QKeySequence
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_key_sequence\\widget not found\\{name=}")
            return False

        if not isinstance(key_sequence, QKeySequence):
            log.warning(f"{cls.__name__}\\set_key_sequence\\value type not QKeySequence\\{type(key_sequence).__name__=}")
            return False

        _t.setKeySequence(key_sequence)
        log.debug(f"{cls.__name__}\\set_key_sequence\\value={key_sequence.toString()}")
        return True

    @classmethod
    def clear(
            cls,
            ui: QWidget,
            name: str,
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\clear\\widget not found\\{name=}")
            return False

        _t.clear()
        log.debug(f"{cls.__name__}\\clear\\{name=}")
        return True

    @classmethod
    def get_maximum_sequence_length(
            cls,
            ui: QWidget,
            name: str,
    ) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum_sequence_length\\widget not found\\{name=}")
            return None

        t = _t.maximumSequenceLength()
        log.debug(f"{cls.__name__}\\get_maximum_sequence_length\\value={t}")
        return t

    @classmethod
    def set_maximum_sequence_length(
            cls,
            ui: QWidget,
            name: str,
            value: int
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum_sequence_length\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum_sequence_length\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMaximumSequenceLength(value)
        log.debug(f"{cls.__name__}\\set_maximum_sequence_length\\value={value}")
        return True

    @classmethod
    def is_clear_button_enabled(
            cls,
            ui: QWidget,
            name: str,
    ) -> bool | None:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\is_clear_button_enabled\\widget not found\\{name=}")
            return None

        t = _t.isClearButtonEnabled()
        log.debug(f"{cls.__name__}\\is_clear_button_enabled\\value={t}")
        return t

    @classmethod
    def set_clear_button_enabled(
            cls,
            ui: QWidget,
            name: str,
            enabled: bool
    ) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QKeySequenceEdit, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_clear_button_enabled\\widget not found\\{name=}")
            return False
        if not isinstance(enabled, bool):
            log.warning(f"{cls.__name__}\\set_clear_button_enabled\\value type not bool\\{type(enabled).__name__=}")
            return False

        _t.setClearButtonEnabled(enabled)
        log.debug(f"{cls.__name__}\\set_clear_button_enabled\\value={enabled}")
        return True


class UICHQSlider(UICHValue):
    @classmethod
    def get_value(cls, ui: QWidget, name: str) -> int | None:
        return cls.get_slider_value(ui=ui, name=name)

    @classmethod
    def set_value(cls, ui: QWidget, name: str, value: int) -> bool:
        return cls.set_slider_value(ui=ui, name=name, value=value)

    @classmethod
    def get_slider_value(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_slider_value\\widget not found\\{name=}")
            return None

        t = _t.value()
        log.debug(f"{cls.__name__}\\get_slider_value\\value={t}")
        return t

    @classmethod
    def set_slider_value(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_slider_value\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_slider_value\\value type not int\\{type(value).__name__=}")
            return False

        _t.setValue(value)
        log.debug(f"{cls.__name__}\\set_slider_value\\value={value}")
        return True

    @classmethod
    def get_maximum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum\\widget not found\\{name=}")
            return None

        t = _t.maximum()
        log.debug(f"{cls.__name__}\\get_maximum\\value={t}")
        return t

    @classmethod
    def set_maximum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMaximum(value)
        log.debug(f"{cls.__name__}\\set_maximum\\value={value}")
        return True

    @classmethod
    def get_minimum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_minimum\\widget not found\\{name=}")
            return None

        t = _t.minimum()
        log.debug(f"{cls.__name__}\\get_minimum\\value={t}")
        return t

    @classmethod
    def set_minimum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_minimum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMinimum(value)
        log.debug(f"{cls.__name__}\\set_minimum\\value={value}")
        return True

    @classmethod
    def get_orientation(cls, ui: QWidget, name: str) -> Qt.Orientation | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_orientation\\widget not found\\{name=}")
            return None

        t = _t.orientation()
        log.debug(f"{cls.__name__}\\get_orientation\\value={t}")
        return t

    @classmethod
    def set_orientation(cls, ui: QWidget, name: str, orientation: Qt.Orientation) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_orientation\\widget not found\\{name=}")
            return False
        if not isinstance(orientation, Qt.Orientation):
            log.warning(f"{cls.__name__}\\set_orientation\\value type not Qt.Orientation\\{type(orientation).__name__=}")
            return False

        _t.setOrientation(orientation)
        log.debug(f"{cls.__name__}\\set_orientation\\value={orientation}")
        return True

    @classmethod
    def get_single_step(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_single_step\\widget not found\\{name=}")
            return None

        t = _t.singleStep()
        log.debug(f"{cls.__name__}\\get_single_step\\value={t}")
        return t

    @classmethod
    def set_single_step(cls, ui: QWidget, name: str, step: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_single_step\\widget not found\\{name=}")
            return False
        if not isinstance(step, int):
            log.warning(f"{cls.__name__}\\set_single_step\\value type not int\\{type(step).__name__=}")
            return False

        _t.setSingleStep(step)
        log.debug(f"{cls.__name__}\\set_single_step\\value={step}")
        return True

    @classmethod
    def get_page_step(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_page_step\\widget not found\\{name=}")
            return None

        t = _t.pageStep()
        log.debug(f"{cls.__name__}\\get_page_step\\value={t}")
        return t

    @classmethod
    def set_page_step(cls, ui: QWidget, name: str, step: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_page_step\\widget not found\\{name=}")
            return False
        if not isinstance(step, int):
            log.warning(f"{cls.__name__}\\set_page_step\\value type not int\\{type(step).__name__=}")
            return False

        _t.setPageStep(step)
        log.debug(f"{cls.__name__}\\set_page_step\\value={step}")
        return True

    @classmethod
    def get_tick_interval(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_tick_interval\\widget not found\\{name=}")
            return None

        t = _t.tickInterval()
        log.debug(f"{cls.__name__}\\get_tick_interval\\value={t}")
        return t

    @classmethod
    def set_tick_interval(cls, ui: QWidget, name: str, interval: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_tick_interval\\widget not found\\{name=}")
            return False
        if not isinstance(interval, int):
            log.warning(f"{cls.__name__}\\set_tick_interval\\value type not int\\{type(interval).__name__=}")
            return False

        _t.setTickInterval(interval)
        log.debug(f"{cls.__name__}\\set_tick_interval\\value={interval}")
        return True

    @classmethod
    def get_tick_position(cls, ui: QWidget, name: str) -> QSlider.TickPosition | None:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_tick_position\\widget not found\\{name=}")
            return None

        t = _t.tickPosition()
        log.debug(f"{cls.__name__}\\get_tick_position\\value={t}")
        return t

    @classmethod
    def set_tick_position(cls, ui: QWidget, name: str, position: QSlider.TickPosition) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QSlider, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_tick_position\\widget not found\\{name=}")
            return False
        if not isinstance(position, QSlider.TickPosition):
            log.warning(f"{cls.__name__}\\set_tick_position\\value type not QSlider.TickPosition\\{type(position).__name__=}")
            return False

        _t.setTickPosition(position)
        log.debug(f"{cls.__name__}\\set_tick_position\\value={position}")
        return True


class UICHQScrollBar(UICHValue):
    @classmethod
    def get_value(cls, ui: QWidget, name: str) -> int | None:
        return cls.get_scrollbar_value(ui=ui, name=name)

    @classmethod
    def set_value(cls, ui: QWidget, name: str, value: int) -> bool:
        return cls.set_scrollbar_value(ui=ui, name=name, value=value)

    @classmethod
    def get_scrollbar_value(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_scrollbar_value\\widget not found\\{name=}")
            return None

        t = _t.value()
        log.debug(f"{cls.__name__}\\get_scrollbar_value\\value={t}")
        return t

    @classmethod
    def set_scrollbar_value(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_scrollbar_value\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_scrollbar_value\\value type not int\\{type(value).__name__=}")
            return False

        _t.setValue(value)
        log.debug(f"{cls.__name__}\\set_scrollbar_value\\value={value}")
        return True

    @classmethod
    def get_maximum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_maximum\\widget not found\\{name=}")
            return None

        t = _t.maximum()
        log.debug(f"{cls.__name__}\\get_maximum\\value={t}")
        return t

    @classmethod
    def set_maximum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_maximum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMaximum(value)
        log.debug(f"{cls.__name__}\\set_maximum\\value={value}")
        return True

    @classmethod
    def get_minimum(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_minimum\\widget not found\\{name=}")
            return None

        t = _t.minimum()
        log.debug(f"{cls.__name__}\\get_minimum\\value={t}")
        return t

    @classmethod
    def set_minimum(cls, ui: QWidget, name: str, value: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_minimum\\widget not found\\{name=}")
            return False
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int\\{type(value).__name__=}")
            return False

        _t.setMinimum(value)
        log.debug(f"{cls.__name__}\\set_minimum\\value={value}")
        return True

    @classmethod
    def get_single_step(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_single_step\\widget not found\\{name=}")
            return None

        t = _t.singleStep()
        log.debug(f"{cls.__name__}\\get_single_step\\value={t}")
        return t

    @classmethod
    def set_single_step(cls, ui: QWidget, name: str, step: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_single_step\\widget not found\\{name=}")
            return False
        if not isinstance(step, int):
            log.warning(f"{cls.__name__}\\set_single_step\\value type not int\\{type(step).__name__=}")
            return False

        _t.setSingleStep(step)
        log.debug(f"{cls.__name__}\\set_single_step\\value={step}")
        return True

    @classmethod
    def get_page_step(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_page_step\\widget not found\\{name=}")
            return None

        t = _t.pageStep()
        log.debug(f"{cls.__name__}\\get_page_step\\value={t}")
        return t

    @classmethod
    def set_page_step(cls, ui: QWidget, name: str, step: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_page_step\\widget not found\\{name=}")
            return False
        if not isinstance(step, int):
            log.warning(f"{cls.__name__}\\set_page_step\\value type not int\\{type(step).__name__=}")
            return False

        _t.setPageStep(step)
        log.debug(f"{cls.__name__}\\set_page_step\\value={step}")
        return True

    @classmethod
    def get_orientation(cls, ui: QWidget, name: str) -> Qt.Orientation | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_orientation\\widget not found\\{name=}")
            return None

        t = _t.orientation()
        log.debug(f"{cls.__name__}\\get_orientation\\value={t}")
        return t

    @classmethod
    def set_orientation(cls, ui: QWidget, name: str, orientation: Qt.Orientation) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_orientation\\widget not found\\{name=}")
            return False
        if not isinstance(orientation, Qt.Orientation):
            log.warning(f"{cls.__name__}\\set_orientation\\value type not Qt.Orientation\\{type(orientation).__name__=}")
            return False

        _t.setOrientation(orientation)
        log.debug(f"{cls.__name__}\\set_orientation\\value={orientation}")
        return True

    @classmethod
    def get_slider_position(cls, ui: QWidget, name: str) -> int | None:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\get_slider_position\\widget not found\\{name=}")
            return None

        t = _t.sliderPosition()
        log.debug(f"{cls.__name__}\\get_slider_position\\value={t}")
        return t

    @classmethod
    def set_slider_position(cls, ui: QWidget, name: str, position: int) -> bool:
        _t = cls.get_widget_instance(ui=ui, _type=QScrollBar, name=name)
        if _t is None:
            log.warning(f"{cls.__name__}\\set_slider_position\\widget not found\\{name=}")
            return False
        if not isinstance(position, int):
            log.warning(f"{cls.__name__}\\set_slider_position\\value type not int\\{type(position).__name__=}")
            return False

        _t.setSliderPosition(position)
        log.debug(f"{cls.__name__}\\set_slider_position\\value={position}")
        return True
