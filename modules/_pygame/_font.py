#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import os.path

from ._window import *

log = Log(
    log_sign="font",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)

os_font_file_path = "font"
if os_name[1] == "Windows":
    os_font_file_path = "C:\\Windows\\Fonts"


class Font(object):
    def __init__(
            self,
            *,
            store_font_file_path: str = os_font_file_path,
            auto_add_font_size: bool = False,
            log: Log = log
    ):
        """
        只支持ttf格式的字体
        字体名称为文件名,不包含扩展名

        :param store_font_file_path: 字体保存路径,非Windows默认为"./font",Windows默认为"C:\\Windows\\Fonts"
        :param auto_add_font_size: 自动添加字体大小
        :param log:
        """
        self.log = log

        self.log.info(f"__init__\\path:{store_font_file_path}")

        self.file_path = store_font_file_path

        self.auto_add_font_size = auto_add_font_size

        self.fonts: dict[str, dict[str, pygame.font.Font | bool | str]] = {}
        """
        {
            "字体名": {
                "path": 字体路径
                "字号": Font对象或None
            }
        }
        """

        pygame.font.init()

    def scan(self) -> list[str]:
        self.log.info("scan")

        t = []
        for root, dirs, files in os.walk(self.file_path):
            for i in files:
                if os.path.splitext(i)[1] != ".ttf":
                    continue
                t.append(os.path.join(root, i))

        self.log.info(f"scan len:{len(t)}")
        return t

    def add_font(self, font_path: str) -> bool:
        """

        :param font_path:
        :return:
        """
        if not os.path.isfile(font_path):
            self.log.error(f"file not in path:{font_path}")
            return False

        file_name = os.path.split(font_path)[1]
        file_ext = os.path.splitext(file_name)[1]
        file_name = os.path.splitext(file_name)[0]

        if file_ext != ".ttf":
            self.log.error(f"file ext not ttf: {file_ext}")
            return False

        self.fonts[file_name] = {
            "path": f"{font_path}"
        }

        self.log.info(f"add True:{font_path}")
        return True

    def add_fonts(self, font_paths: list[str]) -> list[bool]:
        if not isinstance(font_paths, list):
            font_paths = [font_paths]

        t = []
        for i in font_paths:
            t.append(self.add_font(i))

        return t

    def add_font_size(self, font_name: str, font_size: int) -> bool:
        """

        :param font_name: 字体名
        :param font_size: 字体大小
        :return:
        """
        if font_name not in self.fonts.keys():
            self.log.error(f"font not in fonts:{font_name}")
            return False

        if not isinstance(font_size, int):
            self.log.error(f"font size type not int:{type(font_size)}")
            return False

        self.fonts[font_name][f"{font_size}"] = pygame.font.Font(
            f"{self.fonts[font_name]['path']}",
            font_size
        )

        self.log.info(f"add font size:{font_name}\\{font_size}")
        return True

    def add_font_size_s(self, font_name: list[str], font_size: list[int]) -> list[list[bool]]:
        """

        :param font_name:
        :param font_size:
        :return:
        """
        if not isinstance(font_name, list):
            font_name = [font_name]
        if not isinstance(font_size, list):
            font_size = [font_size]

        t = []
        for i in font_name:
            _t = []
            for _i in font_size:
                _t.append(self.add_font_size(i, _i))
            t.append(_t)

        return t

    def __get__(self, font_name: str, font_size: int) -> pygame.font.Font | None:
        """
        获取对象,没有就返回None
        :param font_name:
        :param font_size:
        :return:
        """
        return self.fonts.get(font_name, {}).get(f"{font_size}", None)

    def bilt(
            self,
            text: str,
            font_name: str,
            font_size: int,
            rgb: tuple[int, int, int] = (0, 0, 0),
            *,
            x: int = 0,
            y: int = 0,
            window: Window
    ) -> bool:
        """
        绘制文字

        :param text: 要渲染的文字
        :param font_name: 字体名称
        :param font_size: 字体大小,必须为初始化时提供的字体大小之一
        :param rgb: 文字颜色,采用RGB格式,默认为黑色
        :param x: x坐标
        :param y: y坐标
        :param window: 窗口对象
        :return: 是否绘制成功
        """
        # 检查字体是否存在
        if font_name not in self.fonts.keys():
            self.log.error(f"font not in fonts:{font_name}")
            return False

        if f"{font_size}" not in self.fonts[font_name].keys():
            self.log.error(f"font size not in sizes:{font_name}\\{font_size}")
            return False

        # 检查字体是否加载成功
        font = self.fonts[font_name][f"{font_size}"]
        if not isinstance(font, pygame.font.Font):
            self.log.error(f"Font not loaded: {font_name}\\{font_size}")
            return False

        # 生成文字图片对象
        try:
            text_surface = font.render(text, True, rgb)
            # 渲染到窗口
            window.window.blit(text_surface, (x, y))
            return True
        except Exception as e:
            self.log.error(f"Failed to render text: {e}")
            return False
