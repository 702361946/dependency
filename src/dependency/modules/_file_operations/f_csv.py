#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import csv
import io

from ._interpreter import *

class CSV(Interpreter):
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
            _interpreter_r=self.csv_interpreter_r,
            _interpreter_w=self.csv_interpreter_w
        )

    def csv_interpreter_r(self, v: str) -> ReturnValue[Any]:
        """

        """
        try:
            # 空串/纯空白处理
            if v.strip() == "":
                return ReturnValue(True, [])
            buffer = io.StringIO(v)
            return ReturnValue(True, list(csv.reader(buffer)))
        except Exception as e:
            self.log.error(f"{e}\\in csv analysis")
            return ReturnValue(False)

    def csv_interpreter_w(self, v: list[list[Any]]) -> ReturnValue[str]:
        """

        """
        if not isinstance(v, list):
            self.log.error(f"v type not dict or list\\{v=}")
            return ReturnValue(False)

        try:
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(v)
            v = buffer.getvalue()
            # 紧凑化
            t = ""
            for i in v.split("\r\n"):
                if not i:
                    continue
                t += i + "\n"
            if t: # 避免空字符串
                v = t[:-1] # -1用来删掉最后的\n
            return ReturnValue(True, v)
        except Exception as e:
            self.log.error(f"{e}\\in list[list] to csv")
            return ReturnValue(False)

    def load(
            self,
            filename: str,
            filepath: str = None,
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> ReturnValue[list[list[Any]]]:
        """
        :param filename: 是否不带后缀决定于$add_file_ext
        :param filepath:
        :param encoding:
        :param add_file_ext: 用于决定是否添加.csv后缀
        :return: False or file content
        """
        if not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return ReturnValue(False)
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return ReturnValue(False)

        if add_file_ext:
            filename = f"{filename}.csv"
        file_content = self._fc.load(
            file_name=filename,
            file_path=filepath,
            encoding=encoding
        )
        if not file_content.ok:
            return ReturnValue(False)

        return self.interpreter(file_content.v, "r")

    def dump(
            self,
            v: list[list[Any]],
            filename: str,
            filepath: str = None,
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> bool:
        """
        :param v: 写入的数据, 要求为矩阵, 同时一定是python库csv支持转换的值类型
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :return: 写入成功标志位
        """
        if not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return False
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return False

        v = self.interpreter(v, "w")
        if not v.ok:
            return False

        if add_file_ext:
            filename = f"{filename}.csv"
        file_content = self._fc.dump(
            v.v,
            file_name=filename,
            file_path=filepath,
            encoding=encoding
        )

        return file_content
