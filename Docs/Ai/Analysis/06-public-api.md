> [!INFO]
> 文档：公共 API 清单  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 依据：各包 `__init__.py` 和 `__all__`

# 公共 API

## 顶层 `dependency`

顶层只转发 `_foundation` 的 `__all__`：

```python
from dependency import Json, Log, LogProtocol, log_path, os_name, work_directory
```

注意：这里的 `Json` 是基础层旧实现，不是 `_file_operations.Json`。

## 功能模块

| 导入路径 | 明确导出 |
| --- | --- |
| `dependency.modules._error_handling` | `MEH`, `ReturnValue` |
| `dependency.modules._file_operations` | `BaseClass`, `PathTools`, `File`, `FileBaseClass`, `Interpreter`, `CSV`, `Ini`, `Json`, 可选 `Toml` |
| `dependency.modules._pygame` | `Music`, `Sound`, `Image`, `Font`, `Key`, `MouseButton`, `Window` |
| `dependency.modules._pyside6` | `Window`, `App`, `UiFile`, `ComponentProtocol`, `Widget`, `Button`, `UICH`, `UICHTextEdit` |
| `dependency.modules._SQLite3` | `SQLite` |
| `dependency.modules._tkinter` | `Window`, `TKComponent` 和版本元数据 |
| `dependency.modules._QR` | `QR` |

## API 一致性

当前公共接口存在以下差异：

- 命名风格混合：`_QR`、`_SQLite3` 使用大写，其他模块小写。
- 返回风格混合：对象、`bool`、`False`、`ReturnValue`、`MEH` 和异常并存。
- 日志参数混合使用 `log`、`_log`。
- 文件参数混合使用 `file_name`/`filename` 和 `file_path`/`filepath`。
- PySide6 实现了大量 `UICH*` 类，但包入口只导出其中两个。
- PySide6 的 `Message` 类存在，但未列入公共导出。
- `Font.bilt` 疑似为 `blit` 的拼写变体。

## 稳定性建议

公共 API 应先定义以下契约：

1. 成功和失败的统一返回模型。
2. 文件名、路径、日志参数的统一命名。
3. 模块命名的大小写规则。
4. `__all__` 中哪些对象属于稳定 API。
5. 异常是否被捕获以及错误对象如何传播。

