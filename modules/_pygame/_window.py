#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import pygame
from typing import Any
from._get_package import *

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
            log: Log = log
    ):
        """
        初始化窗口

        :param caption: 标题
        :param size: 大小
        :param fps:
        :param icon_path: 图标路径
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

        self.log.info("__init__ ok\n")

    def quit(self, event = None):
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


    def run(self, updata = None, record_frame_interval: bool = False) -> bool:
        """
        运行窗口
        :param updata: 更新函数
        :param record_frame_interval: 是否记录帧间隔,日志等级必须为DEBUG或能记录DEBUG日志的等级
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

                if updata is not None:
                    updata()

                pygame.display.flip()

                if record_frame_interval:
                    self.log.debug(f"tick:{self.clock.tick(self.fps)}")

            except Exception as e:
                self.log.error(f"Window Error: {e}")
                return False

        return True
