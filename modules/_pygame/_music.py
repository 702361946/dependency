#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import pygame
from ._get_package import *

log = Log(
    log_sign="pygame.music",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)


# 音乐
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
        self.log = log
        self.log.info('__init__\n'
                      f'file_path:{store_music_file_path}\n'
                      f'loop:{loop}\n'
                      f'volume:{volume}\n'
                      f'raise_error:{raise_error}\n')

        self.file_path = os.path.join(
            os.getcwd(),
            store_music_file_path
        )

        # 遍历文件,建立字典
        self.audios = {}
        for root, dirs, files in os.walk(self.file_path):
            for file in files:
                # 获取基于存储路径的相对路径
                rel_path = os.path.relpath(root, self.file_path)
                if rel_path == '.':
                    key = file
                else:
                    key = f"{rel_path.replace(os.sep, '.')}.{file}"
                self.audios[key] = os.path.join(root, file)

        self.name: str | None = None
        self.volume: float = volume
        self.status: str = 'close'
        self.loop = loop
        self.raise_error = raise_error

        pygame.mixer.init()

        self.set_volume(volume)

        self.log.info('__init__ ok\n')

    def get_music_path(
            self,
            name: str,
            path: list[str] | None = None
    ) -> str | None:
        """
        获取音乐文件
        :param path: 基于存储路径的相对路径,顺序拼接
        :param name: 文件名,需带后缀
        :return:
        """
        self.log.info(f"get_music\\path:{path}\\name:{name}")

        if name is None:
            self.log.error('name is None')
            if self.raise_error:
                raise ValueError('name is None')
        elif type(name).__name__ != 'str':
            self.log.error('name type not str')
            if self.raise_error:
                raise TypeError('name type not str')

        if type(path).__name__ != 'list' and path is not None:
            if type(path).__name__ == 'str':
                # mypy error: List item 0 has incompatible type "list[str]"; expected "str"  [list-item]
                path = [str(path)]
            else:
                self.log.error(f'path type not list and not str\\type: {type(path)}')
                if self.raise_error:
                    raise TypeError(f'path type not list and not str\\{type(path)=}')

        if path is not None:
            t = ""
            for i in path:
                t = f"{t}.{i}"
            t = f"{t}.{name}"
        else:
            t = name

        t = self.audios.get(t, ".ERROR.ERROR.ERROR.")
        if t == ".ERROR.ERROR.ERROR.":
            self.log.error(f'no music:{t}')
            if self.raise_error:
                raise ValueError(f'no music:{t}')
            return None

        self.log.info(f"get path: {t}")

        return t

    def play(
            self,
            name: str | None = None,
            path: list[str] | None = None,
            loop: bool | None = None
    ) -> bool:
        """
        播放歌曲
        """
        self.log.info(f'play\\name:{name}\\path:{path}\\loop:{loop}')

        if self.name is None and name is None:
            self.log.error('name is None')
            if self.raise_error:
                raise ValueError('name is None')
            return False

        music_path: str | None = self.get_music_path(str(name), path)
        if music_path is not None:
            pygame.mixer.music.load(music_path)
            try:
                if self.loop is True:
                    pygame.mixer.music.play(-1)
                    self.status = 'playing'

                elif self.loop is False:
                    pygame.mixer.music.play()
                    self.status = 'playing'

                else:
                    self.log.error('loop type not bool')
                    if self.raise_error:
                        raise TypeError('loop type not bool')
                    return False

                if name is not None:
                    self.name = name
                if loop is not None:
                    self.loop = loop

            except pygame.error as e:
                self.log.error(f'pygame error:{e}')
                if self.raise_error:
                    raise pygame.error(e)
                return False

            return True
        else:
            self.log.error(f'not music file\\name:{name}\\path:{path}')
            if self.raise_error:
                raise ValueError(f'no music:{music_path}\\name:{name}')
            return False

    def stop(self) -> bool:
        """
        将会完全停止播放并从内存中释放!
        """
        self.log.info('stop')
        pygame.mixer.music.stop()
        self.status = 'close'
        return True

    def pause(self) -> bool:
        """
        暂停
        """
        self.log.info('pause')
        if self.status != 'playing':
            self.log.info('status not playing')
            if self.raise_error:
                raise ValueError('status not playing')
            return False

        else:
            pygame.mixer.music.pause()
            self.status = 'pause'
            return True

    def unpause(self) -> bool:
        """
        恢复播放
        """
        self.log.info('unpause')
        if self.status != 'pause':
            self.log.info('status not pause')
            if self.raise_error:
                raise ValueError('status not pause')
            return False
        else:
            pygame.mixer.music.unpause()
            self.status = 'playing'
            return True

    def set_volume(self, volume: float) -> bool:
        """
        volume传入的float应在0~1之间
        """
        self.log.info(f'set_volume\\volume:{volume}')
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)
            return True
        else:
            self.log.error('volume in 0.0 ~ 1.0')
            if self.raise_error:
                raise ValueError(f'volume in 0.0~1.0 not {volume}')
            return False
