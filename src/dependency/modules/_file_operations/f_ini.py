#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import configparser
import io

from ._interpreter import *


class Ini(Interpreter):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: FileBaseClass = None,
    ):
        super().__init__(
            _log=_log,
            file_save_path=file_save_path,
            _fc=_fc,
            _interpreter_r=self.ini_interpreter_r,
            _interpreter_w=self.ini_interpreter_w
        )

    def ini_interpreter_r(self, text: str) -> dict[str, Any]:
        if not isinstance(text, str):
            self.log.error(f"ini interpreter need str, got {type(text)}")
            raise TypeError(f"ini interpreter need str, got {type(text)}")
        try:
            cp = configparser.ConfigParser()
            cp.read_string(text)
            v = {sect: dict(cp[sect]) for sect in cp.sections()}
            return v
        except Exception as e:
            self.log.error(f"{e} \\ in ini_interpreter_r")
            raise e

    def ini_interpreter_w(self, v: dict[str, dict[str, Any]]) -> str:
        """
        v应符合https://docs.python.org/3/library/configparser.html所定义的标准
        """
        cp = configparser.ConfigParser()
        for sect, opts in v.items():
            if not isinstance(opts, dict):
                self.log.error(f"section '{sect}' must be dict, got {type(opts)}")
                raise TypeError(f"section '{sect}' must be dict, got {type(opts)}")

            try:
                cp.add_section(sect)
            except configparser.DuplicateSectionError:
                self.log.error(f"duplicate section '{sect}'")

            for k, val in opts.items():
                cp.set(sect, str(k), str(val))

        with io.StringIO() as s:
            cp.write(s)
            text = s.getvalue()

        return text

    def load(
            self,
            file_name: str,
            file_path: str | None = None,
            mode: str = "r",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            *args,
            **kwargs
    ) -> ReturnValue[dict[str, Any]]:
        if add_file_ext and file_name:
            file_name += ".ini"

        v = self._fc.load(
            file_name = file_name,
            file_path = file_path,
            mode = mode,
            encoding = encoding,
        )
        if not v.ok:
            return ReturnValue(False, v)

        return self.interpreter(v.v, "r")

    def dump(
            self,
            v: dict[str, dict[str, Any]],
            file_name: str,
            file_path: str | None = None,
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            *args,
            **kwargs,
    ) -> ReturnValue[Any]:
        """嵌套 dict -> ini 文件"""
        if not isinstance(v, dict):
            self.log.error(f"dump need dict, got {type(v)}")
            return ReturnValue(False, TypeError(f"dump need dict, got {type(v)}"))

        if add_file_ext and file_name:
            file_name += ".ini"

        v = self.interpreter(v, "w")
        if not v.ok:
            return v

        return self._fc.dump(
            v.v,
            file_name,
            file_path,
            mode="w",
            encoding=encoding
        )
