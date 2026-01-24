#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from ._path import *

class File(BaseClass):
    def load(
            self,
            file_path: str | Path,
            mode: str = "r",
            encoding: str = "UTF-8",
            mkdir_path: bool = False,
            *args,
            **kwargs
    ) -> ReturnValue[str | bytes | Exception]:
        """
        :param file_path: 需要文件后缀
        :param mode: 允许"r","b"
        :param encoding:
        :param mkdir_path: 补全目录
        :return: 当触发ERROR时返回RV(False)
        因为使用的是f.read(),故读大文件(>=1GB)有概率内存溢出,请小心使用
        """
        file_path = PathTools.str_to_path(file_path)
        if not file_path.ok:
            return ReturnValue(False, file_path)
        file_path = file_path.v

        if not isinstance(encoding, str):
            self.log.warning("encoding type not str")
            return ReturnValue(False, TypeError("encoding type not str"))

        if mode not in ["r", "b"]:
            self.log.warning(f"mode value not 'r' or 'b'\\{mode=}")
            return ReturnValue(
                False,
                TypeError(f"mode value not 'r' or 'b'\\{mode=}")
            )

        try:
            if mkdir_path:
                mkd = PathTools.mkdir(file_path.parent)
                if not mkd.ok:
                    return ReturnValue(False, mkd)

            # 需要更彻底的修改
            file_path = PathTools.path_to_str(file_path)
            if not file_path.ok:
                return ReturnValue(False, file_path)
            file_path = file_path.v

            if mode == "b":
                with open(file_path, "rb") as f:
                    return ReturnValue(True, f.read())
            else:
                with open(file_path, mode, encoding=encoding) as f:
                    return ReturnValue(True, f.read())
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return ReturnValue(False, e)

    def dump(
            self,
            v: Any,
            file_path: str | Path,
            mode: str = "w",
            encoding: str = "UTF-8",
            mkdir_path: bool = False,
            *args,
            **kwargs
    ) -> ReturnValue[Exception | None]:
        """
        :param v: 写入的值,在w or a模式下必须为str,在b模式下必须为二进制原始数据
        :param file_path: 需要带后缀
        :param mode: 允许"w","a","b"
        :param encoding:
        :param mkdir_path: 补全目录
        :return: 写入成功标志
        """
        file_path = PathTools.str_to_path(file_path)
        if not file_path.ok:
            return ReturnValue(False, file_path)
        file_path = file_path.v

        if not isinstance(encoding, str):
            self.log.warning("encoding type not str")
            return ReturnValue(False, TypeError(f"encoding type not str"))

        match mode:
            case "w" | "a":
                if not isinstance(v, str):
                    self.log.error(f"v type not str\\{v=}")
                    return ReturnValue(False, TypeError(f"v type not str\\{v=}"))
            case "b":
                if not isinstance(v, bytes):
                    self.log.error(f"v type not bytes\\{v=}")
                    return ReturnValue(False, TypeError(f"v type not bytes\\{v=}"))
            case _:
                self.log.error(f"mode value not 'w' or 'a' or 'b'\\{mode=}")
                return ReturnValue(
                    False,
                    TypeError(f"mode value not 'w' or 'a' or 'b'\\{mode=}")
                )

        try:
            if mkdir_path:
                mkd = PathTools.mkdir(file_path.parent)
                if not mkd.ok:
                    return ReturnValue(False, mkd)

            # 需要更彻底的修改
            file_path = PathTools.path_to_str(file_path)
            if not file_path.ok:
                return ReturnValue(False, file_path)
            file_path = file_path.v

            if mode == "b":
                with open(file_path, "wb") as f:
                    f.write(v)
            else:
                with open(file_path, mode, encoding=encoding) as f:
                    f.write(v)

            return ReturnValue(True, None)
        except Exception as e:
            self.log.error(f"{e}\\{file_path=}\\{encoding=}")
            return ReturnValue(False, e)


