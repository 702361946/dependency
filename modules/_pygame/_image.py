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
            exclusion_directory: list[str] = None,
            image_file_extension: set[str] = None,
            separator: str = ".",
            log: Log = log
    ):
        """
        :param store_image_file_path: 保存路径,从.\\开始,除非为绝对路径
        :param exclusion_directory: 排除的目录, 均为保存路径拼接
        :param image_file_extension: 允许的文件后缀
        :param separator: 分隔符,用以分割路径
        :param log:
        """
        self.log = log
        self.log.info("__init__")

        self.separator = separator

        # 处理默认值
        if exclusion_directory is None:
            exclusion_directory = []
        if image_file_extension is None:
            image_file_extension: set[str] = {"png", "jpg", "jpeg"}

        if os.path.isabs(store_image_file_path):
            self.file_path: str = store_image_file_path
        else:
            self.file_path: str = os.path.abspath(store_image_file_path)

        t: set[str] = set()
        for i in exclusion_directory:
            t.add(os.path.join(self.file_path, i))
        self.exclusion_directory: set[str] = t
        self.image_file_extension: set[str] = image_file_extension

        self.images: dict[str, dict[str, str | pygame.Surface | None]] = {}
        """
        {
            "file_path": str,
            
            "file_name": str(带后缀),
            
            "image": pygame.Surface | None 
        }
        """

        pygame.init()
        self.log.info("__init__ ok\n")

    def add_file(self, file_path: str) -> bool:
        """

        :param file_path: 文件路径,基于保存路径
        :return:
        """
        path = os.path.join(self.file_path, file_path)

        # 排除目录
        for ed in self.exclusion_directory:
            if os.path.commonpath([path, ed]) in self.exclusion_directory:
                self.log.warning(f"file_path in exclusion directory:{path}")
                return False

        # 文件存在
        if not os.path.isfile(path):
            self.log.warning(f"file not in: {path}")
            return False

        # 后缀检查
        _, ext = os.path.splitext(path)
        # .开头,需去掉
        if ext[1:] not in self.image_file_extension:
            self.log.info(f"file extension not in extension:{self.image_file_extension}\\{ext}")
            return False

        # key
        try:
            rel_path = os.path.relpath(path, self.file_path)
        except ValueError:
            self.log.warning(f"无法计算相对路径: {path}")
            return False
        key = rel_path.replace(os.sep, self.separator)

        # key存在检查
        if key in self.images:
            self.log.info(f"file in images: {path}\\{key}")
            return False

        # 加入
        self.images[key] = {
            "path": path,
            "image": None
        }
        self.log.info(f"已加入: {key}")
        return True

    def add_files(self, file_path_s: list[str] | str) -> list[bool]:
        """

        :param file_path_s: 文件路径,均为相对路径
        :return: 每次添加的成功情况
        """
        if isinstance(file_path_s, str):
            file_path_s = [file_path_s]

        t = []
        for i in file_path_s:
            t.append(self.add_file(i))

        return t

    def scan_directory(self, directory: str) -> list[str]:
        """

        :param directory: 扫描目录
        :return: 返回扫描到的所有后缀匹配的文件
        """
        directory = os.path.join(self.file_path, directory)

        t = []
        for root, dirs, files in os.walk(directory):
            for i in files:
                _, ext = os.path.splitext(i)
                if ext[1:] in self.image_file_extension:
                    t.append(os.path.join(self.file_path, root, i))

        return t

    def scan_directory_s(self, directorys: list[str] | str) -> list[str]:
        """

        :param directorys:
        :return:
        """
        if isinstance(directorys, str):
            directorys = [directorys]

        t: set[str] = set()
        for i in directorys:
            for _i in self.scan_directory(i):
                t.add(_i)

        return list(t)

    def add_exclusion_directory(self, ed_path: str, del_file: bool = False):
        """

        :param ed_path: 排除目录,基于相对目录
        :param del_file: 删除已加载的匹配项目
        :return:
        """
        ed_path = os.path.join(self.file_path, ed_path)
        self.exclusion_directory.add(ed_path)

        if del_file:
            for i in self.images.keys():
                if os.path.commonpath([self.images[i]["path"], ed_path]) == ed_path:
                    if self.images.pop(i, None) is None:
                        self.log.warning(f"file not in images:{i}")

    def add_exclusion_directory_s(self, ed_path_s: list[str] | str, del_file: bool = False):
        """
        同add_exclusion_directory
        :param ed_path_s: 需要的列表
        :param del_file:
        :return:
        """
        if isinstance(ed_path_s, str):
            ed_path_s = [ed_path_s]

        for i in ed_path_s:
            self.add_exclusion_directory(i, del_file)

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

        总之就是把路径分隔符换成指定的分隔符
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
