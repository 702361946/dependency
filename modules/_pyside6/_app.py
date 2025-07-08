#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import os.path

from PySide6.QtCore import QTranslator

from ._get_package import *
from PySide6.QtWidgets import QApplication

log = Log(
    log_sign="app",
    log_output_to_file_path=f"{log_path}pyside6"
)


class App:
    def __init__(
            self,
            language: str = "zh_CN",
            translator: QTranslator | None = None,
            *,
            log: LogProtocol = log
    ):
        self.log = log

        app = QApplication(sys.argv)
        self.app = app

        self.language = language

        if isinstance(translator, QTranslator):
            self.translator = translator
        else:
            self.translator = QTranslator()

        if not self.translator.load(f"{os.path.join(os.path.join('.', 'language'), language)}.qm"):
            log.error("translator load ERROR")
        else:
            self.app.installTranslator(self.translator)

    def close_all_windows(self):
        self.app.closeAllWindows()
        self.log.info("close all windows -- ok")

    def set_language(self, language: str):
        """
        设置窗口语言

        不知道有没有问题
        :param language: qm文件名,存放于language文件夹下
        """
        self.app.removeTranslator(self.translator)

        if self.translator.load(f"{os.path.join(os.path.join('.', 'language'), language)}.qm"):
            self.app.installTranslator(self.translator)
            self.language = language
            self.log.info(f"Language set to {language}")
        else:
            self.log.error(f"Failed to load translation file for {language}")
            self.translator.load(f"{os.path.join(os.path.join('.', 'language'), language)}.qm")
            self.app.installTranslator(self.translator)
