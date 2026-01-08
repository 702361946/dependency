#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

from ._file import *


class Interpreter(FileBaseClass):
    def __init__(
            self,
            _log: Log | Logger = log,
            file_save_path: str = ".",
            _fc: FileBaseClass = None,
            _interpreter_r = None,
            _interpreter_w = None
    ):
        super().__init__(_log, file_save_path)
        if not isinstance(_fc, FileBaseClass):
            self.log.error("Interpreter must be a FileBaseClass object")
            _fc = FileBaseClass(file_save_path=file_save_path)
        elif _fc is None:
            _fc = FileBaseClass(file_save_path=file_save_path)
        self._fc = _fc

        self._interpreter_r = _interpreter_r
        if not self._interpreter_check("r"):
            self._interpreter_r = None

        self._interpreter_w = _interpreter_w
        if not self._interpreter_check("w"):
            self._interpreter_w = None

    def _interpreter_check(self, mode = "a") -> bool:
        """
        :param mode:mode 有三种值, a:all,r,w, 在all模式下返回值不单独取决于一个,而是有一个False则返回False
        """
        mode.lower()
        if mode not in ["a", "all", "r", "w"]:
            log.error(f"mode not a, all, r, w\\{mode=}")
            return False
        elif mode == "all":
            mode = "a"

        if mode in ["a", "r"]:
            if self._interpreter_r is None or not callable(self._interpreter_r):
                return False
        if mode in ["a", "w"]:
            if self._interpreter_w is None or not callable(self._interpreter_w):
                return False

        return True

    def interpreter(
            self,
            v: Any,
            mode: str = "r",
    ) -> ReturnValue[Any]:
        """
        :param v:
        :param mode:有两种模式,r,w,分别调用不同的解析器
        """
        mode = mode.lower()
        if not self._interpreter_check(mode=mode):
            log.error("interpreter check failed")
            return ReturnValue(False)

        try:
            match mode:
                case "r":
                    v = self._interpreter_r(v)
                case "w":
                    v = self._interpreter_w(v)
                case _:
                    log.error(f"not mode\\{mode=}")
                    return ReturnValue(False)

            return ReturnValue(True, v)
        except Exception as e:
            self.log.error(f"{e}\\in interpreter")
            return ReturnValue(False)

    def set_interpreter_r(self, _interpreter) -> bool:
        """
        在设置解析器时请勿调用解析器,
        暂未实现多线程调用锁
        """
        _t = self._interpreter_r
        self._interpreter_r = _interpreter
        if not self._interpreter_check(mode="r"):
            self._interpreter_r = _t
            return False
        return True

    def set_interpreter_w(self, _interpreter) -> bool:
        """
        在设置解析器时请勿调用解析器,
        暂未实现多线程调用锁
        """
        _t = self._interpreter_w
        self._interpreter_w = _interpreter
        if not self._interpreter_check(mode="w"):
            self._interpreter_w = _t
            return False
        return True
