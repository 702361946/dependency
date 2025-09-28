#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
from typing import Protocol, Any, Literal

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QIcon, QCursor, QPixmap, QFont, QPalette, QColor
from PySide6.QtWidgets import QPushButton, QWidget, QSizePolicy, QLayout, QMessageBox

from _get_package import *

log = Log(
    log_sign="component",
    log_output_to_file_path=f"{log_path}pyside6"
)


# 协议类
class ComponentProtocol(Protocol):
    def __init__(
            self,
            *,
            log: Log
    ):
        self.component: Any
        self.log: Log
        ...

    def get(self) -> Any:
        ...

    def set(self) -> bool:
        ...


# 基类
class Widget(QWidget):
    def __init__(self, parent: QWidget | None = None, *, log: Log = log) -> None:
        super().__init__(parent)
        self.log = log
        self.component = self

    def set_geometry(
            self,
            rect: QRect | tuple[int, int, int, int]
    ) -> bool:
        """

        :param rect:
        :return:
        """
        if not isinstance(rect, QRect) and not isinstance(rect, tuple):
            self.log.error("rect type not QRect or tuple")
            return False

        if isinstance(rect, tuple):
            if len(rect) != 4:
                self.log.error("rect len != 4")
                return False
            rect = QRect(rect[0], rect[1], rect[2], rect[3])

        self.component.setGeometry(rect)
        return True

    def set_fixed_size(
            self,
            size: QSize | tuple[int, int]
    ) -> bool:
        """

        :param size:
        :return:
        """
        if not isinstance(size, QSize) and not isinstance(size, tuple):
            self.log.error("size type not QSize or tuple")
            return False

        if isinstance(size, tuple):
            if len(size) != 2:
                self.log.error("size len != 2")
                return False

        self.component.setFixedSize(size)
        return True

    def set_size_policy(
            self,
            size_policy: QSizePolicy | tuple[QSizePolicy.Policy, QSizePolicy.Policy]
    ) -> bool:
        """

        :param size_policy:
        :return:
        """
        if not isinstance(size_policy, QSizePolicy) and not isinstance(size_policy, tuple):
            self.log.error("size_policy type not QSizePolicy or tuple")
            return False

        if isinstance(size_policy, tuple):
            if len(size_policy) != 2:
                self.log.error("size_policy len != 2")
                return False
            size_policy = QSizePolicy(size_policy[0], size_policy[1])

        self.component.setSizePolicy(size_policy)
        return True

    def set_style_sheet(self, sheet: str) -> bool:
        """

        :param sheet:
        :return:
        """
        if not isinstance(sheet, str):
            self.log.error("sheet type not str")
            return False

        self.component.setStyleSheet(sheet)
        return True

    def set_cursor(self, cursor: QCursor | Qt.CursorShape | QPixmap) -> bool:
        """

        :param cursor:
        :return:
        """
        if (
                not isinstance(cursor, QCursor) and
                not isinstance(cursor, Qt.CursorShape) and
                not isinstance(cursor, QPixmap)
        ):
            self.log.error("cursor type not QCursor or Qt.CursorShape or QPixmap")
            return False

        if not isinstance(cursor, QCursor):
            cursor = QCursor(cursor)

        self.component.setCursor(cursor)
        return True

    def set_focus(self, focus: bool = True) -> bool:
        """

        :param focus:
        :return:
        """
        if focus:
            self.component.setFocus()
        else:
            self.component.clearFocus()

        return True

    def set_font(self, font: str | QFont) -> bool:
        """

        :param font:
        :return:
        """
        if (
                not isinstance(font, QFont) and
                not isinstance(font, str)
        ):
            self.log.error("font type not QFont or str or Sequence['str']")
            return False

        if not isinstance(font, QFont):
            font = QFont(font)

        self.component.setFont(font)
        return True

    def set_palette(self, palette: QPalette | Qt.GlobalColor | QColor) -> bool:
        """

        :param palette:
        :return:
        """
        if (
                not isinstance(palette, QPalette) and
                not isinstance(palette, Qt.GlobalColor) and
                not isinstance(palette, QColor)
        ):
            self.log.error("palette type not QPalette or Qt.GlobalColor or QColor")
            return False

        if not isinstance(palette, QPalette):
            palette = QPalette(palette)

        self.component.setPalette(palette)
        return True

    def set_layout(self, layout: QLayout) -> bool:
        """

        :param layout:
        :return:
        """
        if not isinstance(layout, QLayout):
            self.log.error("layout type not QLayout")
            return False

        if layout.parent() is None:
            self.log.error("layout.parent is None")
            return False

        self.component.setLayout(layout)
        return True

    def set_enabled(self, enabled: bool) -> bool:
        """

        :param enabled:
        :return:
        """
        enabled = bool(enabled)
        self.component.setEnabled(enabled)
        return True

    def set_visible(self, visible: bool) -> bool:
        """

        :param visible:
        :return:
        """
        visible = bool(visible)
        self.component.setVisible(visible)
        return True

    def set_tooltip(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception as e:
                self.log.error(f"text type not str and Cannot convert to str type\\{e}")
                return False
        self.component.setToolTip(text)
        return True

    def set_status_tip(self, text: str) -> bool:
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception as e:
                self.log.error(f"text type not str and Cannot convert to str type\\{e}")
                return False

        self.component.setStatusTip(text)
        return True

    def set_minimum_size(self, size: QSize | tuple[int, int]) -> bool:
        """

        :param size:
        :return:
        """
        if isinstance(size, tuple):
            if len(size) != 2:
                self.log.error("minimum_size tuple len != 2")
                return False
            size = QSize(size[0], size[1])
        self.component.setMinimumSize(size)
        return True

    def set_maximum_size(self, size: QSize | tuple[int, int]) -> bool:
        """

        :param size:
        :return:
        """
        if isinstance(size, tuple):
            if len(size) != 2:
                self.log.error("maximum_size tuple len != 2")
                return False
            size = QSize(size[0], size[1])
        self.component.setMaximumSize(size)
        return True


class Button(Widget):
    def __init__(
            self,
            parent: QWidget,
            text: str = "",
            icon: QIcon | None = None,
            *,
            log: Log = log
    ):
        """

        :param parent: 必须给的参,没有必引发ERROR
        :param text:
        :param icon: QIcon类
        :param log:
        """
        if not isinstance(parent, QWidget):
            log.error("parent value type not QWidget")
            raise TypeError("parent value type not QWidget")
        super().__init__(parent)
        self.log = log

        if icon is None:
            self.component = QPushButton(text, parent)
        else:
            self.component = QPushButton(icon, text, parent)

    def get(
            self,
            content: Literal[
                "text",
                "icon",
                "enabled",
                "visible"
            ] = "text"
    ):
        """

        :param content: .{content}
        :return:
        """
        match content:
            case "text":
                return self.component.text()
            case "icon":
                return self.component.icon()
            case "enabled":
                return self.component.isEnabled()
            case "visible" | "showing":
                return self.component.isVisible()
            case _:
                self.log.error(f"no content\\{content=}\\Button\\get")
                raise ValueError(f"no content\\{content=}")

    def set(
            self,
            content: Literal[
                "text",
                'icon',
                'icon_size',
                'checked',
                'checkable',
                'auto_repeat',
                'auto_repeat_delay',
                'auto_repeat_interval',
                'default',
                'auto_default',
                'flat',
                'menu'
            ] = "text",
            value: Any = None
    ) -> bool:
        """
        肯定有没收录的东西
        :param content:
        :param value:
        :return:
        """
        try:
            match content:
                case "text":
                    self.component.setText(value)
                case "icon":
                    self.component.setIcon(value)
                case "icon_size":
                    self.component.setIconSize(value)
                case "checked":
                    self.component.setChecked(value)
                case "checkable":
                    self.component.setCheckable(value)
                case "auto_repeat":
                    self.component.setAutoRepeat(value)
                case "auto_repeat_delay":
                    self.component.setAutoRepeatDelay(value)
                case "auto_repeat_interval":
                    self.component.setAutoRepeatInterval(value)
                case "default":
                    self.component.setDefault(value)
                case "auto_default":
                    self.component.setAutoDefault(value)
                case "flat":
                    self.component.setFlat(value)
                case "menu":
                    self.component.setMenu(value)
                case _:
                    self.log.error(f"no content\\{content=}\\Button\\set")
                    raise ValueError(f"no content\\{content=}")

            return True
        except Exception as e:
            self.log.error(e)
            return False

    def clicked(self):
        return self.component.clicked


class Message(Widget):
    """
    还不完整
    """
    def __init__(
        self,
        parent: QWidget | None = None,
        text: str = "",
        icon: QIcon | None = None,
        *,
        log: Log = log,
    ) -> None:
        """
        信息展示标签
        :param parent: 父对象
        :param text: 文本
        :param icon: 图标
        :param log:
        """
        super().__init__(parent)
        self.component: QMessageBox = QMessageBox(parent=parent, text=text, icon=icon)

    def get(
        self,
        content: Literal[
            "text",
            "enabled",
            "visible",
        ] = "text",
    ) -> str | QPixmap | bool:
        match content:
            case "text":
                return self.component.text()
            case "enabled":
                return self.component.isEnabled()
            case "visible":
                return self.component.isVisible()
            case _:
                self.log.error(f"no content\\{content=}\\Message\\get")
                raise ValueError(f"no content\\{content=}")

    def set(
        self,
        content: Literal[
            "text",
            "enabled",
            "visible",
        ] = "text",
        value: Any = None,
    ) -> bool:
        """
        统一设置接口
        """
        try:
            match content:
                case "text":
                    self.component.setText(value)
                case "enabled":
                    self.component.setEnabled(bool(value))
                case "visible":
                    self.component.setVisible(bool(value))
                case _:
                    self.log.error(f"no content\\{content=}\\Message\\set")
                    raise ValueError(f"no content\\{content=}")
            return True
        except Exception as e:
            self.log.error(e)
            return False
