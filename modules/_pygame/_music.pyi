#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
from ._get_package import *

log: Log

class Music(object):
    def __init__(
            self,
            *,
            store_music_file_path: str = "music",
            loop: bool = True,
            volume: float = 1.0,
            raise_error: bool = True,
            log: Log = log
    ):
        """
        status有三个值,Playing播放中,close关闭,Pause暂停

        :param store_music_file_path: 音乐文件的存储路径,无需./或.\\
        :param loop: 循环
        :param volume: 音量(0~1)
        :param raise_error: 触发错误
        :param log: 日志
        """
        self.log: Log = log
        self.file_path: str = os.path.join(
            os.getcwd(),
            store_music_file_path
        )
        self.audios: dict[str, str] = {}
        self.name: str | None = None
        self.volume: float = 1.0
        self.status: str = 'close'
        self.loop: bool = loop
        self.raise_error: bool = raise_error

    def get_music_path(
            self,
            name: str,
            path: list[str] | None = None
    ) -> str | bool:
        ...

    def play(
            self,
            name: str | None = None,
            path: list[str] | None = None,
            loop: bool | None = None
    ) -> bool:
        ...

    def stop(self) -> bool:...

    def pause(self) -> bool:...

    def unpause(self) -> bool:...

    def set_volume(self, volume: float) -> bool:...

    def logging_get(self) -> None:...
