#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._get_package import *
from PySide6.QtWidgets import QApplication

log = Log(
    log_sign="app",
    log_output_to_file_path=f"{log_path}pyside6"
)


class App:
    def __init__(
            self,
            *,
            log: Log = log
    ):
        app = QApplication(sys.argv)
        self.app = app
        self.log = log

    def close_all_windows(self):
        self.app.closeAllWindows()
        self.log.info("close all windows -- ok")

    def set_language(self, lang: str):
        """
        设置窗口语言

        等待制作
        """
