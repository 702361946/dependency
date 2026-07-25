> [!INFO]
> 文档：`_pyside6` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_pyside6`

# `_pyside6`

## 职责

该模块封装 Qt 应用、主窗口、`.ui` 文件加载、基础组件，以及大量控件值的安全读取和设置。

## 公共 API

- `App`
- `Window`
- `UiFile`
- `ComponentProtocol`
- `Widget`
- `Button`
- `UICH`
- `UICHTextEdit`

实现中还存在 `Message` 和多个 `UICH*` 子类，但没有全部从包入口导出。

## 子系统

### `App`

- 复用或创建 `QApplication`。
- 从当前工作目录下的 `language/<语言>.qm` 加载翻译。
- 运行事件循环、关闭窗口和显示 UI。

### `Window`

包装 `QMainWindow`，提供标题、尺寸、图标、透明度、窗口状态、显示关闭和状态栏消息。

### `UiFile`

使用共享 `QUiLoader` 加载 `.ui` 文件，以 `MEH[QWidget]` 返回成功或错误。

### `Widget`、`Button`、`Message`

对 Qt 组件常用属性提供布尔返回的 setter/getter 包装。

### `UICH` 系列

`_ui_control_handling.py` 约 1745 行，覆盖：

- 通用 QWidget 调用。
- 数值控件。
- 日期、时间和日期时间。
- LineEdit、TextEdit。
- SpinBox、DoubleSpinBox。
- Dial、Slider、ScrollBar。
- KeySequenceEdit。

大部分方法通过 `MEH` 返回调用结果。

## 风险

- `_ui_file.py` 和 `_ui_control_handling.py` 使用顶层 `modules._error_handling` 导入。
- 最大实现文件过大，重复逻辑多。
- `App` 的语言文件路径依赖当前工作目录。
- 翻译加载失败分支会再次加载同一个失败路径。
- `Window` 尺寸文档写作 `(h, w)`，实现和默认值实际表现为 `(w, h)`。
- `Message` 和多数 `UICH*` 类未纳入明确公共 API。
- 没有 GUI 测试或无头测试配置。
- 包装层同时使用 `bool` 和 `MEH`，调用体验不一致。

## 建议

按控件族拆分 `UICH` 文件，抽取统一的安全调用模板，并通过相对导入连接错误处理模块。对应用和窗口层使用 Qt offscreen 平台建立最小测试。

