#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
"""
用于QT ui文件加载转化等
"""
import os

from .config import log
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from modules._error_handling import MEH


class UiFile:
    _uiloader: QUiLoader = None
    @classmethod
    def _get_uiloader(cls) -> QUiLoader:
        if not cls._uiloader:
            cls._uiloader = QUiLoader()

        return cls._uiloader

    @classmethod
    def load(
            cls,
            file_path: str,
            add_file_ext: bool = True,
            parent: QWidget | None = None
    ) -> MEH[QWidget]:
        """

        :param file_path: 必须是绝对路径,除非能保证相对路径是正确的
        :param add_file_ext:
        :param parent:
        :return:
        """
        if not file_path.lower().endswith(".ui") and add_file_ext:
            file_path += ".ui"

        if not os.path.isfile(file_path):
            return MEH.unit_err("file not exist")

        ui_file = QFile(file_path)
        try:
            ui = None
            if ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
                ui = cls._get_uiloader().load(ui_file, parentWidget=parent)
        except Exception as e:
            log.error(e)
            ui = None
        finally:
            ui_file.close()

        if ui is None:
            return MEH.unit_err(f"load ui file Error")

        return MEH.unit_ok(ui)
