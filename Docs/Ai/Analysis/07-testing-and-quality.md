> [!INFO]
> 文档：测试与质量状态  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 验证环境：仓库 `.venv`，Python 3.12

# 测试与质量

## 本次验证

| 检查 | 结果 |
| --- | --- |
| `python -m compileall -q src` | 通过 |
| 文件操作与 MEH 显式测试 | `62 passed` |
| `mypy src` | 未执行，虚拟环境未安装 `mypy` |
| 源码模块导入烟雾测试 | 7 个功能模块均可从源码导入 |

Pytest 产生一条缓存警告：当前 `.pytest_cache` 无法创建或写入，不影响测试结果。

## 现有测试覆盖

### 已覆盖

- `_file_operations.CSV`
- `_file_operations.Ini`
- `_file_operations.Json`
- `_file_operations.Toml`
- `_error_handling.MEH`

覆盖内容包括往返读写、空内容、非法类型、不存在文件、编码和链式错误处理。

### 未覆盖

- `_foundation` 的 `Log` 和基础 `Json`
- `ReturnValue`
- `_pygame`
- `_pyside6`
- `_SQLite3`
- `_tkinter`
- `_QR`
- 打包后安装与导入

## 测试结构问题

- 测试使用 `from src.dependency...`，没有验证用户实际使用的 `dependency...` 导入路径。
- `test/_error_handling/monadic_eh.py` 文件名不符合默认 `test_*.py` 发现规则，本次通过显式指定文件执行。
- GitHub Actions 不运行测试。
- GUI、音频和图像模块需要无头环境策略或适配层后才能稳定测试。
- 没有覆盖率配置和最低覆盖率门槛。

## 质量工具

- `mypy.ini` 的 `mypy_path` 是本机绝对路径 `D:\xm\python\dependency`，不可移植。
- 仓库没有统一的 lint、format 或测试配置。
- `.pyi` 只覆盖基础日志/JSON和部分 Pygame 音频类，类型声明不完整。

## 建议验证矩阵

1. Python 3.12 的 Windows 与 Ubuntu。
2. 基础安装，不安装任何 extra。
3. 每个 extra 独立安装。
4. 全部 extras 安装。
5. 从源码测试和从构建 wheel 安装后测试。
6. GUI/媒体模块使用 mock 或 dummy 驱动执行无头测试。

