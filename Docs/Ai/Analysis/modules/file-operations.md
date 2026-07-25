> [!INFO]
> 文档：`_file_operations` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_file_operations`

# `_file_operations`

## 职责

该模块是当前结构最完整、测试最集中的功能层。它在 `ReturnValue` 之上建立路径、原始文件、路径基类、解释器和具体格式处理器。

## 公共 API

- `BaseClass`
- `PathTools`
- `File`
- `FileBaseClass`
- `Interpreter`
- `CSV`
- `Ini`
- `Json`
- `Toml`，仅在安装 `tomlkit` 时导出

## 内部分层

```text
ReturnValue
  └── BaseClass
      └── File
          └── FileBaseClass
              └── Interpreter
                  ├── CSV
                  ├── Ini
                  ├── Json
                  └── Toml

PathTools 为各层提供 Path 转换、拼接和目录创建。
```

## 核心组件

### `PathTools`

提供字符串/`Path` 转换、路径拼接、创建目录和临时目录。所有操作返回 `ReturnValue`。

### `File`

直接读写完整路径：

- 读取模式：`r`、`b`。
- 写入模式：`w`、`a`、`b`。
- 可选创建父目录。
- 一次性读取全部内容，不适合超大文件。

### `FileBaseClass`

维护基础保存目录和底层文件控制器，负责：

- 校验文件名非法字符。
- 拼接 `file_save_path`、子路径和文件名。
- 将读写委托给 `_fc`。

### `Interpreter`

维护读解释器和写解释器，将原始文本与结构化数据相互转换。

### 格式类

| 类 | 读取结果 | 写入输入 |
| --- | --- | --- |
| `CSV` | 行列矩阵 | `list[list[Any]]` |
| `Ini` | 嵌套字典 | `dict[str, dict]` |
| `Json` | 字典或列表 | 字典或列表 |
| `Toml` | TOML 文档/字典结构 | 字典或列表 |

## 已验证状态

CSV、INI、JSON 和 TOML 测试覆盖有效数据、非法数据、文件不存在、扩展名参数和往返读写。本次执行全部通过。

## 风险

- `config.py` 通过顶层 `modules._error_handling` 导入，依赖 `_get_package.py` 先修改路径。
- `BaseClass.load()`、`dump()` 使用 `pass`，但没有声明为抽象方法。
- 失败时常把另一个 `ReturnValue` 放入外层结果，形成嵌套。
- `set_fc()` 文档允许任意具有读写方法的对象，实际却要求继承 `File`。
- 文件名校验禁止路径字符，因此目录必须单独通过 `file_path` 传递。
- 各格式类参数命名和默认 `filepath` 值不完全一致。

## 建议

优先修复相对导入和嵌套结果，再把 `File` 抽象成协议。保留当前解释器分层，因为它已经形成可扩展结构并有测试支撑。

