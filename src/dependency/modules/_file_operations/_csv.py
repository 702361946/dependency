import csv
import io
import os

from ._file import FileBaseClass

class CSV(FileBaseClass):
    def load(
            self,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> list[list] | bool:
        """
        :param filename: 是否不带后缀决定于$add_file_ext
        :param filepath:
        :param encoding:
        :param add_file_ext: 用于决定是否添加.csv后缀
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
            filename = f"{filename}.csv"
        filepath = os.path.join(filepath, filename)
        file_content = self._fc.load(file_path=filepath, encoding=encoding)
        if file_content is False:
            return False

        # analysis
        try:
            buffer = io.StringIO(file_content)
            file_content = list(csv.reader(buffer))
        except Exception as e:
            self.log.error(f"{e}\\in csv analysis")
            return False

        return file_content

    def dump(
            self,
            v: list[list],
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            **kwargs
    ) -> bool:
        """
        :param v: 写入的数据
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :return: 写入成功标志位
        """
        if not isinstance(v, list):
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

        try:
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(v)
            v = buffer.getvalue()
            # 紧凑化
            t = ""
            for i in v.split("\r\n"):
                if not i:
                    continue
                t += i + "\n"
            v = t[:-1] # -1用来删掉最后的\n
        except Exception as e:
            self.log.error(f"{e}\\in list[list] to csv")
            return False

        if add_file_ext:
            filename = f"{filename}.csv"
        filepath = os.path.join(filepath, filename)
        file_content = self._fc.dump(v, file_path=filepath, encoding=encoding)
        if not file_content:
            return False
        return True
