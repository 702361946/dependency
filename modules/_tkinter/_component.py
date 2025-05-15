#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._window import *

log = Log(
    log_sign="tk_component",
    log_output_to_file_path=f"{log_path}tkinter.log",
    log_output_to_file_mode="a"
)

class TKComponent:
    """
    组件框架
    创建一个组件框架, 并将组件放入其中
    基于tk.Frame
    """
    def __init__(
            self,
            window: Window,
            frame_rige: tuple[int, int, int, int] = (0, 0, 100, 100),
            frame_pack_mode: str = 'pack',
            *,
            log: Log = log
    ):
        """
        初始化组件框架
        :param window: Window类对象
        :param frame_rige: Frame的位置和大小, 格式为(x, y, width, height)
        :param frame_pack_mode: 部署方法,pack,grid,place, 当为place时,将根据rige[0],[1]来确定
        :param log:
        """
        self.log = log
        self.log.info(f"TK Component frame: {frame_rige}")

        if not isinstance(window, Window):
            self.log.error("window type not Window")
            raise TypeError("参数必须是一个Window类对象")

        self.window = window.window
        self.frame = {
            "frame": tk.Frame(
                window.window,
                width=frame_rige[2],
                height=frame_rige[3]
            ),
            "pack": {
                "mode": frame_pack_mode,
                "x": frame_rige[0],
                "y": frame_rige[1],
            }
        }  # 创建Frame

        self.components = {}  # 组件表
        """
        {
            "name": {
                "type": str,
                "Component": "tk.xxx",
                "pack": {
                    "mode": str,
                    "x": int,
                    "y": int,
                    "open": bool,
                }
            }
        }
        """

    def deploy(self):
        """
        整体部署
        :return:
        """
        self.log.info("Deploy")
        self.deploy_component()
        self.deploy_frame()

    def deploy_frame(self):
        """
        部署Frame
        """
        self.log.info("Frame deploy")

        match self.frame["pack"]["mode"]:
            case 'pack':
                self.frame["frame"].pack()
            case 'grid':
                self.frame["frame"].grid()
            case 'place':
                self.frame["frame"].place(
                    x=self.frame["pack"]["x"],
                    y=self.frame["pack"]["y"]
                )

    def deploy_component(self):
        """
        部署组件

        :return:
        """
        self.log.info("Component deploy")

        for k in self.components.keys():
            if self.components[k]["pack"]["open"] is False:
                continue

            match self.components[k]["pack"]["mode"]:
                case 'pack':
                    self.components[k]["Component"].pack()
                case 'grid':
                    self.components[k]["Component"].grid()
                case 'place':
                    self.components[k]["Component"].place(
                        x=self.components[k]["pack"]["x"],
                        y=self.components[k]["pack"]["y"]
                    )

    def check_name_and_mode(self, name: str = None, mode: str = None):
        """

        :param name:
        :param mode:
        :return:
        """
        t = [False,False]
        self.log.info(f"Check name: {name} and mode: {mode}")
        if name not in self.components.keys() and name is not None:
            t[0] = True
        if mode in ["pack", "grid", "place"] and mode is not None:
            t[1] = True
        return tuple(t)

    def add_component(
            self,
            name: str,
            component,
            pack_open: bool = True,
            pack_mode: str = 'pack',
            pack_x: int = 0,
            pack_y: int = 0,
    ):
        """

        :param name:
        :param component:
        :param pack_open:
        :param pack_mode:
        :param pack_x:
        :param pack_y:
        :return:
        """
        self.log.info(f"Add component: {name}")

        self.components[name] = {
            "type": type(component).__name__,
            "Component": component,
            "pack": {
                "mode": pack_mode,
                "x": pack_x,
                "y": pack_y,
                "open": pack_open,
            }
        }

    def get_component(self, name: str):
        """

        :param name:
        :return: tk组件
        """
        self.log.info(f"Get component: {name}")
        return self.components.get(
            name,
            {'Component': False}
        )["Component"]

    def button(
            self,
            name: str,
            text: str | None = None,
            command=None,
            x: int = 0,
            y: int = 0,
            w: int = None,
            h: int = None,
            pack_open: bool = True,
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
        :param pack_open: 是否部署按钮
        :param pack_mode: 部署方法,pack,grid,place
        :return:
        """
        self.log.info(f"button: {name}")

        if self.check_name_and_mode(name, pack_mode) != (True, True):
            self.log.error(f"name: {name} or mode: {pack_mode} is exist")
            raise ValueError("名字存在或/和部署方法错误")

        self.add_component(
            name,
            tk.Button(
                self.frame["frame"],
                text=text,
                command=command,
                width=w,
                height=h
            ),
            pack_open,
            pack_mode,
            x,
            y
        )

    def text(
            self,
            name: str,
            text: str | None = None,
            x: int = 0,
            y: int = 0,
            w: int = None,
            h: int = 1,
            pack_open: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name:
        :param text:
        :param x:
        :param y:
        :param w: 可展示全角字符数(半角可展示翻倍)
        :param h: 行
        :param pack_open:
        :param pack_mode:
        :return:
        """
        self.log.info(f"text: {name}")
        if self.check_name_and_mode(name, pack_mode) != (True, True):
            self.log.error(f"name: {name} or mode: {pack_mode} is exist")
            raise ValueError("名字存在或/和部署方法错误")

        tk_text = tk.Text(
                self.frame["frame"],
                width=w,
                height=h
            )

        if text is not None:
            tk_text.insert(
                tk.END,
                text
            )

        self.add_component(
            name,
            tk_text,
            pack_open,
            pack_mode,
            x,
            y
        )

    def message(
            self,
            name: str,
            text: str | None = None,
            x: int = 0,
            y: int = 0,
            w: int = None,
            pack_open: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name:
        :param text:
        :param x:
        :param y:
        :param w:
        :param pack_open:
        :param pack_mode:
        :return:
        """
        self.log.info(f"message: {name}")
        if self.check_name_and_mode(name, pack_mode)!= (True, True):
            self.log.error(f"name: {name} or mode: {pack_mode} is exist")
            raise ValueError("名字存在或/和部署方法错误")

        tk_message = tk.Message(
            self.frame["frame"],
            text=text,
            width=w,
        )

        self.add_component(
            name,
            tk_message,
            pack_open,
            pack_mode,
            x,
            y
        )


    def entry(
            self,
            name: str,
            default_text: str | None = None,
            x: int = 0,
            y: int = 0,
            w: int = None,
            pack_open: bool = True,
            pack_mode: str = 'pack',
    ):
        """

        :param name:
        :param default_text: 默认文本
        :param x:
        :param y:
        :param w:
        :param pack_open:
        :param pack_mode:
        :return:
        """
        self.log.info(f"entry: {name}")
        if self.check_name_and_mode(name, pack_mode)!= (True, True):
            self.log.error(f"name: {name} or mode: {pack_mode} is exist")
            raise ValueError("名字存在或/和部署方法错误")

        tk_entry = tk.Entry(
            self.frame["frame"],
            width=w,
        )

        if default_text:
            # noinspection PyUnusedLocal
            def set_default_text(event=None):
                """当输入框失去焦点且为空时，设置默认文本"""
                if not tk_entry.get():
                    tk_entry.insert(0, default_text)

            # noinspection PyUnusedLocal
            def clear_default_text(event=None):
                """当输入框获得焦点且有默认文本时，清除文本"""
                if tk_entry.get() == default_text:
                    tk_entry.delete(0, tk.END)

            # 默认文本
            tk_entry.insert(0, default_text)

            # 绑定焦点事件
            tk_entry.bind("<FocusIn>", clear_default_text)
            tk_entry.bind("<FocusOut>", set_default_text)

        self.add_component(
            name,
            tk_entry,
            pack_open,
            pack_mode,
            x,
            y
        )

    def list(
            self,
            name: str,
            _list = None,
            w: int = None,
            h: int = None,
            pack_open: bool = True,
    ):
        """
        建议单独开个Frame,list这玩意不好受
        默认部署方法为pack
        :param name:
        :param _list:
        :param w:
        :param h:
        :param pack_open:
        :return:
        """
        self.log.info(f"list: {name}")
        if self.check_name_and_mode(name, 'pack')!= (True, True):
            self.log.error(f"name: {name} or mode: {pack_open} is exist")
            raise ValueError("名字存在或/和部署方法错误")

        if _list is None:
            _list = []
        elif type(_list) is not list:
            _list = [_list]

        tk_list = tk.Listbox(
            self.frame["frame"],
            width=w,
            height=h,
        )

        for i in _list:
            tk_list.insert(
                tk.END,
                i
            )

        self.add_component(
            name,
            tk_list,
            pack_open,
            'pack',
        )

