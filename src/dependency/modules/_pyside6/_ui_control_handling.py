#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from typing import Any, Callable, TypeVar

from PySide6.QtCore import QDate, QTime, QDateTime, Qt
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

from modules._error_handling import MEH
from .config import log

QWidgetType = TypeVar("QWidgetType", bound=QWidget)
R = TypeVar("R")


class UICH:
    @classmethod
    def __get_widget_instance_or_return_widget_instance(
            cls,
            *,
            widget: QWidgetType | None = None,
            ui: QWidget | None = None,
            _type: type[QWidgetType] | None = None,
            name: str = None
    ) -> MEH[QWidgetType]:
        if widget is not None:
            if isinstance(widget, QWidget):
                return MEH.unit_ok(widget)
            else:
                log.warning(f"{cls.__name__}\\__gwiorwi\\widget type not QWidget")

        if ui is None or _type is None or name is None:
            log.warning(f"{cls.__name__}\\__gwiorwi\\Incomplete parameters, ui or type or name is none")
            return MEH.unit_err("ui or type or name is None, Please provide all the parameters")

        return cls.get_widget_instance(ui=ui, _type=_type, name=name)

    @classmethod
    def get_widget_instance(
            cls,
            *,
            ui: QWidget,
            _type: type[QWidgetType],
            name: str
    ) -> MEH[QWidgetType]:
        """
        获取部件实例
        :param ui:
        :param _type:
        :param name:
        :return:
        """
        _t = ui.findChild(_type, name=name)
        if _t is None:
            log.info(f"{cls.__name__}\\get_widget_instance\\Component not found\\{_type.__name__=}&{name=}")
            return MEH.unit_err("Component not found")

        log.debug(f"{cls.__name__}\\get_widget_instance\\Component found\\{_t=}")
        return MEH.unit_ok(_t)

    @classmethod
    def safe_widget_call(
            cls,
            *,
            func: Callable[[QWidgetType], R],
            widget: QWidgetType = None,
            ui: QWidget = None,
            _type: type[QWidgetType] = None,
            name: str = None
    ) -> MEH[R]:
        return cls.__get_widget_instance_or_return_widget_instance(
            ui=ui,
            _type=_type,
            name=name,
            widget=widget
        ).map_no_raise(func)

    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[Any]:
        ...

    @classmethod
    def set_value(
            cls,
            *,
            value: Any,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[None]:
        ...

    @classmethod
    def get_tool_tip(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x: x.toolTip()
        )

    @classmethod
    def set_tool_tip(
            cls,
            *,
            tool_tip: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[None]:
        if not isinstance(tool_tip, str):
            log.warning(f"{cls.__name__}\\set_tool_tip\\value type not str\\{type(tool_tip).__name__=}")
            return MEH.unit_err("tool_tip type not str")

        return cls.safe_widget_call(
            func=lambda x: x.setToolTip(tool_tip),
            widget=widget,
            ui=ui,
            _type=_type,
            name=name
        )

    @classmethod
    def get_status_tip(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            func=lambda x: x.statusTip(),
            widget=widget,
            ui=ui,
            _type=_type,
            name=name
        )

    @classmethod
    def set_status_tip(
            cls,
            *,
            status_tip: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[None]:
        _t = cls.__get_widget_instance_or_return_widget_instance(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name
        )
        if not isinstance(status_tip, str):
            log.warning(f"{cls.__name__}\\set_status_tip\\value type not str\\{type(status_tip).__name__=}")
            return MEH.unit_err("status_tip type not str")

        return _t.map(lambda x: x.setStatusTip(status_tip))

    @classmethod
    def get_whats_this(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[str]:
        _t = cls.__get_widget_instance_or_return_widget_instance(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name
        )

        return _t.map(lambda x: x.whatsThis())

    @classmethod
    def set_whats_this(
            cls,
            *,
            whats_this: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QWidgetType] = None,
    ) -> MEH[None]:
        _t = cls.__get_widget_instance_or_return_widget_instance(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name
        )
        if not isinstance(whats_this, str):
            log.warning(f"{cls.__name__}\\set_whats_this\\value type not str\\{type(whats_this).__name__=}")
            return MEH.unit_err("whats_this type not str")

        return _t.map(lambda x: x.setWhatsThis(whats_this))


class UICHValue(UICH):
    @classmethod
    def get_value(
            cls,
            *,
            widget: (
                    QSpinBox |
                    QDoubleSpinBox |
                    QSlider |
                    QScrollBar |
                    QDial
            ) = None,
            ui: QWidget = None,
            name: str = None,
            _type: (
                    type[QSpinBox] |
                    type[QDoubleSpinBox] |
                    type[QSlider] |
                    type[QScrollBar] |
                    type[QDial]
            ) = None,
    ) -> MEH[int | float]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=_type,
            func=lambda x: x.value()
        )

    @classmethod
    def get_maximum(
            cls,
            *,
            widget: (
                    QSpinBox |
                    QDoubleSpinBox |
                    QDial |
                    QSlider |
                    QScrollBar
            ) = None,
            ui: QWidget = None,
            name: str = None,
            _type: (
                    type[QSpinBox] |
                    type[QDoubleSpinBox] |
                    type[QDial] |
                    type[QSlider] |
                    type[QScrollBar]
            ) = None,
    ) -> MEH[int | float]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x: x.maximum(),
        )

    @classmethod
    def set_maximum(
            cls,
            *,
            value: int | float,
            widget: (
                    QSpinBox |
                    QDoubleSpinBox |
                    QDial |
                    QSlider |
                    QScrollBar
            ) = None,
            ui: QWidget = None,
            name: str = None,
            _type: (
                    type[QSpinBox] |
                    type[QDoubleSpinBox] |
                    type[QDial] |
                    type[QSlider] |
                    type[QScrollBar]
            ) = None,
    ) -> MEH[None]:
        if not isinstance(value, (int, float)):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int or float\\{type(value).__name__=}")
            return MEH.unit_err("value type not int or float")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x: x.setMaximum(value)
        )

    @classmethod
    def get_minimum(
            cls,
            *,
            widget: (
                    QSpinBox |
                    QDoubleSpinBox |
                    QDial |
                    QSlider |
                    QScrollBar
            ) = None,
            ui: QWidget = None,
            name: str = None,
            _type: (
                    type[QSpinBox] |
                    type[QDoubleSpinBox] |
                    type[QDial] |
                    type[QSlider] |
                    type[QScrollBar]
            ) = None,
    ) -> MEH[int | float]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x: x.minimum(),
        )

    @classmethod
    def set_minimum(
            cls,
            *,
            value: int | float,
            widget: (
                    QSpinBox |
                    QDoubleSpinBox |
                    QDial |
                    QSlider |
                    QScrollBar
            ) = None,
            ui: QWidget = None,
            name: str = None,
            _type: (
                    type[QSpinBox] |
                    type[QDoubleSpinBox] |
                    type[QDial] |
                    type[QSlider] |
                    type[QScrollBar]
            ) = None,
    ) -> MEH[None]:
        if not isinstance(value, (int, float)):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int or float\\{type(value).__name__=}")
            return MEH.unit_err("value type not int or float")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=_type,
            name=name,
            func=lambda x: x.setMinimum(value)
        )


