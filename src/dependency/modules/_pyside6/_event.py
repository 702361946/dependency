#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QEvent

from modules._file_operations import ReturnValue
from .config import *


class BindEvent:
    def __init__(self, _log = log):
        self.log = _log
        self.all_e_t: dict[int, int] = dict()
        self.binds = dict()
        """
        {
            "name": {
                "event_type": QEvent.Type.*.value,
                "callback_function": Callable[[QEvent, ...], Any],
                "end_event": bool
            },
        }
        """

    def __add_et(self, event_type: int):
        """添加事件类型引用计数"""
        self.all_e_t[event_type] = self.all_e_t.get(event_type, 0) + 1

    def __un_et(self, event_type: int):
        """减少事件类型引用计数"""
        if event_type not in self.all_e_t:
            return

        self.all_e_t[event_type] -= 1
        if self.all_e_t[event_type] <= 0:
            del self.all_e_t[event_type]

    def bind_event(
            self,
            name: str,
            event_type: QEvent.Type,
            callback_function: Callable[[QEvent], Any],
            end_event: bool = False
    ) -> ReturnValue[None]:
        """
        :param name:
        :param event_type:
        :param callback_function: 回调函数, 要求第一个位置必须是QEvent参
        :param end_event: 结束事件传播(True会调用.accept())
        """
        if not isinstance(name, str):
            self.log.error(f"name type not str\\{type(name)}")
            return ReturnValue(False, TypeError(f"name type not str\\{type(name)}"))
        if not callable(callback_function):
            self.log.error("callback_function must be callable")
            return ReturnValue(False, TypeError("callback_function must be callable"))

        if isinstance(event_type, QEvent.Type):
            event_type = event_type.value

        self.binds[name] = {
            "event_type": event_type,
            "callback_function": callback_function,
            "end_event": end_event
        }
        self.__add_et(event_type)

        return ReturnValue(True)

    def unbind_event(
            self,
            name: str
    ) -> ReturnValue[None]:
        """
        :param name:
        """
        try:
            r = self.binds.pop(name)
        except KeyError as e:
            self.log.warning(f"unbind event {name}, key not found")
            return ReturnValue(True, e)

        self.__un_et(r["event_type"])

        return ReturnValue(True)

    def traversal_event(
            self,
            events: list[QEvent]
    ) -> ReturnValue[list[tuple[str, Exception]]]:
        """
        :param events:
        """
        if isinstance(events, QEvent):
            events = [events]
        elif not isinstance(events, list):
            return ReturnValue(
                False,
                TypeError(f"events must be list or QEvent, got {type(events)}")
            )

        r_b = True
        r_e = []
        for event in events:
            if event.type() not in self.all_e_t:
                continue

            for i in self.binds.items():
                if i[1]["event_type"] != event.type():
                    continue
                try:
                    i[1]["callback_function"](event)
                    if i[1]["end_event"]:
                        event.accept()
                        break

                except Exception as e:
                    r_b = False
                    r_e.append((i[0], e))
                    self.log.error(
                        f"Callback '{i[0]}' "
                        f"failed for event {event}: {type(e).__name__}: {e}"
                    )

        return ReturnValue(r_b, r_e)

    def get_value(self, name) -> ReturnValue[dict[str, Any]]:
        """
        根据name返回value
        :param name:
        :return:
        """
        if name not in self.binds:
            return ReturnValue(False, ValueError(f"bind event {name} not found"))
        return ReturnValue(True, self.binds[name])


