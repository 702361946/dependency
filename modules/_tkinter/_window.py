#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

import tkinter as tk

from ._get_package import *

log = Log(
    "tkinter",
    log_output_to_file_path=f"{log_path}tkinter.log"
)


class Window:
    def __init__(
            self,
            title: str = "MainWindow",
            geometry: str = "100x100",
            resizable: tuple[bool, bool] = (False, False),
            main_window: tk.Tk | None = None,
            log: Log = log
    ):
        """
        创建窗口
        :param title: 窗口标题
        :param geometry: 窗口大小
        :param resizable: 窗口是否可缩放(x,y)
        :param main_window: 主窗口,若为None则创建主窗口,否则创建子窗口
        """
        log.info("__init__, Window")
        if main_window is None:
            self.window = tk.Tk()
            log.info("sign window")
        else:
            self.window = tk.Toplevel(main_window)
            # 关闭主窗口时同步关闭子窗口
            main_window.protocol(
                "WM_DELETE_WINDOW",
                self.window.destroy()
            )
            log.info("sign sub window")

        log.info(f"title:{title}")
        log.info(f"geometry:{geometry}")
        log.info(f"resizable:{resizable}")

        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(resizable[0], resizable[1])

        self.info = {
            "title": title,
            "geometry": geometry,
            "resizable": resizable,
            "main_window": main_window,
            "log": log
        }

    def modify_window_title(self, title: str):
        """
        修改窗口标题,要求未运行
        :param title: 窗口标题
        :return:
        """
        log.info(f"modify window title: {title}")
        self.window.title(title)
        self.info["title"] = title

    def modify_window_geometry(self, geometry: str):
        """
        修改窗口大小,要求未运行
        :param geometry: 窗口大小
        :return:
        """
        log.info(f"modify window geometry: {geometry}")
        self.window.geometry(geometry)
        self.info["geometry"] = geometry

    def modify_window_resizable(self, resizable: tuple[bool, bool]):
        """
        修改窗口是否可缩放,要求未运行
        :param resizable: 窗口是否可缩放(x,y)
        :return:
        """
        log.info(f"modify window resizable: {resizable}")
        self.window.resizable(resizable[0], resizable[1])
        self.info["resizable"] = resizable

    def close(self):
        """
        关闭窗口
        :return:
        """
        self.window.destroy()
        log.info(f"close window: {self.window.title}")

    def withdraw(self):
        """
        隐藏窗口
        :return:
        """
        self.window.withdraw()
        log.info(f"withdraw window: {self.window.title}")

    def deiconify(self):
        """
        显示窗口
        :return:
        """
        self.window.deiconify()
        log.info(f"deiconify window: {self.window.title}")

    def run(self):
        """
        运行窗口
        :return:
        """
        log.info(f"run window: {self.info['title']}")
        self.window.mainloop()
