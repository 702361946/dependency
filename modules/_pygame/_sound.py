#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

import pygame
from ._get_package import *

log = Log(
    log_sign="pygame.sound",
    log_output_to_file_path=f"{log_path}pygame.log",
    log_output_to_file_mode="a"
)

# 音效
class Sound(object):
    def __init__(
            self,
            *,
            store_sound_file_path: str = "sound",
            volume: float = 1.0,
            raise_error: bool = True,
            log: Log = log
    ):
        self.log = log
        self.log.info('__init__\n'
                      f'file_path:{store_sound_file_path}\n'
                      f'volume:{volume}\n'
                      f'raise_error:{raise_error}\n')

        self.file_path = os.path.join(
            os.getcwd(),
            store_sound_file_path
        )

        # 遍历文件,建立字典
        self.sounds = {}
        for root, dirs, files in os.walk(self.file_path):
            for file in files:
                # 获取基于存储路径的相对路径
                rel_path = os.path.relpath(root, self.file_path)
                if rel_path == '.':
                    key = file
                else:
                    key = f"{rel_path.replace(os.sep, '.')}.{file}"
                self.sounds[key]: dict[str, str | pygame.mixer.Sound] = {
                    "path": os.path.join(root, file),
                    "sound": None
                }

        self.volume: float = volume
        self.raise_error = raise_error

        pygame.mixer.init()

        self.log.info('__init__ ok\n')

    def init_sound(self, sounds: list[str] | str) -> list[bool]:
        """
        用来初始化音效
        提交的内容示例

        self.file_path\\temp.mp3
        self.file_path\\temp\\temp.mp3
        如上的两个mp3文件,
        如果要加载,格式如下
        temp.mp3
        temp.temp.mp3

        总之就是去掉.\\(./),\\(/)换成.

        """
        self.log.info(f'init_sound\\sounds:{sounds}')
        if type(sounds).__name__ != 'list':
            sounds = [str(sounds)]

        t = []
        for i in sounds:
            if i in self.sounds.keys():
                self.sounds[i]["sound"] = pygame.mixer.Sound(self.sounds[i]["path"])
                self.log.info(f'ok:{i}')
                t.append(True)
            else:
                self.log.error(f'no sound:{i}')
                if self.raise_error:
                    raise KeyError(f'no sound:{i}')
                t.append(False)

        return t

    def play(self, sound_name: str) -> bool:
        """
        播放音效
        """
        self.log.info(f'play\\name:{sound_name}')
        if sound_name not in self.sounds.keys():
            self.log.error(f'sounds no key:{sound_name}')
            if self.raise_error:
                raise KeyError(f'sounds no key:{sound_name}')
            return False

        elif self.sounds[sound_name]["sound"] is None:
            self.log.error(f"no init sound:{sound_name}")
            if self.raise_error:
                raise ValueError(f"no init sound:{sound_name}")
            return False

        else:
            self.sounds[sound_name]["sound"].play()
            return True

    def stop(self, sound_name: str) -> bool:
        """
        停止播放
        """
        self.log.info(f'stop\\name:{sound_name}')
        if sound_name not in self.sounds.keys():
            self.log.error(f'sounds no key:{sound_name}')
            if self.raise_error:
                raise KeyError(f'sounds no key:{sound_name}')
            return False

        elif self.sounds[sound_name]["sound"] is None:
            self.log.error(f"no init sound:{sound_name}")
            if self.raise_error:
                raise ValueError(f"no init sound:{sound_name}")
            return False

        else:
            self.sounds[sound_name]["sound"].stop()
            return True

    def set_volume(self, sound_name: str, volume: float) -> bool:
        """
        设置单体音效音量
        """
        self.log.info(f'set_volume\\name:{sound_name}\\volume:{volume}')
        if not 0 <= volume <= 1:
            self.log.error('volume not in 0~1')
            if self.raise_error:
                raise ValueError(f'volume in 0~1 not {volume}')
            return False

        elif sound_name not in self.sounds.keys():
            self.log.error(f'sounds no key:{sound_name}')
            if self.raise_error:
                raise KeyError(f'sounds no key:{sound_name}')
            return False

        elif self.sounds[sound_name]["sound"] is None:
            self.log.error(f"no init sound:{sound_name}")
            if self.raise_error:
                raise ValueError(f"no init sound:{sound_name}")
            return False

        else:
            self.sounds[sound_name]["sound"].set_volume(volume)
            return True
