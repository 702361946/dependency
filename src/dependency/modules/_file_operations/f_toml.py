#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import tomlkit

from ._interpreter import *


class Toml(Interpreter):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: FileBaseClass = None
    ):
        super().__init__(
            _log=_log,
            file_save_path=file_save_path,
            _fc=_fc,
            _interpreter_r=tomlkit.loads,
            _interpreter_w=tomlkit.dumps
        )

    def load(
            self,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> ReturnValue[dict]:
        """
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        """
        if not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return ReturnValue(False, TypeError(f"add_file_ext type not bool\\{add_file_ext=}"))

        if add_file_ext:
            filename = f"{filename}.toml"
        file_content = self._fc.load(
            file_name=filename,
            file_path=filepath,
            encoding=encoding,
            **kwargs
        )
        if not file_content.ok:
            return ReturnValue(False, file_content)

        # analysis
        return self.interpreter(file_content.v, "r", **kwargs)

    def dump(
            self,
            v: dict | list,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> ReturnValue[Any]:
        """
        :param v: 写入的数据
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :return: 写入成功标志位
        """
        if not isinstance(v, dict) and not isinstance(v, list):
            self.log.error(f"v type not dict or list\\{v=}")
            return ReturnValue(False, TypeError(f"v type not dict or list\\{v=}"))
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return ReturnValue(False, TypeError(f"add_file_ext type not bool\\{add_file_ext=}"))

        v = self.interpreter(v, "w", **kwargs)
        if not v.ok:
            return v

        if add_file_ext:
            filename = f"{filename}.toml"
        return self._fc.dump(
            v.v,
            file_name=filename,
            file_path=filepath,
            encoding=encoding,
            **kwargs
        )
