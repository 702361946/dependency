#  Copyright (c) 2025-2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import inspect
import os
from datetime import datetime

from ._os_name_get import os_name, work_directory

# 貌似需要使用模板重构Log了

match os_name[0]:
    case "nt":
        log_path = ".\\log\\"
    case _:
        log_path = "./log/"

class Log:
    log_levels = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4
    }
    log_output_replace_identifications = {
        "time",
        "sign",
        "level",
        "message",
        "code"
    }
    lori = log_output_replace_identifications
    log_level_color = {
        "DEBUG": 34,
        "INFO": 37,
        "WARNING": 33,
        "ERROR": 31,
        "CRITICAL": 91
    }

    def __init__(
            self,
            log_sign: str = "default",
            log_level: int = 1,
            log_output_to_console: bool = False,
            log_output_format: tuple[list[str], str] = (
                    ["time", "sign", "code", "level", "message"],
                    ";"
            ),
            log_output_to_file_path: str = f"{log_path}_.log",
            log_output_to_file_mode: str = "w",
            log_output_to_file_encoding: str = "utf-8",
            log_output_time_format: str = "%Y-%m-%d %H:%M:%S",
            get_code_file_and_line: bool = False,
            get_code_len: int = 0,
            start_color: bool = False,
    ):
        """
        替换标识支持:time,sign,level,message,code
        其中message请务必带上,否则无法输出消息内容

        :param log_sign: 日志标识
        :param log_level: 日志等级,对应log_levels,只会输出大于等于的
        :param log_output_to_console: 是否输出到控制台
        :param log_output_format: 输出格式,索引0为替换标识,索引1为分隔符
        :param log_output_to_file_path: 输出到文件的路径,需要带上文件名
        :param log_output_to_file_mode: 输出到文件的模式,只支持w,a
        :param log_output_to_file_encoding: 输出到文件的编码
        :param log_output_time_format: 输出时间的格式(格式与datetime一致)
        :param get_code_file_and_line: 获取调用log的地址
        :param get_code_len: 获取长度(不含Log类),为0时为全部
        :param start_color: 启用颜色
        """
        self.sign = str(log_sign)
        self.level = int(log_level)
        self.otc = bool(log_output_to_console)
        self.of = log_output_format
        self.otfp = str(log_output_to_file_path)
        self.otfm = str(log_output_to_file_mode)
        self.otfe = str(log_output_to_file_encoding)
        self.otf = str(log_output_time_format)
        self.gcfal = bool(get_code_file_and_line)
        self.gcl = get_code_len
        self.start_color = bool(start_color)

        # 格式化of
        t = []
        for i in self.of[0]:
            if i in self.__class__.lori:
                t.append(i)
            else:
                print(f"未知替换符:{i}")
        self.of = (t, str(self.of[1]))

        # 后缀补全
        if self.otfp[-4:] != ".log":
            self.otfp += ".log"

        if self.otfm not in ["w", "a"]:
            print(f"未知模式:{self.otfm}\n已自动设置为w")
            self.otfm = "w"

        os.makedirs(os.path.split(self.otfp)[0], exist_ok=True)

        if self.otfm == "w":
            with open(self.otfp, "w", encoding=self.otfe) as f:
                f.write("")

    def level_if(self, level: str) -> bool:
        """
        检查是否可以输出日志
        :param level: 请求等级
        :return: T/F
        """
        return self.__class__.log_levels.get(level, 5) >= self.level

    def output_console(
            self,
            message: str = "",
            level: str = "Info",
    ):
        if self.otc:
            if self.start_color:
                message = (f"\033["
                           f"{self.__class__.log_level_color.get(level, 37)}m"
                           f"{message}"
                           f"\033[0m")

            print(message)

    def output(self, level: str, message: str = "") -> bool:
        """
        输出
        :param level:
        :param message:
        :return:
        """
        if not self.level_if(level):
            return False

        # 格式化输出
        t = ''
        for i in self.of[0]:
            match i:
                case "time":
                    t += f"{datetime.now().strftime(self.otf)}{self.of[1]}"
                case "sign":
                    t += f"{self.sign}{self.of[1]}"
                case "code":
                    if self.gcfal:
                        a = inspect.stack()
                        file_in = os.path.abspath(__file__)
                        v = 0
                        _t = ""
                        for frame in a:
                            if v >= self.gcl != 0:
                                break
                            f_name = str(frame.filename)
                            if f_name == file_in:
                                continue
                            f_name = f_name.replace(work_directory, ".")

                            f_line = frame.lineno

                            _t += f"{f_name}:{f_line},"
                            v += 1
                        _t = _t[:-1]  # 去掉最后的","
                        t += f"{_t}{self.of[1]}"

                case "level":
                    t += f"{level}{self.of[1]}"
                case "message":
                    t += f"{message}{self.of[1]}"

        t = t[:-1]

        self.output_console(message=t, level=level)

        with open(self.otfp, "a", encoding=self.otfe) as f:
            f.write(t + "\n")

        return True

    def debug(self, message="") -> bool:
        """
        输出DEBUG日志
        :param message:
        :return:
        """
        return self.output("DEBUG", message)

    def info(self, message="") -> bool:
        """
        输出INFO日志
        :param message:
        :return:
        """
        return self.output("INFO", message)

    def warning(self, message="") -> bool:
        """
        输出WARNING日志
        :param message:
        :return:
        """
        return self.output("WARNING", message)

    def error(self, message="") -> bool:
        """
        输出ERROR日志
        :param message:
        :return:
        """
        return self.output("ERROR", message)

    def critical(self, message="") -> bool:
        """
        输出CRITICAL日志
        :param message:
        :return:
        """
        return self.output("CRITICAL", message)

    def save(self, message="", level: str = "DEBUG") -> bool:
        """
        保存等级为self.level的日志,或手动输入
        :param level:
        :param message:
        :return:
        """
        if level is None:
            for i in self.__class__.log_levels.items():
                if i[1] == self.level:
                    return self.output(i[0], message)
        return self.output(level, message)

    def dict_config(self):
        return {
            "sign": self.sign,
            "level": self.level,
            "otc": self.otc,
            "of": self.of,
            "otfp": self.otfp,
            "otfm": self.otfm,
            "otfe": self.otfe,
            "otf": self.otf
        }
