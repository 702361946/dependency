import os
import tomlkit
from .config import *
from ._file import File

fc = File()

class Toml(BaseClass):
    def load(
            self,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            _fc: File = fc,
    ) -> dict | bool:
        """
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :param _fc:
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
        elif not isinstance(_fc, File):
            self.log.error(f"_fc type not File\\{_fc=}")
            return False

        if add_file_ext:
            filename = f"{filename}.toml"
        filepath = os.path.join(filepath, filename)
        file_content = fc.load(file_path=filepath, encoding=encoding)
        if file_content is False:
            return False

        # analysis
        try:
            file_content = tomlkit.loads(file_content)
        except Exception as e:
            self.log.error(f"{e}\\in toml analysis")
            return False

        return file_content

    def dump(
            self,
            v: dict | list,
            filename: str,
            filepath: str = ".",
            encoding: str = "UTF-8",
            add_file_ext: bool = True,
            _fc: File = fc,
    ) -> bool:
        """
        :param v: 写入的数据
        :param filename:
        :param filepath:
        :param encoding:
        :param add_file_ext:
        :param _fc:
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
        elif not isinstance(_fc, File):
            self.log.error(f"_fc type not File\\{_fc=}")
            return False

        v = tomlkit.dumps(v)

        if add_file_ext:
            filename = f"{filename}.toml"
        filepath = os.path.join(filepath, filename)
        file_content = fc.dump(v, file_path=filepath, encoding=encoding)
        if not file_content:
            return False
        return True


