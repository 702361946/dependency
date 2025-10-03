#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

import inspect
import os
from datetime import datetime
from pyclbr import Function
from string import Template
from typing import Optional, Any

from ._log_type import *
from ._os_name_get import os_name, work_directory

match os_name[0]:
    case "nt":
        log_path = ".\\log\\"
        os.makedirs(log_path, exist_ok=True)
    case _:
        log_path = "./log/"
        os.makedirs(log_path, exist_ok=True)


class LogTemplate:
    _levels = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR",
        4: "CRITICAL"
    }

    def __init__(
            self,
            sign: str = "default",
            level: int = 1,
            replace_logo: list[str] | None = None,
            replace_logo_template: dict[str, dict[str, Template | Function | str]] | None = None,
            outputs: Optional[OutputsConfig] | Optional[dict[str, Any]] | None = None,
            output_time_format: str = "%Y-%m-%d %H:%M:%S",

            **kwargs,
    ):
        """
        默认替换标识:time,sign,level,message,code
        其中message请务必带上,否则无法输出消息内容

        :param sign: 标识
        :param level: 等级, 对应请查看 ``cls._levels``
        :param replace_logo: 替换标识, 为replace_logo_func的key, 且顺序决定输出
        :param replace_logo_template: 替换标识所对应的模板、文本、颜色(未实装), \
        必有key为"template", 可含有以"parameter_"开头的参, 可对应一个函数
        :param outputs: 用于替换所有以log_output_以及get_code_开头的传入参
        :param output_time_format: 输出时间格式(datetime怎么来的就怎么来)
        """
        __all_message = []

        # outputs check
        _outputs = dict(
            file=dict(
                path=f"{log_path}_.log",
                mode="a",
                encoding="utf-8",
            ),
            time=lambda: datetime.now().strftime(output_time_format),
            console=False,
            code=dict(
                get=False,
                len=0,
                including_log=False,
            ),
            delimiter=";"
        )

        self.outputs = _outputs
        if outputs is not None:
            self.outputs.update(outputs)

            if self.outputs["file"].get("path", None) is None:
                self.outputs["file"]["path"] = f"{log_path}_.log"
                __all_message.append("no file path")

        self.sign = str(sign)
        self.level = int(level)

        if replace_logo is None:
            replace_logo = ["time", "sign", "code", "level", "message"]
            if not self.outputs["code"].get("get", False):
                replace_logo = ["time", "sign", "level", "message"]

        _replace_logo_template = {
            "time": {
                "template": Template("$time"),
            },
            "sign": {
                "template": Template("$sign")
            },
            "code": {
                "template": Template("$code"),
            },
            "level": {
                "template": Template("$level"),
            },
            "message": {
                "template": Template("$message"),
            }
        }
        if replace_logo_template is not None:
            _replace_logo_template.update(replace_logo_template)
            replace_logo_template = _replace_logo_template
        else:
            replace_logo_template = _replace_logo_template

        t = []
        for i, logo in enumerate(replace_logo):
            if logo not in replace_logo_template.keys():
                t.append(i)
                __all_message.append(f"replace logo no template\\{logo}")
        for i in sorted(t, reverse=True):
            del replace_logo[i]

        self.replace_logo = replace_logo
        self.replace_logo_template = replace_logo_template

        if self.outputs['file']['path'][-4:] != ".log":
            self.outputs['file']['path'] += ".log"

        if self.outputs['file']['mode'] not in ["w", "a"]:
            __all_message.append(f"未知模式:{self.outputs['file']['mode']}\n已自动设置为w")
            self.outputs['file']['mode'] = "w"

        os.makedirs(os.path.split(self.outputs['file']['path'])[0], exist_ok=True)

        if self.outputs["file"]["mode"] == "w":
            with open(
                    self.outputs["file"]["path"],
                    "w",
                    encoding=self.outputs["file"]["encoding"],
            ) as f:
                f.write("")

        if __all_message:
            with open(
                    f"{log_path}__log_message.log",
                    "w",
                    encoding="utf-8",
            ) as f:
                for i in __all_message:
                    f.write(f"{i}\n")

    def level_if(self, level: int) -> bool:
        """
        检查是否可以输出日志
        :param level: 请求等级
        :return: T/F
        """
        return level >= self.level

    def _get_code(self) -> str:
        a = inspect.stack()
        file_in = os.path.abspath(__file__)
        v = 0
        _t = ""
        for frame in a:
            # noinspection PyTypeChecker
            if v >= self.outputs["code"]["len"] != 0:
                break
            f_name = str(frame.filename)
            if f_name == file_in and not self.outputs["code"]["including_log"]:
                continue
            f_name = f_name.replace(work_directory, ".")

            f_line = frame.lineno

            _t += f"{f_name}:{f_line},"
            v += 1
        _t = _t[:-1]  # 去掉最后的","
        return _t

    def output(self, level: int, message: str = "") -> bool:
        """
        最终输出
        """
        if not self.level_if(level):
            return False

        t = ""
        for i in self.replace_logo:
            match i:
                case "time":
                    try:
                        t += self.replace_logo_template["time"]["template"].substitute(
                            time=self.outputs["time"]()
                        )
                    except TypeError:
                        t += self.outputs["time"]
                case "sign":
                    t += self.sign
                case "code":
                    if self.outputs["code"]["get"]:
                        t += self._get_code()
                case "level":
                    t += self.__class__._levels[level]
                case "message":
                    t += message
                case _:
                    _t = self.replace_logo_template[i]["template"]
                    __t = []
                    ___t = {}
                    for _i in self.replace_logo_template[i].keys():
                        if "parameter_" in _i:
                            __t.append(_i.replace("parameter_", "", 1))
                    for _i in __t:
                        if callable(self.replace_logo_template[i][f"parameter_{_i}"]):
                            # noinspection PyCallingNonCallable
                            ___t[_i] = self.replace_logo_template[i][f"parameter_{_i}"]()
                        else:
                            ___t[_i] = self.replace_logo_template[i][f"parameter_{_i}"]

                    try:
                        # noinspection PyUnresolvedReferences
                        t += self.replace_logo_template[i]["template"].substitute(___t)
                    except KeyError:
                        t += self.replace_logo_template[i]["template"]

            t += self.outputs["delimiter"]

        t = t[:-1]

        if self.outputs["console"]:
            print(t)

        with open(
                self.outputs["file"]["path"],
                "a",
                encoding=self.outputs["file"]["encoding"],
        ) as f:
            f.write(t + "\n")

        return True

    def debug(self, message="") -> bool:
        """
        输出DEBUG日志
        :param message:
        :return:
        """
        return self.output(0, message)

    def info(self, message="") -> bool:
        """
        输出INFO日志
        :param message:
        :return:
        """
        return self.output(1, message)

    def warning(self, message="") -> bool:
        """
        输出WARNING日志
        :param message:
        :return:
        """
        return self.output(2, message)

    def error(self, message="") -> bool:
        """
        输出ERROR日志
        :param message:
        :return:
        """
        return self.output(3, message)

    def critical(self, message="") -> bool:
        """
        输出CRITICAL日志
        :param message:
        :return:
        """
        return self.output(4, message)

    def save(self, message="", level: int = 0) -> bool:
        """
        保存等级为self.level的日志,或手动输入
        :param level:
        :param message:
        :return:
        """
        return self.output(level, message)