class ObjectKeyEvent:
    def __init__(
            self,
            cls_be: BindEvent,
            _log = log,
            registry: dict[QEvent.Type, Callable[[QEvent], Any]] = None,
            cls_name = "default"
    ):
        self.log = _log
        self.cls_be = cls_be
        self.flag = 0
        self.all_bind_event_name: list[str] = []
        if registry is None:
            registry = dict()
        elif not isinstance(registry, dict):
            registry = dict()
            self.log.error("registry type not dict")
        self.registry: dict[QEvent.Type, Callable[[QEvent], Any]] = registry
        self.cls_name = cls_name

    def bind_event(
            self,
            event_type: QEvent.Type,
            end_event: bool = False,
            callback_function: Callable[[QEvent], Any] = None
    ) -> ReturnValue[str | None]:
        """

        :param event_type:
        :param end_event:
        :param callback_function: 传入的可执行对象会在绑定成功后被持久化至注册表!
        :return: 返回name,失败返回为Error
        """
        name = f"__{self.cls_name}_{self.flag}__"
        if event_type not in self.registry:
            self.log.error("No corresponding function")
            return ReturnValue(False, ValueError("No corresponding function"))

        if callback_function is None:
            callback_function = self.registry.get(event_type)

        if not callable(callback_function):
            self.log.error(f"callback_function is not callable")
            return ReturnValue(False, TypeError("callback_function is not callable"))

        r = self.oke_bind_event(
            name,
            event_type,
            callback_function,
            end_event
        )
        if r:
            self.flag += 1
            self.modify_registry(event_type, callback_function)
            return ReturnValue(True, name)
        return r

    @staticmethod
    def __none_def(qe: QEvent):
        ...

    def oke_bind_event(
            self,
            name: str,
            event_type: QEvent.Type,
            callback_function: Callable[[QEvent], Any],
            end_event: bool = False
    ) -> ReturnValue[str | None]:
        r = self.cls_be.bind_event(name, event_type, callback_function, end_event)
        if r:
            self.all_bind_event_name.append(name)

        return r

    def unbind_event(self, name: str) -> ReturnValue[None]:
        if name not in self.all_bind_event_name:
            self.log.warning("overstep authority, Does not exist in the binding list")
            return ReturnValue(
                False,
                Exception(f"overstep authority, Does not exist in the binding list")
            )

        r = self.cls_be.unbind_event(name)
        if r:
            self.all_bind_event_name.remove(name)

        return r

    def modify_registry(
            self,
            event_type: QEvent.Type,
            callback_function: Callable[[QEvent], Any]
    ) -> ReturnValue[None]:
        """
        绑定可执行对象至注册表
        :param event_type: 
        :param callback_function: 
        :return: 
        """
        if event_type not in self.registry:
            self.log.warning("Does not exist in the table")
            return ReturnValue(False, Exception("Does not exist in the table"))

        if not callable(callback_function):
            self.log.warning(f"callback_function is not callable")
            return ReturnValue(False, TypeError("callback_function is not callable"))

        self.registry[event_type] = callback_function
        return ReturnValue(True)

    def reset_registry(
            self,
            event_type: QEvent.Type
    ) -> ReturnValue[None]:
        """
        重置某一项注册表
        :param event_type:
        :return:
        """
        if event_type not in self.registry:
            self.log.warning("Does not exist in the table")
            return ReturnValue(False, Exception("Does not exist in the table"))

        self.registry[event_type] = self.__class__.__none_def
        return ReturnValue(True)

    def unbind_all_registry(
            self,
            event_type: QEvent.Type
    ) -> ReturnValue[int | None]:
        """
        卸载某项注册表的所有绑定
        :return:
        """
        if event_type not in self.registry:
            self.log.error("Does not exist in the table")
            return ReturnValue(False, Exception("Does not exist in the table"))

        all_remove = []
        for i in self.all_bind_event_name:
            r = self.cls_be.get_value(i)
            if r and r.v["event_type"] == event_type.value:
                all_remove.append(i)

        for i in all_remove:
            self.cls_be.unbind_event(i)
            self.all_bind_event_name.remove(i)

        return ReturnValue(True, len(all_remove))


class MouseEvent(ObjectKeyEvent):
    """
    鼠标特化
    """
    def __init__(self, cls_be: BindEvent, _log = log):
        super().__init__(
            cls_be=cls_be,
            _log=_log,
            cls_name="MouseEvent",
            registry={
                QEvent.Type.Wheel: self.__class__.__none_def,
                QEvent.Type.MouseMove: self.__class__.__none_def,
                QEvent.Type.MouseButtonPress: self.__class__.__none_def,
                QEvent.Type.MouseButtonRelease: self.__class__.__none_def,
                QEvent.Type.MouseButtonDblClick: self.__class__.__none_def,
                QEvent.Type.MouseTrackingChange: self.__class__.__none_def
            }
        )


class KeyEvent(ObjectKeyEvent):
    """
    键盘特化
    """
    def __init__(self, cls_be: BindEvent, _log = log):
        super().__init__(
            cls_be=cls_be,
            _log=_log,
            cls_name="KeyEvent",
            registry={
                QEvent.Type.KeyPress: self.__class__.__none_def,
                QEvent.Type.KeyRelease: self.__class__.__none_def,

                QEvent.Type.InputMethod: self.__class__.__none_def,

                QEvent.Type.Shortcut: self.__class__.__none_def,
                QEvent.Type.ShortcutOverride: self.__class__.__none_def,
            }
        )


class TouchEvent(ObjectKeyEvent):
    """
    触控特化
    """
    def __init__(self, cls_be: BindEvent, _log = log):
        super().__init__(
            cls_be = cls_be,
            _log=_log,
            cls_name="TouchEvent",
            registry={
                QEvent.Type.TouchEnd: self.__class__.__none_def,
                QEvent.Type.TouchBegin: self.__class__.__none_def,
                QEvent.Type.TouchUpdate: self.__class__.__none_def,
                QEvent.Type.TouchCancel: self.__class__.__none_def
            }
        )


class TabletEvent(ObjectKeyEvent):
    """
    数位板特化
    """
    def __init__(self, cls_be: BindEvent, _log = log):
        super().__init__(
            cls_be=cls_be,
            _log=_log,
            cls_name="TabletEvent",
            registry={
                QEvent.Type.TabletMove: self.__class__.__none_def,
                QEvent.Type.TabletPress: self.__class__.__none_def,
                QEvent.Type.TabletRelease: self.__class__.__none_def,
                QEvent.Type.TabletEnterProximity: self.__class__.__none_def,
                QEvent.Type.TabletLeaveProximity: self.__class__.__none_def
            }
        )
