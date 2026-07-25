> [!INFO]
> 文档：`_QR` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_QR`

# `_QR`

## 职责

该模块对 `qrcode.QRCode` 提供薄包装，负责参数校验、数据生成和图像保存。

## 公共 API

```python
from dependency.modules._QR import QR
```

### 构造参数

- `version`：二维码版本，允许 `None`。
- `error_correction`：0 到 3。
- `box_size`：每个模块的像素尺寸。
- `border`：边框宽度。
- `image_factory`：图像工厂。
- `mask_pattern`：0 到 7。
- `log`：日志器。

### 方法

- `generate(data, make=False, fill_color=None, back_color=None)`
- `save_image(image, file_path)`

## 数据流

```text
构造 QR
  └── add_data
      ├── 可选 make
      └── make_image
          └── GenericImage
              └── save_image
```

## 风险

- 同一个 `QR` 实例多次调用 `generate()` 会继续向同一个 `QRCode` 对象添加数据，状态不会自动清空。
- 参数值错误主要抛 `TypeError`，即使问题属于值范围。
- `generate()` 和 `save_image()` 以 `False` 表示运行时失败，和构造阶段异常风格不同。
- 没有测试覆盖颜色、版本、掩码、重复生成和文件保存。
- 模块名 `_QR` 的大小写与其他模块不一致。

## 建议

每次生成时创建新 `QRCode`，或提供明确的 `clear()`/复用语义。增加图像尺寸、二维码可解码性和重复调用测试。

