#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import pygame
from ._key_mapping import *
import types

log = Log(
    log_sign="pygame.window",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)


class Window(object):
    def __init__(
            self,
            *,
            caption: str = "MainWindow",
            size: tuple[int, int] = (320, 180),
            fps: int = 60,
            icon_path: str | None = None,
            update: types.FunctionType,
            log: Log = log
    ):
        """
        初始化窗口

        :param caption: 标题
        :param size: 大小
        :param fps:
        :param icon_path: 图标路径
        :param update: 更新函数
        :param log:
        """
        self.log = log
        self.log.info(
            f"__init__\n"
            f"caption: {caption}\n"
            f"size: {size}\n"
            f"fps: {fps}\n"
            f"icon_path: {icon_path}\n"
        )

        self.caption = caption
        self.size = size
        self.fps = fps

        self.run_bool = False
        self.user_event_match: dict[Any, dict[str, Any]] = {
            256: {
                "function": self.quit,
                "open": True,
            }
        }

        pygame.init()

        # 窗口标题
        pygame.display.set_caption(caption)

        # 帧率
        self.clock = pygame.time.Clock()
        self.clock.tick(fps)

        # 图标
        self.icon = None
        if icon_path is not None:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
            self.icon = icon

        # 窗口
        self.window: pygame.Surface = pygame.display.set_mode(size)

        # update
        if isinstance(update, types.FunctionType):
            self.log.info("update set True")
            self.update = update
        else:
            self.log.error("update Type Error, update is set None")
            self.update = None

        self.key_mapping: dict[str, Key | MouseButton] = {}
        self.current_key_mapping: dict[str, str | None] = {
            "key": None,
            "MouseButton": None
        }

        self.log.info("__init__ ok\n")

    def set_key_mapping(self, name: str, mapping: Key | MouseButton) -> bool:
        self.log.info(f"set key mapping {name} -> {mapping}")
        self.key_mapping[name] = mapping
        return True

    def activate_key_mapping(self, name: str, _type: str):
        """
        激活按键映射
        :param name: key_mapping_name
        :param _type: 输入"Key"或"MouseButton"
        :return:
        """
        self.log.info(f"activate key mapping:{name}&{_type}")
        a = _type.upper()[0]
        if a != "K" and a != "M":
            self.log.error("type not Key or MouseButton")
            raise ValueError("_type not K or M")
        elif name not in self.key_mapping.keys():
            self.log.error(f"does not exist key mapping:{name}")
            raise ValueError(f"does not exist key mapping:{name}")

        match a:
            case "K":
                a = "Key"
            case "M":
                a = "MouseButton"

        self.current_key_mapping[a] = name

    def quit(self, event=None):
        """

        :return:
        """
        self.log.info(f"Window quit\\{event}")
        pygame.quit()
        self.run_bool = False
        return True

    def add_user_event_match(self, event: int, _function, _open: bool = True):
        """
        添加用户事件匹配

        :param event: 事件代码,详见event_compare.md文件
        :param _function: 函数,要求必须带一个可传入event参数
        :param _open:
        :return:
        """
        self.log.info(f"add_user_event_match\\event:{event}")
        self.user_event_match[event] = {
            "open": bool(_open),
            "function": _function
        }
        return True

    def key_event_match(self, event: pygame.event.Event) -> bool:
        """
        用来执行key类的按键匹配
        event只能绑定768,769,1025,1026这种按键事件
        同时请手动使用cls.add_user_event_match(_function = cls.key_event_match)添加用户事件匹配
        :param event: 事件
        :return:
        """
        mode = type(event).__name__
        if "Key" in mode:
            cls_name = "key"
            mode = mode.replace("Key", "")
            key = event.dict.get("key", 0)
        elif "MouseButton" in mode:
            cls_name = "MouseButton"
            mode = mode.replace("MouseButton", "")
            key = event.dict.get("button", 0)
        else:
            self.log.error(f"mode {mode} not Key or MouseButton")
            return False

        if self.current_key_mapping[cls_name] is not None:
            self.key_mapping[self.current_key_mapping[cls_name]].run_key_mapping(
                key=key,
                mode=mode,
                event=event
            )
            return True

        return False

    def set_update(self, update) -> bool:
        """
        用来切换你的屏幕显示
        :param update: 更新函数
        :return: T/F
        """
        if isinstance(update, types.FunctionType):
            self.log.info("update set True")
            self.update = update
        else:
            self.log.error("input update type not Function")
            return False
        return True

    def run(self, record_frame_interval: bool = False) -> bool:
        """
        运行窗口
        :param record_frame_interval: 是否记录帧间隔,日志等级必须为能记录DEBUG日志的等级
        :return:
        """
        self.log.info("Window run")
        self.run_bool = True

        while self.run_bool:
            try:
                for event in pygame.event.get():
                    if event.type in self.user_event_match:
                        if self.user_event_match[event.type]["open"]:
                            self.user_event_match[event.type]["function"](event=event)

                self.window.fill((0, 0, 0))

                if self.update is not None:
                    self.update()

                pygame.display.flip()

                if record_frame_interval:
                    self.log.debug(f"tick:{self.clock.tick(self.fps)}")

            except Exception as e:
                self.log.error(f"Window Error: {e}")
                return False

        return True
