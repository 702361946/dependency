import configparser
import io

from ._interpreter import *

class Ini(Interpreter):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: FileBaseClass = FileBaseClass()
    ):
        super().__init__(_log, file_save_path, _fc)
        self.set_interpreter(self.ini_interpreter)

    def ini_interpreter(self, text: str) -> bool | dict[str, Any]:
        if not isinstance(text, str):
            self.log.error(f"ini interpreter need str, got {type(text)}")
            return False
        try:
            cp = configparser.ConfigParser()
            cp.read_string(text)
            v = {sect: dict(cp[sect]) for sect in cp.sections()}
            return v
        except Exception as e:
            self.log.error(f"{e} \\ in ini_interpreter")
            return False

    def load(
            self,
            file_name: str,
            file_path: str | None = None,
            mode: str = "r",
            encoding: str = "UTF-8",
            *args,
            **kwargs
    ):
        v = self._fc.load(
            file_name = file_name,
            file_path = file_path,
            mode = mode,
            encoding = encoding,
        )

        return self.interpreter(v)

    def dump(
            self,
            v: dict[str, dict[str, Any]],
            file_name: str,
            file_path: str | None = None,
            encoding: str = "UTF-8",
            **kwargs,
    ) -> bool:
        """嵌套 dict -> ini 文件"""
        if not isinstance(v, dict):
            self.log.error(f"dump need dict, got {type(v)}")
            return False

        cp = configparser.ConfigParser()
        for sect, opts in v.items():
            if not isinstance(opts, dict):
                self.log.error(f"section '{sect}' must be dict, got {type(opts)}")
                return False
            try:
                cp.add_section(sect)
            except configparser.DuplicateSectionError:
                self.log.error(f"duplicate section '{sect}'")
            for k, val in opts.items():
                cp.set(sect, str(k), str(val))

        with io.StringIO() as s:
            cp.write(s)
            text = s.getvalue()

        return self._fc.dump(
            text,
            file_name,
            file_path,
            mode="w",
            encoding=encoding
        )
