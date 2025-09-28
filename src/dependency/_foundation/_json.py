#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

import json
import os
from typing import Any

from ._log import Log, log_path

log = Log(
    log_sign="json",
    log_output_to_file_path=f"{log_path}_.log",
    log_output_to_file_mode="w"
)


class Json(object):
    def __init__(
            self,
            file_path: str = 'json',
            encoding: str = 'utf-8',
            indent: int = 4,
            ensure_ascii: bool = False,
            log: Log = log
    ):
        self.log = log
        if type(indent).__name__ != 'int':
            self.log.error('indent type not int')
            raise TypeError('indent type not int')
        if type(ensure_ascii).__name__ != 'bool':
            self.log.error('ensure_ascii type not bool')
            raise TypeError('ensure_ascii type not bool')

        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self.ensure_ascii = ensure_ascii

        self.log.info('init ok')

    def dumps(
            self,
            a: Any
    ) -> str | bool:
        """

        :param a: 要转换的内容
        :return: json
        """
        self.log.debug(f"dumps\\{a}")

        try:
            a = json.dumps(a, indent=self.indent, ensure_ascii=self.ensure_ascii)
        except Exception as e:
            self.log.error(f"{e}")
            return False

        self.log.debug(f"dumps r\\{a}")
        return a

    def dump(self, a, file_name: str, file_path: list[str] | str | None = None) -> bool:
        """
        写入文件
        :param a: 要写入的内容
        :param file_name: 要写入的文件名,可带后缀
        :param file_path: 中间的文件夹,如果没有请放空,在list里填文件夹名称,顺序拼接
        :return: True&False
        """
        self.log.info(f'w\nfile_path:{file_path}\nfile_name:{file_name}')
        try:
            if type(file_path).__name__ in ['list', 'str']:
                if type(file_path).__name__ != 'list':
                    file_path = [file_path]
                __t = self.file_path
                for _t in file_path:
                    __t = os.path.join(__t, str(_t))
                file_path = os.path.join(__t, file_name)
            elif file_path is None:
                file_path = os.path.join(self.file_path, file_name)
            else:
                raise TypeError('file_path type is list or str')

            if file_path[-5:] != ".json":
                file_path += ".json"

            # 目录补全
            os.makedirs(os.path.dirname(f'{file_path}'), exist_ok=True)

            with open(
                    f'{file_path}',
                    'w',
                    encoding=self.encoding
            ) as f:
                a = self.dumps(a)
                if a is False:
                    return False

                f.write(a)
                self.log.info('ok')
                return True
        except Exception as e:
            self.log.error(e)
            return False

    def load(self, file_name: str, file_path: list[str] | str | None = None):
        """
        读取文件
        :param file_name: 要写入的文件名,不带后缀
        :param file_path: 中间的文件夹,如果没有请放空,在list里填文件夹名称,顺序拼接
        :return: 文件内容&False
        """
        self.log.info(f'r\\file_name:{file_name}')
        try:
            if type(file_path).__name__ in ['list', 'str']:
                if type(file_path).__name__ != 'list':
                    file_path = [file_path]
                __t = self.file_path
                for _t in file_path:
                    __t = os.path.join(__t, str(_t))
                file_path = os.path.join(__t, file_name)
            elif file_path is None:
                file_path = os.path.join(self.file_path, file_name)
            else:
                raise TypeError('file_path type is list or str')

            if file_path[-5:] != ".json":
                file_path += ".json"

            with open(
                    f'{file_path}.json',
                    'r+',
                    encoding=self.encoding
            ) as f:
                a = json.load(f)
                self.log.info('ok')
                return a

        except Exception as e:
            self.log.error(e)
            return False

    def loads(self, a: str) -> dict | list | bool:
        """
        将文本json转为python对象
        :param a:
        :return:
        """
        self.log.debug(f"loads\\{a}")
        try:
            a = json.loads(a)
        except Exception as e:
            self.log.error(f"{e}")
            return False

        self.log.debug(f"loads r\\{a}")
        return a
