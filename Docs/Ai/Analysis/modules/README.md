> [!INFO]
> 文档：功能模块索引  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules`

# 功能模块索引

功能模块不由顶层 `dependency` 自动导入，需要按模块路径显式使用。

| 源码模块               | 文档                         | 核心职责           | 外部依赖               |
|--------------------|----------------------------|----------------|--------------------|
| `_error_handling`  | [错误处理](error-handling.md)  | 结果对象、链式错误处理    | 无                  |
| `_file_operations` | [文件操作](file-operations.md) | 路径、文件、格式解析     | 可选 `tomlkit`       |
| `_pygame`          | [Pygame](pygame.md)        | 窗口、事件和媒体资源     | `pygame`           |
| `_pyside6`         | [PySide6](pyside6.md)      | 应用、窗口、组件、UI 文件 | `PySide6`          |
| `_QR`              | [QR](qr.md)                | 二维码生成和保存       | `qrcode`, `Pillow` |
| `_SQLite3`         | [SQLite3](sqlite3.md)      | SQLite 操作包装    | Python `sqlite3`   |
| `_tkinter`         | [Tkinter](tkinter.md)      | Tk 窗口和组件注册     | Python `tkinter`   |

## 共同结构

除 `_error_handling` 外，各模块大多包含重复的 `_get_package.py`：

1. 根据当前文件位置计算 `dependency` 目录。
2. 将目录追加到 `sys.path`。
3. 导入顶层 `_foundation`。

这不是稳定的包间依赖方式。模块内部应改用相对导入，并由 `dependency.modules` 明确定义父包。

## 共同质量状态

- 自动测试集中在 `_error_handling.MEH` 和 `_file_operations`。
- 其他模块只完成了源码导入烟雾验证。
- 多数模块创建独立日志器，导入时可能产生文件 I/O。
- 公共返回值和异常策略不统一。

