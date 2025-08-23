#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
"""
用于QT ui文件加载转化等
"""
from _get_package import *
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

log = Log(
    log_sign="ui_file",
    log_output_to_file_path=f"{log_path}pyside6"
)


class UiFile:
    def __init__(
            self,
            file_save_path: str = "ui",
            log: Log = log
    ):
        """

        :param file_save_path: ui文件存储位置
        """
        self.file_save_path = os.path.join(work_directory, file_save_path)

    def load(
            self,
            file_name: str,
            file_paths: list[str] | str | None = None
    ) -> QWidget | None:
        """

        :param file_name: 文件名,无需带.ui后缀
        :param file_paths: {self.file_save_path}与ui文件所间隔的文件夹
        :return:
        """
        if file_paths is None:
            file_paths = []

        elif not isinstance(file_paths, list):
            file_paths = [file_paths]

        file_path = self.file_save_path
        for i in file_paths:
            file_path = os.path.join(file_path, i)

        file_path = os.path.join(file_path, file_name)

        if not file_path.lower().endswith(".ui"):
            file_path += ".ui"

        # load部分
        log.info(f"load {file_path}")
        ui_file = QFile(file_path)
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

    def ui_file_to_python_file(
            self,
            file_name: str,
            file_paths: list[str] | str | None = None
    ) -> str | None:
        """
        使用 self.load 加载 .ui 并生成等价的 Python 类源码字符串。
        失败时返回 None。

        注意!!!
        这个函数纯粹使用AI生成,不保证可用以及结果!!!
        同时两个参数同self.load
        """
        ui = self.load(file_name, file_paths)
        if ui is None:
            return None

        import keyword
        import re
        from collections import deque
        from pathlib import Path

        # 1. 提取纯文件名主干（不含目录、不含扩展）
        pure_stem = Path(file_name).stem

        # 2. 将 snake_case / kebab-case 转 PascalCase
        pascal = "".join(
            word.capitalize()
            for word in re.split(r"[-_]+", pure_stem)
        )

        # 3. 处理关键字冲突
        cls_name = f"{pascal}_" if keyword.iskeyword(pascal) else pascal

        # 4. 生成源码
        lines = [
            f"class {cls_name}(QWidget):",
            "    def __init__(self, parent=None):",
            "        super().__init__(parent)"
        ]

        queue = deque([(ui.objectName() or "centralWidget", ui)])
        while queue:
            name, obj = queue.popleft()
            if name and name != "centralWidget":
                lines.append(
                    f"        self.{name} = "
                    f"self.findChild({obj.__class__.__name__}, '{name}')"
                )
            for child in obj.findChildren(QWidget):
                if child.objectName():
                    queue.append((child.objectName(), child))

        return "\n".join(lines)