class FileBaseClass(File):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str | Path = ".",
            _fc: File = None
    ):
        """
        :param file_save_path:
        :param _log:
        :param _fc: 用于加载&写入内容的类,要求有load&dump方法
        """
        super().__init__(_log)
        cl = check_log(_log)
        if not cl.ok:
            self.log: Log = log
        else:
            self.log = _log

        fp = PathTools.str_to_path(file_save_path)
        if not fp.ok:
            fp = PathTools.str_to_path(".").v
            self.log.warning(f'file_save_path value set Path(".")')
        else:
            fp = fp.v

        self.file_path = fp
        self.generation_time = time.time()

        if _fc is None:
            self._fc = File()
        else:
            self._fc = _fc

    def _path_check(
            self,
            file_name: str,
            file_path: str | Path | None = None,
            mkdir_path: bool = False,
    ) -> ReturnValue[Path | Exception]:
        """
        通过检查返回路径, 未通过返回False
        :param file_name:
        :param file_path: 为None时等价于{self.file_path}
        :param mkdir_path: 是否创建目录
        """
        if file_path is None:
            file_path = self.file_path

        fp_rv = PathTools.str_to_path(file_path)
        if not fp_rv.ok:
            return ReturnValue(False, fp_rv)
        fp = fp_rv.v

        # file_name 检查
        if not isinstance(file_name, str):
            self.log.error(f"file_name type not str\\{file_name=}")
            return ReturnValue(False, TypeError(f"file_name type not str\\{type(file_name)=}"))
        # 空字符串
        if not file_name:
            self.log.error(f"file_name is empty\\{file_name=}")
            return ReturnValue(False, ValueError(f"file_name is empty"))

        # 非法文件名检查(error完全输出)
        not_in = '<>:"/\\|?*\x00'
        _r = False
        for c in not_in:
            if c in file_name:
                self.log.error(f"file_name contains {c}\\{file_name=}")
                _r = True
        if _r:
            return ReturnValue(
                False,
                ValueError(f"file_name contains illegal characters\\{file_name=}")
            )

        # 拼接路径
        join_path = fp / file_name  # Path 运算

        # 可选创建父目录
        if mkdir_path:
            mkd = PathTools.mkdir(join_path.parent)
            if not mkd.ok:
                return ReturnValue(False, mkd)

        return ReturnValue(True, join_path)

    def load(
            self,
            file_name: str,
            file_path: str | Path | None = None,
            mode: str = "r",
            encoding: str = "UTF-8",
            mkdir_path: bool = False,
            *args,
            **kwargs
    ) -> ReturnValue[str | bytes | Exception]:
        """
        当{file_path}为None时,将使用{self.file_path}
        """
        file_path = self._path_check(file_name, file_path, mkdir_path)
        if not file_path.ok:
            return file_path
        return self._fc.load(file_path.v, mode, encoding, *args, **kwargs)

    def dump(
            self,
            v: Any,
            file_name: str,
            file_path: str | Path | None = None,
            mode: str = "w",
            encoding: str = "UTF-8",
            mkdir_path: bool = False,
            *args,
            **kwargs
    ) -> ReturnValue[Exception | None]:
        """
        {v}为要写入的值
        当{file_path}为None时,将使用{self.file_path}
        """
        file_path = self._path_check(file_name, file_path, mkdir_path)
        if not file_path.ok:
            return file_path
        return self._fc.dump(v, file_path.v, mode, encoding, *args, **kwargs)

    def set_fc(self, new_fc: File) -> bool:
        # 是否允许用户自行拓展有待深究
        if not isinstance(new_fc, File):
            self.log.error(f"new_fc type not File\\{new_fc=}")
            return False

        if "load" not in dir(new_fc) or "dump" not in dir(new_fc):
            self.log.error(f'new_fc no func "load" or/and "dump"\\{dir(new_fc)=}')
            return False
        self._fc = new_fc
        return True

    def set_log(self, new_log: Log) -> bool:
        if not check_log(new_log).ok:
            return False
        self.log = new_log
        return True

