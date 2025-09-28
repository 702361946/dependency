#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._app import *
from types import FunctionType
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

log = Log(
    log_sign="window",
    log_output_to_file_path=f"{log_path}pyside6.log",
)


class Window:
    def __init__(
            self,
            title: str = "MainWindow",
            size: tuple[int, int] = (1280, 720),
            icon: QIcon | None | str = None,
            opacity: float = 1.0,
            window_close_callback_function: FunctionType | None = None,
            *,
            log: Log = log
    ):
        """
        请先创立一个app实例,否则窗口将无法显示也无法创立

        :param title: 窗口标题
        :param size: 窗口大小(h, w)
        :param icon: 窗口图标,要求为QIcon对象或路径
        :param opacity: 窗口透明度,0~1的小数
        :param window_close_callback_function: 窗口关闭回调函数
        :param log: 日志
        """
        self.log = log
        self.log.info(
            "init window\n"
            f"{title=}\n"
            f"{size=}\n"
            f"{icon=}\n"
            f"{opacity=}"
        )

        # 建立实例
        window = QMainWindow()

        # 窗口标题
        window.setWindowTitle(title)

        # 窗口大小
        window.resize(size[0], size[1])

        # 窗口透明度
        window.setWindowOpacity(opacity)

        # 窗口图标
        if icon is not None:
            if isinstance(icon, str):
                icon = QIcon(icon)

            if isinstance(icon, QIcon):
                window.setWindowIcon(icon)
            else:
                self.log.error("icon type not QIcon")

        self.window = window
        self.window_close_cf = window_close_callback_function

        self.log.info("Window init ok")

    # 窗口设置部分
    def set_title(self, title: str):
        """
        设置窗口标题
        :param title:
        :return:
        """
        self.log.info(f"window title -> {title}")
        self.window.setWindowTitle(title)

    def set_size(self, size: tuple[int, int]):
        """
        设置窗口大小
        :param size: w, h
        :return:
        """
        self.log.info(f"window size -> {size}")
        self.window.resize(size[0], size[1])

    def set_icon(self, icon: QIcon | str):
        """
        设置窗口图标
        :param icon: 路径或QIcon对象
        :return:
        """
        self.log.info(f"window icon -> {icon}")
        if isinstance(icon, str):
            icon = QIcon(icon)

        if isinstance(icon, QIcon):
            self.window.setWindowIcon(icon)
        else:
            self.log.error("icon type not QIcon")

    def set_opacity(self, opacity: float):
        """
        设置窗口透明度
        :param opacity: 透明度值，范围为0.0到1.0
        :return:
        """
        self.log.info(f"window opacity -> {opacity}")
        if 0.0 <= opacity <= 1.0:
            self.window.setWindowOpacity(opacity)
        else:
            self.log.error("Opacity must be between 0.0 and 1.0")

    # 窗口操作
    def max_window(self):
        """
        最大化窗口
        """
        self.log.info("show max window")
        self.window.showMaximized()

    def min_window(self):
        """
        最小化窗口
        """
        self.log.info("show min window")
        self.window.showMinimized()

    def restore_window(self):
        """
        恢复窗口大小
        """
        self.log.info("show restore window")
        self.window.showNormal()

    def full_screen_window(self):
        """
        全屏化窗口
        """
        self.log.info("show full screen window")
        self.window.showFullScreen()

    def show_window(self):
        """
        显示窗口
        :return:
        """
        self.log.info("show window")
        self.window.show()

    def close_window(self):
        """
        关闭窗口
        :return:
        """
        self.log.info("close window")
        self.window.close()
        if self.window_close_cf is not None:
            self.window_close_cf()

    # 窗口组件
    def add_status_bar_message(self, info: str):
        """
        添加栏状态(左下角)

        有待完善
        """
        self.log.info(f"status bar message:{info}")
        self.window.statusBar().showMessage(info)
