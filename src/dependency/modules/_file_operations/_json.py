import json
import os

from ._file import FileBaseClass


class Json(FileBaseClass):
    def load(
            self,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> dict | list | bool:
        """
        :param filename: 是否不带后缀决定于$add_file_ext
        :param filepath:
        :param encoding:
        :param add_file_ext: 用于决定是否添加.json后缀
        :return: False or file content
        """
        if not isinstance(filename, str):
            self.log.error(f"filename type not str\\{filename=}")
            return False
        elif not isinstance(filepath, str):
            self.log.error(f"filepath type not str\\{filepath=}")
            return False
        elif not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return False
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return False

        if add_file_ext:
            filename = f"{filename}.json"
        filepath = os.path.join(filepath, filename)
        file_content = self._fc.load(file_path=filepath, encoding=encoding)
        if file_content is False:
            return False

        # analysis
        try:
            file_content = json.loads(file_content)
        except Exception as e:
            self.log.error(f"{e}\\in json analysis")
            return False

        return file_content

    def dump(
            self,
            v: dict | list,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            ensure_ascii: bool = False,
            indent: int | str | None = 4,
            **kwargs
    ) -> bool:
        """
        :param v: 写入的数据
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :param ensure_ascii:
        :param indent:
        :return: 写入成功标志位
        """
        if not isinstance(v, dict) and not isinstance(v, list):
            self.log.error(f"v type not dict or list\\{v=}")
            return False
        elif not isinstance(filename, str):
            self.log.error(f"filename type not str\\{filename=}")
            return False
        elif not isinstance(filepath, str):
            self.log.error(f"filepath type not str\\{filepath=}")
            return False
        elif not isinstance(encoding, str):
            self.log.error(f"encoding type not str\\{encoding=}")
            return False
        elif not isinstance(add_file_ext, bool):
            self.log.error(f"add_file_ext type not bool\\{add_file_ext=}")
            return False
        elif not isinstance(ensure_ascii, bool):
            self.log.error(f"ensure_ascii type not bool\\{ensure_ascii=}")
            return False
        elif not isinstance(indent, int):
            self.log.error(f"indent type not int\\{indent=}")
            return False

        v = json.dumps(v, ensure_ascii=ensure_ascii, indent=indent)

        if add_file_ext:
            filename = f"{filename}.json"
        filepath = os.path.join(filepath, filename)
        file_content = self._fc.dump(v, file_path=filepath, encoding=encoding)
        if not file_content:
            return False
        return True

