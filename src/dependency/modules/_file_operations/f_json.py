#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import json

from ._interpreter import *

class Json(Interpreter):
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
            _interpreter_r=json.loads,
            _interpreter_w=json.dumps
        )

    def load(
            self,
            filename: str,
            filepath: str = None,
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> ReturnValue[dict | list]:
        """
        :param filename: 是否不带后缀决定于$add_file_ext
        :param filepath:
        :param encoding:
        :param add_file_ext: 用于决定是否添加.json后缀
        :return: RV[False or file content]
        """
        if not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return ReturnValue(False)
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return ReturnValue(False)

        if add_file_ext:
            filename = f"{filename}.json"
        v = self._fc.load(
            file_name=filename,
            file_path=filepath,
            encoding=encoding
        )
        if not v.ok:
            return ReturnValue(False)

        # analysis
        try:
            v = self.interpreter(v.v, "r")
        except Exception as e:
            self.log.error(f"{e}\\in json analysis")
            return ReturnValue(False)

        return v

    def dump(
            self,
            v: dict | list,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            ensure_ascii: bool = False,
            indent: int | str | None = 4,
            **kwargs
    ) -> bool:
        """
        :param v: 写入的数据
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :param ensure_ascii:
        :param indent:
        :return: 写入成功标志位
        """
        if not isinstance(v, dict) and not isinstance(v, list):
            self.log.error(f"v type not dict or list\\{v=}")
            return False
        elif not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return False
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return False
        elif not isinstance(ensure_ascii, bool):
            self.log.error(f"ensure_ascii type not bool\\{ensure_ascii=}")
            return False
        elif not isinstance(indent, int):
            self.log.error(f"indent type not int\\{indent=}")
            return False

        v = self.interpreter(v, "w", ensure_ascii=ensure_ascii, indent=indent)
        if not v.ok:
            return False

        if add_file_ext:
            filename = f"{filename}.json"
        file_content = self._fc.dump(
            v.v,
            file_name=filename,
            file_path=filepath,
            encoding=encoding
        )
        return file_content

