#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
from typing import TypedDict, Callable, Union


# Log.__init__.outputs
# 定义嵌套的 TypedDict
class FileConfig(TypedDict):
    path: str
    mode: str
    encoding: str


class CodeConfig(TypedDict):
    get: bool  # 是否获取
    len: int  # 获取长度
    including_log: bool  # 包含Log类源文件


# 定义主 TypedDict
class OutputsConfig(TypedDict, total=False):
    file: FileConfig
    time: Union[Callable[[], str], str]
    console: bool  # 打印至控制台开关
    code: CodeConfig
    delimiter: str
