#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

import json
import os

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

    def dump(self, a, file_name: str, file_path: list[str] | str | None = None) -> bool:
        """
        写入文件
        :param a: 要写入的内容
        :param file_name: 要写入的文件名,不带后缀
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

            # 目录补全
            os.makedirs(os.path.dirname(f'{file_path}.json'), exist_ok=True)

            with open(
                    f'{file_path}.json',
                    'w',
                    encoding=self.encoding
            ) as f:
                # noinspection PyTypeChecker
                json.dump(a, f, indent=self.indent, ensure_ascii=self.ensure_ascii)
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

    def log_get(self) -> None:
        """
        打印到日志中
        """
        self.log.info('log_get\n')
        self.log.info(f'file_path:{self.file_path}')
        self.log.info(f'encoding:{self.encoding}')
        self.log.info(f'indent:{self.indent}')
        self.log.info(f'ensure_ascii:{self.ensure_ascii}')
        self.log.info('END\n')
