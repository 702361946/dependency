> [!INFO]
> 文档：`_SQLite3` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_SQLite3`

# `_SQLite3`

## 职责

该模块包装 Python 标准库 `sqlite3`，提供连接、事务和常见 DDL/DML 的便捷方法。

## 公共 API

```python
from dependency.modules._SQLite3 import SQLite
```

## 能力

### 连接与事务

- `close()`
- `commit()`
- `rollback()`
- `savepoint()`
- `rollback_to()`
- `release()`

构造使用 Python 3.12 的 `sqlite3.connect(..., autocommit=...)`。

### 数据操作

- `execute()`
- `select()`
- `insert()`
- `update()`
- `delete()`

### 数据库对象

- 表、索引、视图和触发器的创建与删除。
- `alter_table()`。
- 附加和分离数据库。
- `pragma()`、`analyze()`、`vacuum()`、`reindex()`。

## 返回方式

`execute()` 成功时总是调用 `fetchall()` 并返回列表，失败返回 `False`。其他方法通常将“结果不是 `False`”转换为布尔值。

## 风险

- 表名、列名、条件、约束、视图和触发器等均通过字符串拼接进入 SQL。
- `update(condition: str)` 和字符串形式的 `delete(condition)` 会直接接受条件文本。
- `attach_database()` 将文件路径直接嵌入 SQL 字符串。
- `execute()` 同时承担查询和写入，返回类型不够明确。
- 没有上下文管理器，异常路径下需要调用方保证关闭连接。
- 没有测试事务、自动提交、DDL/DML 和注入边界。
- 类名和模块名使用大写 `SQLite3` 风格，与 Python 包命名惯例不同。

## 建议

将查询与命令执行分开，限定标识符格式，使用结构化条件构建器，并实现 `__enter__`/`__exit__`。优先增加内存数据库测试。

