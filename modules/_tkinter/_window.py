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
        self.log = log

        self.log.info("add Window\n")

        if main_window is None:
            self.window = tk.Tk()
            self.log.info("sign: window")
        else:
            self.window = tk.Toplevel(main_window)
            # 关闭主窗口时同步关闭子窗口
            main_window.protocol(
                "WM_DELETE_WINDOW",
                self.window.destroy()
            )
            self.log.info("sign: sub window")

        self.log.info(f"title:{title}")
        self.log.info(f"geometry:{geometry}")
        self.log.info(f"resizable:{resizable}")

        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(resizable[0], resizable[1])

        self.info = {
            "title": title,
            "geometry": geometry,
            "resizable": resizable,
            "main_window": main_window,
            "log": self.log
        }

        self.buttons: dict[str, dict] = {}
        self.messages: dict[str, dict] = {}
        self.entrys: dict[str, dict] = {}

        self.log.info("add window ok\n")

    def modify_window_title(self, title: str):
        """
        修改窗口标题,要求未运行
        :param title: 窗口标题
        :return:
        """
        self.log.info(f"modify window title: {title}")
        self.window.title(title)
        self.info["title"] = title

    def modify_window_geometry(self, geometry: str):
        """
        修改窗口大小,要求未运行
        :param geometry: 窗口大小
        :return:
        """
        self.log.info(f"modify window geometry: {geometry}")
        self.window.geometry(geometry)
        self.info["geometry"] = geometry

    def modify_window_resizable(self, resizable: tuple[bool, bool]):
        """
        修改窗口是否可缩放,要求未运行
        :param resizable: 窗口是否可缩放(x,y)
        :return:
        """
        self.log.info(f"modify window resizable: {resizable}")
        self.window.resizable(resizable[0], resizable[1])
        self.info["resizable"] = resizable

    def close(self):
        """
        关闭窗口
        :return:
        """
        self.window.destroy()
        self.log.info(f"close window: {self.info["title"]}")

    def withdraw(self):
        """
        隐藏窗口
        :return:
        """
        self.window.withdraw()
        self.log.info(f"withdraw window: {self.info["title"]}")

    def deiconify(self):
        """
        显示窗口
        :return:
        """
        self.window.deiconify()
        self.log.info(f"deiconify window: {self.info["title"]}")

    def run(
            self,
            pack_button: bool = True,
            pack_message: bool = True,
            pack_entry: bool = True,
    ):
        """
        运行窗口
        :return:
        """
        self.log.info(f"run window: {self.info['title']}")

        if pack_button:
            for i in self.buttons.keys():
                if self.buttons[i]["pack"]["pack"]:
                    match self.buttons[i]["pack"]["mode"]:
                        case "pack":
                            self.buttons[i]["button"].pack()
                            self.log.info(f"pack button:{i}")
                        case "grid":
                            self.buttons[i]["button"].grid()
                            self.log.info(f"grid button:{i}")
                        case "place":
                            self.buttons[i]["button"].place(
                                x=self.buttons[i]["pack"]["x"],
                                y=self.buttons[i]["pack"]["y"]
                            )
                            self.log.info(f"place button:{i}")
                        case _:
                            self.log.error(f"pack_mode error: {self.buttons[i]['pack']['mode']}")
                            raise ValueError(f"pack_mode error: {self.buttons[i]['pack']['mode']}")

        if pack_message:
            for i in self.messages.keys():
                if self.messages[i]["pack"]["pack"]:
                    match self.messages[i]["pack"]["mode"]:
                        case "pack":
                            self.messages[i]["message"].pack()
                            self.log.info(f"pack message:{i}")
                        case "grid":
                            self.messages[i]["message"].grid()
                            self.log.info(f"grid message:{i}")
                        case "place":
                            self.messages[i]["message"].place(
                                x=self.messages[i]["pack"]["x"],
                                y=self.messages[i]["pack"]["y"]
                            )
                        case _:
                            self.log.error(f"pack_mode error: {self.messages[i]['pack']['mode']}")
                            raise ValueError(f"pack_mode error: {self.messages[i]['pack']['mode']}")

        if pack_entry:
            for i in self.entrys.keys():
                if self.entrys[i]["pack"]["pack"]:
                    match self.entrys[i]["pack"]["mode"]:
                        case "pack":
                            self.entrys[i]["entry"].pack()
                            self.log.info(f"pack entry:{i}")
                        case "grid":
                            self.entrys[i]["entry"].grid()
                            self.log.info(f"grid entry:{i}")
                        case "place":
                            self.entrys[i]["entry"].place(
                                x=self.entrys[i]["pack"]["x"],
                                y=self.entrys[i]["pack"]["y"]
                            )
                            self.log.info(f"place entry:{i}")
                        case _:
                            self.log.error(f"pack_mode error: {self.entrys[i]['pack']['mode']}")
                            raise ValueError(f"pack_mode error: {self.entrys[i]['pack']['mode']}")

        self.window.mainloop()

    def button(
            self,
            name: str,
            text: str | None = None,
            command=None,
            x: int = 0,
            y: int = 0,
            w: int = None,
            h: int = None,
            pack_if: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name: 按钮名称
        :param text: 按钮文本
        :param command: function(函数)
        :param x:
        :param y:
        :param w:
        :param h:
        :param pack_if: 是否部署按钮
        :param pack_mode: 部署方法,pack,grid,place
        :return:
        """
        self.log.info(f"button: {name}")

        if name in self.buttons.keys():
            self.log.warning("name in keys")
            t = input("name in keys, replace?(y/n)")
            if t != "y":
                return

        if pack_mode not in ['pack', 'grid', 'place']:
            self.log.error(f"pack_mode error: {pack_mode}")
            raise ValueError(f"pack_mode error: {pack_mode}")

        self.buttons[name] = {
            "button": tk.Button(
                self.window,
                text=text,
                command=command,
                width=w,
                height=h
            ),
            "pack": {
                "x": x,
                "y": y,
                "pack": bool(pack_if),
                "mode": pack_mode
            }
        }

        self.log.info(f"button {name} ok")

    def message(
            self,
            name: str,
            message: str,
            x: int = 0,
            y: int = 0,
            w: int = 100,
            pack_if: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name: 消息名称
        :param message: 文本
        :param w: 宽度
        :param x:
        :param y:
        :param pack_if: 是否部署消息
        :param pack_mode: 部署方法,pack,grid,place
        :return:
        """
        self.log.info(f"message: {message}")
        if name in self.messages.keys():
            self.log.warning("name in keys")
            t = input("name in keys, replace?(y/n)")
            if t != "y":
                return

        if pack_mode not in ['pack', 'grid', 'place']:
            self.log.error(f"pack_mode error: {pack_mode}")
            raise ValueError(f"pack_mode error: {pack_mode}")

        self.messages[name] = {
            "message": tk.Message(
                self.window,
                text=message,
                width=w
            ),
            "pack": {
                "x": x,
                "y": y,
                "pack": bool(pack_if),
                "mode": pack_mode
            }
        }

        self.log.info(f'message {name} ok')

    def entry(
            self,
            name: str,
            default_text: str = None,
            x: int = 0,
            y: int = 0,
            w: int = 100,
            pack_if: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name:
        :param default_text: 默认文本
        :param x:
        :param y:
        :param w:
        :param pack_if:
        :param pack_mode:
        :return:
        """
        self.log.info(f'default_text: {default_text}')

        if name in self.entrys.keys():
            self.log.warning("name in keys")
            t = input("name in keys, replace?(y/n)")
            if t!= "y":
                return

        if pack_mode not in ['pack', 'grid', 'place']:
            self.log.error(f"pack_mode error: {pack_mode}")

        entry = tk.Entry(
            self.window,
            width=w
        )

        if default_text:
            # noinspection PyUnusedLocal
            def set_default_text(event=None):
                """当输入框失去焦点且为空时，设置默认文本"""
                if not entry.get():
                    entry.insert(0, default_text)

            # noinspection PyUnusedLocal
            def clear_default_text(event=None):
                """当输入框获得焦点且有默认文本时，清除文本"""
                if entry.get() == default_text:
                    entry.delete(0, tk.END)

            # 默认文本
            entry.insert(0, default_text)

            # 绑定焦点事件
            entry.bind("<FocusIn>", clear_default_text)
            entry.bind("<FocusOut>", set_default_text)

        self.entrys[name] = {
            "entry": entry,
            "pack": {
                "x": x,
                "y": y,
                "pack": bool(pack_if),
                "mode": pack_mode
            }
        }

        self.log.info(f'entry {name} ok')