class UICHDateTimeEdit(UICH):
    @classmethod
    def __type_issubclass_datetime(
            cls,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None
    ) -> type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] | None:
        if _type is None:
            return None

        try:
            if not issubclass(_type, (QDateTimeEdit, QDateEdit, QTimeEdit)):
                log.warning(f"{cls.__name__}\\__type_issubclass\\{_type} is not a supported type")
                return None
        except TypeError as e:
            log.error(f"{cls.__name__}\\__type_issubclass\\{e}")
            return None

        return _type

    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDateTime]:
        return cls.get_datetime(
            widget=widget,
            ui=ui,
            _type=QDateTimeEdit,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            datetime: QDateTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs,
    ) -> MEH[None]:
        return cls.set_datetime(
            datetime=datetime,
            widget=widget,
            ui=ui,
            _type=QDateTimeEdit,
            name=name,
        )

    @classmethod
    def get_date(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[QDate]:
        return cls.safe_widget_call(
            func=lambda x: x.date(),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )

    @classmethod
    def set_date(
            cls,
            *,
            date: QDate,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[None]:
        if not isinstance(date, QDate):
            log.warning(f"{cls.__name__}\\set_date\\value type not QDate\\{type(date).__name__=}")
            return MEH.unit_err("date type not QDate")

        return cls.safe_widget_call(
            func=lambda x: x.setDate(date),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )

    @classmethod
    def get_time(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[QTime]:
        return cls.safe_widget_call(
            func=lambda x: x.time(),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )

    @classmethod
    def set_time(
            cls,
            *,
            time: QTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[None]:
        if not isinstance(time, QTime):
            log.warning(f"{cls.__name__}\\set_time\\value type not QTime\\{type(time).__name__=}")
            return MEH.unit_err("time type not QTime")

        return cls.safe_widget_call(
            func=lambda x: x.setTime(time),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )

    @classmethod
    def get_datetime(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[QDateTime]:
        return cls.safe_widget_call(
            func=lambda x: x.dateTime(),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )

    @classmethod
    def set_datetime(
            cls,
            *,
            datetime: QDateTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            _type: type[QDateTimeEdit] | type[QDateEdit] | type[QTimeEdit] = None,
    ) -> MEH[None]:
        if not isinstance(datetime, QDateTime):
            log.warning(f"{cls.__name__}\\set_datetime\\value type not QDateTime\\{type(datetime).__name__=}")
            return MEH.unit_err("datetime type not QDateTime")

        return cls.safe_widget_call(
            func=lambda x: x.setDateTime(datetime),
            widget=widget,
            ui=ui,
            _type=cls.__type_issubclass_datetime(_type),
            name=name
        )


class UICHDateEdit(UICHDateTimeEdit):
    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDate]:
        return cls.get_date(
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            date: QDate,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs,
    ) -> MEH[None]:
        return cls.set_date(
            date=date,
            widget=widget,
            ui=ui,
            name=name,
        )

    @classmethod
    def get_date(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDate]:
        return super().get_date(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDateEdit
        )

    @classmethod
    def set_date(
            cls,
            *,
            date: QDate,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return super().set_date(
            date=date,
            widget=widget,
            ui=ui,
            name=name,
            _type=QDateEdit
        )

    @classmethod
    def get_time(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QTime]:
        log.warning(f"{cls.__name__}\\get_time\\QDateEdit generally does not handle this content")
        return super().get_time(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDateEdit
        )

    @classmethod
    def set_time(
            cls,
            *,
            time: QTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        log.warning(f"{cls.__name__}\\set_time\\QDateEdit does not handle this content")
        return super().set_time(
            widget=widget,
            ui=ui,
            name=name,
            time=time,
            _type=QDateEdit
        )

    @classmethod
    def get_datetime(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDateTime]:
        log.warning(f"{cls.__name__}\\get_datetime\\QDateEdit does not handle this content")
        return super().get_datetime(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDateEdit
        )

    @classmethod
    def set_datetime(
            cls,
            *,
            datetime: QDateTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        log.warning(f"{cls.__name__}\\set_datetime\\QDateEdit does not handle this content")
        return super().set_datetime(
            widget=widget,
            ui=ui,
            name=name,
            datetime=datetime,
            _type=QDateEdit
        )


class UICHTimeEdit(UICHDateTimeEdit):
    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QTime]:
        return cls.get_time(
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            time: QTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs,
    ) -> MEH[None]:
        return cls.set_time(
            time=time,
            widget=widget,
            ui=ui,
            name=name,
        )

    @classmethod
    def get_date(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDate]:
        log.warning(f"{cls.__name__}\\get_date\\QTimeEdit does not handle this content")
        return super().get_date(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTimeEdit
        )

    @classmethod
    def set_date(
            cls,
            *,
            date: QDate,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        log.warning(f"{cls.__name__}\\set_date\\QTimeEdit does not handle this content")
        return super().set_date(
            widget=widget,
            ui=ui,
            name=name,
            date=date,
            _type=QTimeEdit
        )

    @classmethod
    def get_time(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QTime]:
        return super().get_time(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTimeEdit
        )

    @classmethod
    def set_time(
            cls,
            *,
            time: QTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return super().set_time(
            widget=widget,
            ui=ui,
            name=name,
            time=time,
            _type=QTimeEdit
        )

    @classmethod
    def get_datetime(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[QDateTime]:
        log.warning(f"{cls.__name__}\\get_datetime\\QTimeEdit does not handle this content")
        return super().get_datetime(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTimeEdit
        )

    @classmethod
    def set_datetime(
            cls,
            *,
            datetime: QDateTime,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        log.warning(f"{cls.__name__}\\set_datetime\\QTimeEdit does not handle this content")
        return super().set_datetime(
            widget=widget,
            ui=ui,
            name=name,
            datetime=datetime,
            _type=QTimeEdit
        )


class UICHLineEdit(UICH):
    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[str]:
        return cls.get_text(
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            text: str | None = None,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return cls.set_text(
            text=text,
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def get_text(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            func=lambda x: x.text(),
            widget=widget,
            ui=ui,
            name=name,
            _type=QLineEdit
        )

    @classmethod
    def set_text(
            cls,
            *,
            text: str | None = None,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if text is None:
            text = ""
        elif not isinstance(text, str):
            log.warning(f"{cls.__name__}\\set_text\\text type not str\\{type(text).__name__=}")
            return MEH.unit_err("text type not str")

        return cls.safe_widget_call(
            func=lambda x: x.setText(text),
            widget=widget,
            ui=ui,
            _type=QLineEdit,
            name=name
        )


class UICHTextEdit(UICH):
    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[str]:
        return cls.get_text(
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            value: str | None = None,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return cls.set_text(
            text=value,
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def get_html(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.toHtml()
        )

    @classmethod
    def set_html(
            cls,
            *,
            html: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(html, str):
            log.warning(f"{cls.__name__}\\set_html\\html type not str\\{type(html).__name__=}")
            return MEH.unit_err("html type not str")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.setHtml(html)
        )

    @classmethod
    def get_markdown(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.toMarkdown()
        )

    @classmethod
    def set_markdown(
            cls,
            *,
            markdown: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(markdown, str):
            log.warning(f"{cls.__name__}\\set_html\\html type not str\\{type(markdown).__name__=}")
            return MEH.unit_err("html type not str")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.setMarkdown(markdown)
        )

    @classmethod
    def get_text(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[str]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.toPlainText()
        )

    @classmethod
    def set_text(
            cls,
            *,
            text: str,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(text, str):
            log.warning(f"{cls.__name__}\\set_text\\text type not str\\{type(text).__name__=}")
            return MEH.unit_err("text type not str")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QTextEdit,
            func=lambda x: x.setText(text)
        )


class UICHSpinBox(UICHValue):
    @classmethod
    def get_value(
            cls,
            *,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[int]:
        return super().get_value(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox,
        )

    @classmethod
    def set_value(
            cls,
            *,
            value: int,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_value\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return super().set_value(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox,
        )

    @classmethod
    def get_maximum(
            cls,
            *,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[int]:
        return super().get_maximum(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox
        )

    @classmethod
    def set_maximum(
            cls,
            *,
            value: int,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return super().set_maximum(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox
        )

    @classmethod
    def get_minimum(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[int]:
        return super().get_minimum(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox
        )

    @classmethod
    def set_minimum(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_minimum\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return super().set_minimum(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QSpinBox
        )


class UICHDoubleSpinBox(UICHValue):
    @classmethod
    def get_value(
            cls,
            *,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[float]:
        return super().get_value(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox,
        )

    @classmethod
    def set_value(
            cls,
            *,
            value: float,
            widget=None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        if not isinstance(value, float):
            log.warning(f"{cls.__name__}\\set_value\\value type not float\\{type(value).__name__=}")
            return MEH.unit_err("value type not float")

        return super().set_value(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox,
        )

    @classmethod
    def get_maximum(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[float]:
        return super().get_maximum(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox
        )

    @classmethod
    def set_maximum(
            cls,
            *,
            value: float,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return super().set_maximum(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox
        )

    @classmethod
    def get_minimum(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[float]:
        return super().get_minimum(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox
        )

    @classmethod
    def set_minimum(
            cls,
            *,
            value: float,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return super().set_minimum(
            value=value,
            widget=widget,
            ui=ui,
            name=name,
            _type=QDoubleSpinBox
        )


class UICHQDial(UICHValue):
    @classmethod
    def get_notches_visible(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[bool]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDial,
            func=lambda x: x.notchesVisible()
        )

    @classmethod
    def set_notches_visible(
            cls,
            *,
            value: bool,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, bool):
            log.warning(f"{cls.__name__}\\set_notches_visible\\value type not bool\\{type(value).__name__=}")
            return MEH.unit_err("value type not bool")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDial,
            func=lambda x: x.setNotchesVisible(value)
        )

    @classmethod
    def get_wrapping(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[bool]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=QDial,
            name=name,
            func=lambda x: x.wrapping()
        )

    @classmethod
    def set_wrapping(
            cls,
            *,
            value: bool,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, bool):
            log.warning(f"{cls.__name__}\\set_wrapping\\value type not bool\\{type(value).__name__=}")
            return MEH.unit_err("value type not bool")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            _type=QDial,
            name=name,
            func=lambda x: x.setWrapping(value)
        )

    @classmethod
    def get_notch_target(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[float]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDial,
            func=lambda x: x.notchTarget()
        )

    @classmethod
    def set_notch_target(
            cls,
            *,
            value: float,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, (int, float)):
            log.warning(f"{cls.__name__}\\set_notch_target\\value type not float\\{type(value).__name__=}")
            return MEH.unit_err("value type not float")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QDial,
            func=lambda x: x.setNotchTarget(value)
        )


class UICHQSlider(UICHValue):
    @classmethod
    def get_orientation(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[Qt.Orientation]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x: x.orientation()
        )

    @classmethod
    def set_orientation(
            cls,
            *,
            value: Qt.Orientation,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, Qt.Orientation):
            log.warning(f"{cls.__name__}\\set_orientation\\value type not Qt.Orientation\\{type(value).__name__=}")
            return MEH.unit_err("value type not Qt.Orientation")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x: x.setOrientation(value)
        )

    @classmethod
    def get_single_step(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x: x.singleStep()
        )

    @classmethod
    def set_single_step(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_single_step\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x: x.setSingleStep(value)
        )

    @classmethod
    def get_page_step(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.pageStep()
        )

    @classmethod
    def set_page_step(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_page_step\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setPageStep(value)
        )

    @classmethod
    def get_tick_interval(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.tickInterval()
        )

    @classmethod
    def set_tick_interval(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_tick_interval\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x: x.setTickInterval(value)
        )

    @classmethod
    def get_tick_position(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[QSlider.TickPosition]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.tickPosition()
        )

    @classmethod
    def set_tick_position(
            cls,
            *,
            value: QSlider.TickPosition,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, QSlider.TickPosition):
            log.warning(
                f"{cls.__name__}\\set_tick_position\\value type not QSlider.TickPosition\\{type(value).__name__=}")
            return MEH.unit_err("value type not QSlider.TickPosition")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setTickPosition(value)
        )


class UICHQScrollBar(UICHValue):
    @classmethod
    def get_single_step(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.singleStep()
        )

    @classmethod
    def set_single_step(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_single_step\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setSingleStep(value)
        )

    @classmethod
    def get_page_step(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.pageStep()
        )

    @classmethod
    def set_page_step(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_page_step\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setPageStep(value)
        )

    @classmethod
    def get_orientation(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[Qt.Orientation]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.orientation()
        )

    @classmethod
    def set_orientation(
            cls,
            *,
            value: Qt.Orientation,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, Qt.Orientation):
            log.warning(f"{cls.__name__}\\set_orientation\\value type not Qt.Orientation\\{type(value).__name__=}")
            return MEH.unit_err("value type not Qt.Orientation")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setOrientation(value)
        )

    @classmethod
    def get_slider_position(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.sliderPosition()
        )

    @classmethod
    def set_slider_position(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_slider_position\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QSlider,
            func=lambda x:x.setSliderPosition(value)
        )


class UICHQKeySequenceEdit(UICH):
    @classmethod
    def get_value(
            cls,
            *,
            widget: QWidgetType = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[Any]:
        return cls.get_key_sequence(
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def set_value(
            cls,
            *,
            value: QKeySequence | None = None,
            widget = None,
            ui: QWidget = None,
            name: str = None,
            **kwargs
    ) -> MEH[None]:
        return cls.set_key_sequence(
            value=value,
            widget=widget,
            ui=ui,
            name=name
        )

    @classmethod
    def get_key_sequence(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[QKeySequence]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.keySequence()
        )

    @classmethod
    def set_key_sequence(
            cls,
            *,
            value: QKeySequence | None = None,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if value is None:
            return cls.clear(widget=widget, ui=ui, name=name)
        elif not isinstance(value, QKeySequence):
            log.warning(f"{cls.__name__}\\set_key_sequence\\value type not QKeySequence\\{type(value).__name__=}")
            return MEH.unit_err("value type not QKeySequence")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.setKeySequence(value)
        )

    @classmethod
    def clear(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.clear()
        )

    @classmethod
    def get_maximum_sequence_length(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[int]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.maximumSequenceLength()
        )

    @classmethod
    def set_maximum_sequence_length(
            cls,
            *,
            value: int,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, int):
            log.warning(f"{cls.__name__}\\set_maximum_sequence_length\\value type not int\\{type(value).__name__=}")
            return MEH.unit_err("value type not int")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.setMaximumSequenceLength(value)
        )

    @classmethod
    def is_clear_button_enabled(
            cls,
            *,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[bool]:
        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.isClearButtonEnabled()
        )

    @classmethod
    def set_clear_button_enabled(
            cls,
            *,
            value: bool,
            widget = None,
            ui: QWidget = None,
            name: str = None,
    ) -> MEH[None]:
        if not isinstance(value, bool):
            log.warning(f"{cls.__name__}\\set_clear_button_enabled\\value type not bool\\{type(value).__name__=}")
            return MEH.unit_err("value type not bool")

        return cls.safe_widget_call(
            widget=widget,
            ui=ui,
            name=name,
            _type=QKeySequenceEdit,
            func=lambda x:x.setClearButtonEnabled(value)
        )
