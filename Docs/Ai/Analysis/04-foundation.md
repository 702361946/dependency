> [!INFO]
> 文档：基础层分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/_foundation`

# 基础层

## 对外导出

`dependency` 顶层通过 `from ._foundation import *` 导出：

- `os_name`
- `work_directory`
- `Log`
- `LogProtocol`
- `Json`
- `log_path`

## 组件职责

### `_os_name_get.py`

- 在导入时获取 `(os.name, platform.system())`。
- 在导入时保存当前工作目录。
- 根据平台结果辅助日志路径选择。

`work_directory` 是导入时快照，不会随后续 `os.chdir()` 更新。

### `_log_protocol.py`

定义运行时可检查的 `LogProtocol`，包含 `debug`、`info`、`warning`、`error`、`critical`。它适合用于依赖注入，但当前多数实现类型仍直接绑定具体 `Log`。

### `_log.py`

`Log` 支持：

- 五级日志过滤。
- 控制台和文件输出。
- 自定义字段顺序和分隔符。
- 时间格式。
- 调用栈文件与行号。
- ANSI 控制台颜色。

主要问题：

- 模块级日志器常使用写入模式，导入可能清空历史日志。
- 写文件是同步操作，每条消息都重新打开文件。
- 没有锁或标准 `logging.Handler` 集成。
- 日志等级接口依赖大写字符串。
- 默认路径和工作目录依赖进程启动位置。

### `_json.py`

基础 `Json` 提供 `dumps`、`loads`、`dump`、`load`。它与 `_file_operations.Json` 是两套独立实现，返回规范也不同。

已发现 `load()` 在补全 `.json` 后又使用 `f"{file_path}.json"` 打开文件，会形成 `.json.json` 路径。现有测试没有覆盖该基础实现。

## 基础层定位建议

- 保留 `LogProtocol`，让上层依赖协议而不是具体类。
- 顶层只保留一个 JSON API，避免同名类产生语义冲突。
- 将日志器创建延迟到对象构造或显式工厂调用。
- 把平台和路径信息封装成函数，避免导入时固定状态。
- 修正 `__varsion__` 拼写并统一版本来源。

