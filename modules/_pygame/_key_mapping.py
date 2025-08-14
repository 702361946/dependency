#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

from typing import Any

import pygame.event

from ._get_package import *

log = Log(
    log_sign="key_mapping",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)


class Key:
    """
    所有键盘按键的按键名-按键id请查看key_mapping.md
    """
    id_key: dict[int, str] = {
        1073741882: "F1",
        1073741883: "F2",
        1073741884: "F3",
        1073741885: "F4",
        1073741886: "F5",
        1073741887: "F6",
        1073741888: "F7",
        1073741889: "F8",
        1073741890: "F9",
        1073741891: "F10",
        1073741892: "F11",
        1073741893: "F12",
        48: "0",
        49: "1",
        50: "2",
        51: "3",
        52: "4",
        53: "5",
        54: "6",
        55: "7",
        56: "8",
        57: "9",
        97: "a",
        98: "b",
        99: "c",
        100: "d",
        101: "e",
        102: "f",
        103: "g",
        104: "h",
        105: "i",
        106: "j",
        107: "k",
        108: "l",
        109: "m",
        110: "n",
        111: "o",
        112: "p",
        113: "q",
        114: "r",
        115: "s",
        116: "t",
        117: "u",
        118: "v",
        119: "w",
        120: "x",
        121: "y",
        122: "z",
        96: "`",
        39: "'",
        45: "-",
        92: "\\",
        61: "=",
        91: "[",
        93: "]",
        59: ";",
        44: ",",
        46: ".",
        47: "/",
        27: "Esc",
        9: "Tab",
        1073741881: "CapsLock",
        1073742051: "Windows",
        32: "Space",
        1073741925: "Menu",
        13: "Enter",
        8: "Back",
        1073742049: "LShift",
        1073742053: "RShift",
        1073742048: "LCtrl",
        1073742052: "RCtrl",
        1073742050: "LAlt",
        1073742054: "RAlt",
        1073741897: "Insert",
        127: "Delete",
        1073741898: "Home",
        1073741901: "End",
        1073741899: "PageUp",
        1073741902: "PageDown",
        1073741894: "PrintScreen",
        1073741895: "ScrollLock",
        1073741896: "Pause",
        1073741906: "Up",
        1073741905: "Down",
        1073741904: "Left",
        1073741903: "Right",
        1073741907: "NumLock",
        1073741912: "NumEnter",
        1073741922: "Num0",
        1073741913: "Num1",
        1073741914: "Num2",
        1073741915: "Num3",
        1073741916: "Num4",
        1073741917: "Num5",
        1073741918: "Num6",
        1073741919: "Num7",
        1073741920: "Num8",
        1073741921: "Num9",
        1073741908: "Num/",
        1073741909: "Num*",
        1073741910: "Num-",
        1073741911: "Num+",
        1073741923: "Num.",
    }
    key_function: dict[str, dict[str, dict[str, Any]]] = {}
    """
    {
        key_name: {
            down: {
                function: function,
                open: bool
            },
            up: {
                function: function,
                open: bool
            }
        }
    }
    """

    def __init__(self, *, log: Log = log):
        self.log = log
        self.cls = self.__class__
        self.key_function = {}

    def key_id_return_key_name(self, key_id: int) -> str | bool:
        """
        按键id返回按键名
        :param key_id: 按键id
        :return:
        """
        if key_id not in self.cls.id_key.keys():
            self.log.error(f"{key_id} not in id_key")
            return False

        return self.cls.id_key[key_id]

    def add_key_mapping(self, key: str | int, mode: str, _function, _open: bool = True) -> bool:
        """

        :param key: 按键或按键id
        :param mode: 模式, down: 按下, up: 松开
        :param _function: 可执行函数(可通过lambda表达式传入), 必须包含一个event参数, 用于传入pygame事件
        :param _open: 是否开启
        :return:
        """
        # key_id -> key_name
        if isinstance(key, int):
            t = self.key_id_return_key_name(key)
            if t is False:
                self.log.error(f"no key id {key}")
                return False
            key = str(t)

        if key not in self.cls.id_key.values():
            self.log.error(f"{key} not in key_mapping")
            return False
        elif mode not in ["down", "up"]:
            self.log.error(f"mode {mode} not down or up")
            return False

        if key not in self.key_function.keys():
            self.key_function[key] = {
                "down": {
                    "function": None,
                    "open": False
                },
                "up": {
                    "function": None,
                    "open": False
                }
            }

        self.key_function[key][mode] = {
            "function": _function,
            "open": _open
        }
        self.log.info(f"{mode} {key} mapping -> {_function}")
        return True

    def remove_key_mapping(self, key: str | int, mode: str) -> bool:
        """
        移除按键映射
        :param key: 按键或按键id
        :param mode: 模式, down: 按下, up: 松开
        :return:
        """
        if isinstance(key, int):
            t = self.key_id_return_key_name(key)
            if t is False:
                self.log.error(f"no key id {key}")
                return False
            key = str(t)

        if key not in self.key_function.keys():
            self.log.error(f"{key} has no mapping")
            return False

        elif mode not in ["down", "up"]:
            self.log.error(f"mode {mode} not down or up")
            return False

        self.key_function[key][mode] = {
            "function": None,
            "open": False
        }
        self.log.info(f"remove {mode} {key} mapping")
        return True

    def run_key_mapping(
            self,
            key: int | str,
            mode: str = "down",
            event: pygame.event.Event | None = None
    ) -> bool:
        """
        运行按键映射
        :param key: 按键或按键id
        :param mode: 模式, down: 按下, up: 松开
        :param event: pygame事件,用于传入
        :return:
        """
        if isinstance(key, int):
            t = self.key_id_return_key_name(key)
            if t is False:
                self.log.error(f"no key id {key}")
                return False
            key = str(t)

        if mode not in ["down", "up"]:
            self.log.error(f"mode {mode} not down or up")
            return False

        elif key not in self.key_function.keys():
            self.log.error(f"{key} has no mapping")
            return False

        elif self.key_function[key][mode]["open"] is False:
            self.log.info(f"{key} {mode} mapping is closed")
            return False

        elif self.key_function[key][mode]["function"] is None:
            self.log.error(f"{key} {mode} mapping is None")
            return False

        try:
            self.key_function[key][mode]["function"](event=event)
            self.log.info(f"{key} {mode} mapping run")
            return True

        except TypeError:
            self.log.error(f"The mapping type of {key} in {mode} mode is not a function")
            return False


class MouseButton(Key):
    """
    所有鼠标按键的按键名-按键id请查看key_mapping.md

    由于鼠标侧键各种各样,
    建议手动适配不同鼠标的侧键(6+)
    """
    id_key: dict[int, str] = {
        1: "Left",
        2: "Middle",
        3: "Right",
        4: "MiddleUp",
        5: "MiddleDown",
        6: "SideButton_Back",
        7: "SideButton_Forward"
    }
