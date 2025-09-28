#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

from ._log import Log

log: Log

class Json(object):
    def __init__(
            self,
            file_path: str = 'json',
            encoding: str = 'utf-8',
            indent: int = 4,
            ensure_ascii: bool = False,
            log: Log = log
    ):
        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.log = log
        ...

    def dumps(self, a) -> str | bool:
        ...

    def dump(self, a, file_name: str, file_path: list[str] | str | None = None) -> bool:
        ...

    def load(self, file_name: str, file_path: list[str] | str | None = None) -> dict | list | bool:
        ...

    def loads(self, a) -> dict | list | bool:
        ...
