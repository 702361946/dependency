#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import os
from .config import *

class File(BaseClass):
    def load(
            self,
            file_path: str,
            mode: str = "r",
            encoding: str = "UTF-8"
    ) -> ReturnValue[str | bytes]:
        """
        :param file_path: 需要文件后缀
        :param mode: 允许"r","b"
        :param encoding:
        :return: 当触发ERROR时返回RV(False)
        因为使用的是f.read(),故读大文件(>=1GB)有概率内存溢出,请小心使用
        """
        if not isinstance(file_path, str):
            self.log.warning("file_path type not str")
            return ReturnValue(False)
        if not isinstance(encoding, str):
            self.log.warning("encoding type not str")
            return ReturnValue(False)

        if mode not in ["r", "b"]:
            self.log.warning(f"mode value not 'r' or 'b'\\{mode=}")
            return ReturnValue(False)

        try:
            if mode == "b":
                with open(file_path, mode) as f:
                    return ReturnValue(True, f.read())
            else:
                with open(file_path, mode, encoding=encoding) as f:
                    return ReturnValue(True, f.read())
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return ReturnValue(False)

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
            if mode == "b":
                with open(file_path, mode) as f:
                    f.write(v)

            else:
                with open(file_path, mode, encoding=encoding) as f:
                    f.write(v)

            return True
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return False


class FileBaseClass(File):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: File = File()
    ):
        """
        :param file_save_path:
        :param _log:
        :param _fc: 用于加载&写入内容的类,要求有load&dump方法
        """
        super().__init__(_log)
        check_log(_log)
        self.log: Log = _log

        if not isinstance(file_save_path, str):
            self.log.warning(f'\nfile_save_path type not str,\n'
                             f'file_save_path value set "."\n{file_save_path=}')
        elif not os.path.isdir(file_save_path):
            self.log.error(f"file_save_path does not exist\\{file_save_path=}")

        self.file_path = file_save_path
        self.generation_time = time.time()
        self._fc = _fc

    def _path_check(
            self,
            file_name: str,
            file_path: str | None = None,
    ) -> bool | str:
        """
        通过检查返回路径, 未通过返回False
        :param file_name:
        :param file_path:为None时等价于{self.file_path}
        """
        if file_path is None:
            file_path = self.file_path

        if file_name:
            if not isinstance(file_name, str):
                self.log.warning(f"The return value will be a directory rather than a file path\\"
                                 f"{file_name=}")
        else:
            self.log.warning(f"file_name is None\\in path check\\{file_name=}")
            return False

        if file_path:
            if not isinstance(file_path, str):
                self.log.warning(f"file_path type not str\\in path check\\{file_path=}")
        else:
            self.log.warning(f"file_path is None\\in path check\\{file_path=}")
            return False

        join_path = os.path.join(file_path, file_name)
        # if not os.path.isdir(join_path):
        #     self.log.error(f"file_path does not exist\\{file_path=}")
        #     return False
        return join_path

    def load(
            self,
            file_name: str,
            file_path: str | None = None,
            mode: str = "r",
            encoding: str = "UTF-8",
            *args,
            **kwargs
    ) -> ReturnValue[str | bytes]:
        """
        当{file_path}为None时,将使用{self.file_path}
        """
        file_path = self._path_check(file_name, file_path)
        if file_path is False:
            return ReturnValue(False)
        return self._fc.load(file_path, mode, encoding)

    def dump(
            self,
            v: Any,
            file_name: str,
            file_path: str | None = None,
            mode: str = "w",
            encoding: str = "UTF-8",
            *args,
            **kwargs
    ) -> bool:
        """
        {v}为要写入的值
        当{file_path}为None时,将使用{self.file_path}
        """
        file_path = self._path_check(file_name, file_path)
        if file_path is False:
            return False
        return self._fc.dump(v, file_path, mode, encoding)

    def set_fc(self, new_fc: File) -> bool:
        # 是否允许用户自行拓展有待深究
        if not isinstance(new_fc, File):
            self.log.error(f"new_fc type not File\\{new_fc=}")
            return False

        if "load" not in dir(new_fc) or "dump" not in dir(new_fc):
            self.log.error(f'new_fc no func "load" or/and "dump"\\{dir(new_fc)=}')
        self._fc = new_fc
        return True

    def set_log(self, new_log: Log) -> bool:
        if not check_log(new_log):
            return False
        self.log = new_log
        return True

