> [!INFO]
> 文档：架构与依赖关系  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 分析对象：包入口、内部依赖和运行时数据流

# 架构与依赖关系

## 分层模型

```text
使用者
├── import dependency
│   └── dependency._foundation
│       ├── OS / 工作目录
│       ├── Log / LogProtocol
│       └── 基础 Json
└── import dependency.modules._xxx
    ├── _error_handling
    ├── _file_operations
    ├── _pygame
    ├── _pyside6
    ├── _SQLite3
    ├── _tkinter
    └── _QR
```

顶层包没有聚合导出功能模块，因此可选依赖不会在普通 `import dependency` 时全部加载。这一方向合理，可以维持基础安装轻量。

## 内部依赖图

```text
_foundation
    ↑
    ├── 各模块的 _get_package.py
    ├── _pygame
    ├── _pyside6
    ├── _SQLite3
    ├── _tkinter
    ├── _QR
    └── _file_operations

_error_handling
    ↑
    ├── _file_operations 使用 ReturnValue
    └── _pyside6 使用 MEH
```

当前依赖方向本身基本单向，但实现方式不是标准包内导入：

1. `_get_package.py` 计算 `src/dependency` 路径。
2. 将该路径追加到 `sys.path`。
3. 以顶层名称导入 `_foundation`。
4. `_file_operations` 和 `_pyside6` 再以顶层名称导入 `modules._error_handling`。

这使模块可用性依赖文件系统布局和全局解释器路径状态。

## 主要设计模式

| 模式 | 使用位置 | 说明 |
| --- | --- | --- |
| Facade/包装器 | GUI、SQLite、Pygame、QR | 对第三方 API 提供更短接口 |
| Result Object | `ReturnValue`、`MEH` | 减少直接抛出异常 |
| Strategy | `Interpreter` | 注入读写解释器函数 |
| Registry | Pygame 图片、字体、声音、按键 | 以字典维护资源和映射 |
| Protocol | `LogProtocol`、`ComponentProtocol` | 描述结构化接口 |
| Optional Adapter | TOML | 缺少 `tomlkit` 时不导出 `Toml` |

## 运行时副作用

- 导入 `_foundation` 会实例化 JSON 日志器并创建或清空日志文件。
- 导入多数功能模块会创建模块级 `Log`。
- `Log` 默认可在构造时创建目录和清空目标文件。
- `Music`、`Sound`、`Image`、`Font` 的构造会初始化 Pygame 子系统。
- GUI 类构造会创建真实窗口或应用对象。

这些行为降低了纯导入、测试隔离和无界面环境运行的可预测性。

## 架构结论

建议保留“基础层 + 可选模块”的总体分层，但把内部连接方式统一为包内相对导入，并用共享协议替代 `sys.path` 修改。返回错误的方式也应在 `ReturnValue`、`MEH`、`False` 和异常之间选定明确规范。

