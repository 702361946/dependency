#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

log_path: str
log_levels: dict[str, int]
log_output_replace_identifications: set[str]
lori = log_output_replace_identifications


class Log:
    def __init__(
            self,
            log_sign: str = "default",
            log_level: int = 1,
            log_output_to_console: bool = False,
            log_output_format: tuple[list[str], str] = (
                    ["time", "sign", "level", "message"],
                    ";"
            ),
            log_output_to_file_path: str = f"{log_path}_.log",
            log_output_to_file_mode: str = "w",
            log_output_to_file_encoding: str = "utf-8",
            log_output_time_format: str = "%Y-%m-%d %H:%M:%S",
            get_code_file_and_line: bool = False,
            get_code_len: int = 0,
            color: dict[str, tuple[int, int, int] | bool] | None = None
    ):
        """
        替换标识支持:time,sign,level,message,
        其中message请务必带上,否则无法输出消息内容

        :param log_sign: 日志标识
        :param log_level: 日志等级,对应log_levels,只会输出大于等于的
        :param log_output_to_console: 是否输出到控制台
        :param log_output_format: 输出格式,索引0为替换标识,索引1为分隔符
        :param log_output_to_file_path: 输出到文件的路径,需要带上文件名及后缀
        :param log_output_to_file_mode: 输出到文件的模式,只支持w,a
        :param log_output_to_file_encoding: 输出到文件的编码
        :param log_output_time_format: 输出时间的格式(格式与datetime一致)
        :param get_code_file_and_line: 获取调用log的地址
        :param get_code_len: 获取长度(不含Log类),为0时为全部
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
        self.color = color or {"open": False}
        self.colorama = None
        ...

    def level_if(self, level: str) -> bool:
        """
        检查是否可以输出日志
        :param level: 请求等级
        :return: T/F
        """
        ...

    def message_color(self, message: str, color: str) -> str: ...

    def output_color(self, level: str, message="") -> bool: ...

    def output(self, level: str, message = "") -> bool:
        """
        输出
        :param level:
        :param message:
        :return:
        """
        ...

    def debug(self, message = "") -> bool: ...

    def info(self, message = "") -> bool: ...

    def warning(self, message = "") -> bool: ...

    def error(self, message = "") -> bool: ...

    def critical(self, message = "") -> bool: ...

    def save(self, message = "", level: str = "DEBUG") -> bool: ...

    def dict_config(self) -> dict[str, int | bool | str | tuple[list[str], str]]: ...