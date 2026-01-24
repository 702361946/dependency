#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from pathlib import Path

from .config import *

class PathTools:
    @staticmethod
    def str_to_path(text: str | Path, _log: Log = log) -> ReturnValue[Path]:
        if isinstance(text, Path):
            return ReturnValue(True, text)
        elif isinstance(text, str):
            return ReturnValue(True, Path(text))
        _log.error(f"text type not Path or str")
        return ReturnValue(False, TypeError("text type not Path or str"))

    @staticmethod
    def path_to_str(path: str | Path, _log: Log = log) -> ReturnValue[str]:
        try:
            return ReturnValue(True, str(path))
        except Exception as e:
            _log.error(f"{e}\\in PathTools.path_to_str")
            return ReturnValue(False, e)

    @staticmethod
    def join_paths(*paths: Path | str, _log: Log = log) -> ReturnValue[Path]:
        """
        顺序拼接所有路径
        """
        if len(paths) < 2:
            _log.error(f"Multiple paths are needed, not just one")
            return ReturnValue(False, ValueError("Multiple paths are needed, not just one"))

        try:
            result = PathTools.str_to_path(paths[0])
            if not result.ok:
                return ReturnValue(False, result)
            result = result.v

            for p in paths[1:]:
                p = PathTools.str_to_path(p)
                if not p.ok:
                    return ReturnValue(False, p)
                result /= p.v

            return ReturnValue(True, result)
        except TypeError as e:
            return ReturnValue(False, e)

    @staticmethod
    def mkdir(path: str | Path, _log: Log = log, **kwargs) -> ReturnValue[Exception | None]:
        """
        补全目录
        :return: RV(bool, None | ERROR)
        """
        path = PathTools.str_to_path(path)
        if not path.ok:
            return ReturnValue(False, path)
        path = path.v

        # 防止kwargs参数引发ERROR
        parents = kwargs.pop('parents', True)
        exist_ok = kwargs.pop('exist_ok', True)

        try:
            path.mkdir(parents=parents, exist_ok=exist_ok, **kwargs)
            return ReturnValue(True, None)
        except Exception as e:
            _log.error(f"{e}\\in PathTools.mkdir")
            return ReturnValue(False, e)
