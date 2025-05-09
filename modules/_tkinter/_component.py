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



