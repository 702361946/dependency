from pyclbr import Function

from ._file import *


class Interpreter(FileBaseClass):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: FileBaseClass = FileBaseClass(),
            _interpreter = None
    ):
        super().__init__(_log, file_save_path)
        self._fc = _fc
        self._interpreter = _interpreter
        if not self._interpreter_chack():
            self._interpreter = None

    def _interpreter_chack(self) -> bool:
        if self._interpreter is None:
            return False

        if isinstance(self._interpreter, Function):
            return True
        else:
            return False

    def interpreter(
            self,
            v: Any,
    ) -> bool | Any:
        if not self._interpreter_chack():
            return False

        try:
            v = self._interpreter(v)
            return v
        except Exception as e:
            self.log.error(f"{e}\\in interpreter\\{v=}")
            return False

    def set_interpreter(self, _interpreter):
        if not self._interpreter_chack():
            return False
        self._interpreter = _interpreter
        return True
