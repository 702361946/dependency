#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from ._window import *

log = Log(
    log_sign="image",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)


class Image(object):
    def __init__(
            self,
            *,
            store_image_file_path: str = "image",
            scan_exclusion_directory: list[str] = None,
            image_file_extension: list[str] = None,
            log: Log = log
    ):
        """
        :param store_image_file_path: 保存路径
        :param scan_exclusion_directory: 扫描时排除的目录, 均为保存路径拼接
        :param image_file_extension: 允许的文件后缀
        :param log:
        """
        self.log = log
        self.log.info("__init__")

        # 处理默认值
        if image_file_extension is None:
            image_file_extension = ["png", "jpg", "jpeg"]
        if scan_exclusion_directory is None:
            scan_exclusion_directory = []

        self.scan_exclusion_directory: list[str] = scan_exclusion_directory
        self.image_file_extension: list[str] = [ext.lower().lstrip(".") for ext in image_file_extension]

        self.file_path: str = store_image_file_path

        # 预计算排除目录的绝对路径，避免每次循环拼接
        exclude_abs = {
            os.path.abspath(os.path.join(self.file_path, d))
            for d in self.scan_exclusion_directory
        }

        self.images: dict[str, dict[str, str | pygame.Surface | None]] = {}
        for root, dirs, files in os.walk(self.file_path):
            # 如果当前目录在排除列表，跳过整个分支
            if os.path.abspath(root) in exclude_abs:
                dirs[:] = []  # 不再遍历子目录
                continue

            for file in files:
                ext = os.path.splitext(file)[1].lower().lstrip(".")
                if ext not in self.image_file_extension:
                    continue

                rel_path = os.path.relpath(root, self.file_path)
                if rel_path == ".":
                    key = file
                else:
                    key = f"{rel_path.replace(os.sep, '.')}.{file}"

                self.images[key] = {
                    "path": os.path.join(root, file),
                    "image": None
                }

        pygame.init()
        self.log.info("__init__ ok\n")

    def init_image(self, images: str | list[str]) -> list[bool]:
        """
        用来初始化图片
        提交的内容示例

        self.file_path\\temp.png
        self.file_path\\temp\\temp.jpg
        如上的两个文件,
        如果要加载,格式如下
        temp.png
        temp.temp.jpg

        总之就是去掉.\\(./),\\(/)换成.
        :return:
        """
        self.log.info(f"load\\images:{images}")

        if type(images).__name__ != 'list':
            images = [str(images)]

        t = []
        for i in images:
            if i in self.images.keys():
                # mypy str | None
                _t = self.images[i]["path"]
                if _t is None:
                    self.log.error(f"no path:{i}")
                    t.append(False)
                    continue

                self.images[i]["image"] = pygame.image.load(str(_t))

                self.log.info(f"ok:{i}")
                t.append(True)
            else:
                self.log.error(f"no image:{i}")
                t.append(False)
                continue

        return t

    def init_all_image(self):
        """
        初始化所有图片
        :return:
        """
        self.log.info("init_all_image")

        for i in self.images.keys():
            if self.images[i]["image"] is not None:
                continue
            self.init_image(i)

        self.log.info("init_all_image ok")

    def get_image(self, images: str | list[str]) -> list[tuple[bool, pygame.Surface | None | str]]:
        """
        获取图片
        :param images: 图片名,依照规则传入
        :return: 返回一个列表,列表的内容是一个元组,元组的内容是成功标识和pygame.Surface对象或None
        """
        self.log.info(f"get_image\\images:{images}")

        if type(images).__name__ != 'list':
            images = [str(images)]

        t = []
        for i in images:
            if i in self.images.keys():
                if self.images[i]["image"] is not None:
                    t.append((True, self.images[i]["image"]))
                    self.log.info(f"ok:{i}")
                else:
                    t.append((False, None))
                    self.log.error(f"no init image:{i}")
            else:
                t.append((False, None))
                self.log.error(f"no image:{i}")

        return t

    def blit(
            self,
            image_name: str,
            window: Window,
            x: int = 0,
            y: int = 0
    ) -> bool:
        """
        绘制图片

        :param image_name: 图片名,依照规则传入
        :param window:
        :param x:
        :param y:
        :return:
        """
        if image_name in self.images.keys():
            if self.images[image_name]["image"] is not None:
                image = self.images[image_name]["image"]
                if isinstance(image, pygame.Surface):
                    window.window.blit(image, (x, y))
                else:
                    self.log.error(f"type not Surface:{image_name}")
                    return False

            else:
                self.log.error(f"no init image:{image_name}")
                return False

        else:
            self.log.error(f"no image:{image_name}")
            return False

        return True

    def scale(self, image_name: str, size: tuple[int, int]) -> bool:
        """
        缩放图片
        :param image_name: 图片名,依照规则传入
        :param size: 缩放后的大小
        :return:
        """
        self.log.info(f"scale\\image_name:{image_name}")

        if image_name in self.images.keys():
            if self.images[image_name]["image"] is not None:
                image = self.images[image_name]["image"]
                if isinstance(image, pygame.Surface):
                    self.images[image_name]["image"] = pygame.transform.scale(image, size)
                else:
                    self.log.error(f"type not Surface:{image_name}")
                    return False

            else:
                self.log.error(f"no init image:{image_name}")
                return False

        else:
            self.log.error(f"no image:{image_name}")
            return False

        return True
