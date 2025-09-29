#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
from typing import Optional

import qrcode
from qrcode.main import GenericImage

from ._get_package import *

log = Log(
    log_sign="QR",
    log_output_to_file_path=f"{log_path}QR.log",
    log_output_to_file_mode="w"
)


class QR:
    def __init__(
            self,
            version: int | None = None,
            error_correction: int = 0,
            box_size: int = 10,
            border: int = 4,
            image_factory: Optional[type[GenericImage]] | None = None,
            mask_pattern: int | None = None,
            *,
            log: Log = log
    ):
        """

        :param version: 1 ~ 40 or None
        :param error_correction: \
        ``0:ERROR_CORRECT_M`` \
        ``1:ERROR_CORRECT_L`` \
        ``2:ERROR_CORRECT_H`` \
        ``3:ERROR_CORRECT_Q``
        :param box_size: 像素大小,
        :param border: QR距离图片边缘距离(像素)
        :param image_factory: 生成图像的工厂类
        :param mask_pattern: 掩码, 0~7
        """
        self.log = log
        if version is not None:
            if not isinstance(version, int):
                self.log.error("version type is not int")
                raise TypeError("version type is not int")

        if not isinstance(error_correction, int):
            self.log.error("error_correction type is not int")
            raise TypeError("error_correction type is not int")
        elif not 0 <= error_correction <= 3:
            self.log.error("error_correction value is not in 0 ~ 3")
            raise TypeError("error_correction value is not in 0 ~ 3")

        if not isinstance(box_size, int):
            self.log.error("box_size type is not int")
            raise TypeError("box_size type is not int")
        elif box_size <= 0:
            self.log.error("box_size value is not > 0")
            raise TypeError("box_size value is not > 0")

        if not isinstance(border, int):
            self.log.error("border type is not int")
            raise TypeError("border type is not int")
        elif border < 0:
            self.log.error("border value is not >= 0")
            raise TypeError("border value is not >= 0")

        if mask_pattern is not None:
            if not isinstance(mask_pattern, int):
                self.log.error("mask_pattern type is not int")
                raise TypeError("mask_pattern type is not int")
            elif not 0 <= mask_pattern <= 7:
                self.log.error("mask_pattern value is not in 0 ~ 7")
                raise TypeError("mask_pattern value is not in 0 ~ 7")

        self.qr_class = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            image_factory=image_factory,
            mask_pattern=mask_pattern,
        )

    def generate(
            self,
            data: str,
            make: bool = False,
            fill_color: tuple[int, int, int] | tuple[int, int, int, int] | str | None = None,
            back_color: tuple[int, int, int] | tuple[int, int, int, int] | str | None = None,
    ) -> bool | GenericImage:
        """

        :param data: 数据
        :param make: 是否主动调整二维码大小(调用make方法)
        :param fill_color:
        :param back_color:
        """
        self.qr_class.add_data(data)

        if make:
            self.log.info("make QR size")
            self.qr_class.make()

        if fill_color is None:
            fill_color = (0, 0, 0)

        if back_color is None:
            back_color = (255, 255, 255)

        try:
            image = self.qr_class.make_image(fill_color=fill_color, back_color=back_color)
        except Exception as e:
            self.log.error(e)
            return False

        return image

    def save_image(self, image: GenericImage, file_path: str) -> bool:
        """

        :param image: QR图片
        :param file_path: 文件路径,必须带后缀
        """
        self.log.info("save QR image")
        try:
            image.save(file_path)
        except Exception as e:
            self.log.error(e)
            return False
        return True
