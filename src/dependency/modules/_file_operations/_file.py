from .config import *

class File(BaseClass):
    def load(
            self,
            file_path: str,
            mode: str = "r",
            encoding: str = "UTF-8"
    ) -> Any:
        """
        :param file_path: 需要文件后缀
        :param mode: 允许"r","b"
        :param encoding:
        :return: 当触发ERROR时返回False
        """
        if not isinstance(file_path, str):
            self.log.warning("file_path type not str")
            return False
        if not isinstance(encoding, str):
            self.log.warning("encoding type not str")
            return False

        if mode not in ["r", "b"]:
            self.log.warning(f"mode value not 'r' or 'b'\\{mode=}")
            return False

        try:
            with open(file_path, mode, encoding=encoding) as f:
                return f.read()
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return False

    def dump(
            self,
            v: Any,
            file_path: str,
            mode: str = "w",
            encoding: str = "UTF-8",
    ) -> bool:
        """
        :param v: 写入的值,在w or a模式下必须为str,在b模式下必须为二进制原始数据
        :param file_path: 需要带后缀
        :param mode: 允许"w","a","b"
        :param encoding:
        :return: 写入成功标志
        """
        if not isinstance(file_path, str):
            self.log.warning("file_path type not str")
            return False
        if not isinstance(encoding, str):
            self.log.warning("encoding type not str")
            return False

        match mode:
            case "w" | "a":
                if not isinstance(v, str):
                    self.log.error(f"v type not str\\{v=}")
                    return False
            case "b":
                if not isinstance(v, bytes):
                    self.log.error(f"v type not bytes\\{v=}")
                    return False
            case _:
                self.log.error(f"mode value not 'w' or 'a' or 'b'\\{mode=}")
                return False

        try:
            with open(file_path, mode, encoding=encoding) as f:
                f.write(v)
                return True
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return False

