#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
from ._window import *

log = Log(
    log_sign="pygame.font",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)

class Font(object):
    def __init__(
            self,
            *,
            store_font_file_path: str = "font",
            font_sizes: tuple[int] | None = None,
            raise_error: bool = True,
            log: Log = log
    ):
        """
        只支持ttf格式的字体
        会扫描指定目录下的所有ttf文件,并生成字体对象
        字体名称为文件名,不包含扩展名

        :param store_font_file_path:
        :param raise_error:
        :param font_sizes: 字体大小列表,用于初始加载,不可更改,默认为(12, 24, 36, 48, 60)
        :param log:
        """
        self.log = log

        if font_sizes is None:
            font_sizes = (12, 24, 36, 48, 60)

        self.log.info("__init__")

        self.file_path = store_font_file_path
        self.raise_error = raise_error

        self.fonts: dict[str, dict[int, pygame.font.Font | bool]] = {}
        """
        key: 字体名
        value: Font对象或False
        """

        self.sizes = font_sizes

        pygame.font.init()

        # 提取所有字体文件名&父目录
        t = []
        for root, _, files in os.walk(self.file_path):
            for file in files:
                if file.lower().endswith('.ttf'):
                    font_name = os.path.splitext(file)[0]
                    t.append((font_name, root))

        # 生成字体对象
        for font_name, root in t:
            try:
                for size in font_sizes:
                    self.fonts[font_name][size] = pygame.font.Font(os.path.join(root, f"{font_name}.ttf"), size)
                    self.log.info(f"Loaded font: {font_name}")

            except Exception as e:
                self.log.error(f"Failed to load font {font_name}: {e}")

                for size in font_sizes:
                    self.fonts[font_name][size] = False

                if self.raise_error:
                    raise RuntimeError(f"Failed to load font {font_name}")

    def bilt(
            self,
            text: str,
            font_name: str,
            font_size: int,
            rgb: tuple[int, int, int] = (0, 0, 0),
            *,
            x: int,
            y: int,
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
        if font_name not in self.fonts or font_size not in self.fonts[font_name]:
            self.log.error(f"Font not found: {font_name} size {font_size}")
            if self.raise_error:
                raise ValueError(f"Font not found: {font_name} size {font_size}")
            return False

        # 检查字体是否加载成功
        font = self.fonts[font_name][font_size]
        if not isinstance(font, pygame.font.Font):
            self.log.error(f"Font not loaded: {font_name} size {font_size}")
            if self.raise_error:
                raise ValueError(f"Font not loaded: {font_name} size {font_size}")
            return False

        # 生成文字图片对象
        try:
            text_surface = font.render(text, True, rgb)
            # 渲染到窗口
            window.window.blit(text_surface, (x, y))
            return True
        except Exception as e:
            self.log.error(f"Failed to render text: {e}")
            if self.raise_error:
                raise RuntimeError(f"Failed to render text: {e}")
            return False
