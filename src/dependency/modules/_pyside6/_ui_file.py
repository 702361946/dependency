#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
"""
用于QT ui文件加载转化等
"""
from pathlib import Path

from config import log, Log, work_directory
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from modules._file_operations import PathTools


class UiFile:
    def __init__(
            self,
            file_save_path: str = "ui",
            _log: Log = log
    ):
        """

        :param file_save_path: ui文件存储位置
        """
        fsp = PathTools.join_paths(work_directory, file_save_path)
        if fsp:
            self.file_save_path = fsp.v
        else:
            self.file_save_path = PathTools.str_to_path(".").v

        self._log = _log

    def load(
            self,
            file_name: str,
            file_paths: list[str | Path] | str | Path | None = None
    ) -> QWidget | None:
        """

        :param file_name: 文件名,无需带.ui后缀,可补全
        :param file_paths: {self.file_save_path}与ui文件所间隔的文件夹
        :return:
        """
        if file_paths is None:
            file_paths = []
        elif not isinstance(file_paths, list):
            file_paths = [file_paths]

        if not file_name.lower().endswith(".ui"):
            file_name += ".ui"

        file_path = PathTools.join_paths(
            self.file_save_path,
            *file_paths,
            file_name
        )
        if not file_path:
            return None

        # load部分
        log.info(f"load {file_path}")
        ui_file = QFile(file_path.v)
        try:
            ui = None
            if ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
                ui = QUiLoader().load(ui_file)
        except Exception as e:
            log.error(e)
            ui = None
        finally:
            ui_file.close()

        return ui
