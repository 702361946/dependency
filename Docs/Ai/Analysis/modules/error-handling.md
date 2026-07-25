> [!INFO]
> 文档：`_error_handling` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_error_handling`

# `_error_handling`

## 职责

该模块提供两种轻量结果容器，用于在不直接抛异常的情况下传递成功值或错误。

## 公共 API

```python
from dependency.modules._error_handling import MEH, ReturnValue
```

### `ReturnValue[T]`

状态字段：

- `ok`：成功标志。
- `v`：成功值或失败附带值。

方法：

- `get(default=None)`：失败时返回默认值。
- `unwrap()`：成功返回值，失败返回 `None`。
- `__call__()`：等价于 `get()`。
- `__bool__()`：返回 `ok`。

构造参数若传入另一个 `ReturnValue`，会复制其状态和值。

### `MEH[T]`

状态字段：

- `v`：成功值。
- `ok`：成功标志。
- `e`：错误值。

主要方法：

- `unit_ok()`、`unit_err()`：构造成功或失败。
- `bind()`：串联返回 `MEH` 的函数。
- `map()`：转换成功值，并把函数异常转为失败。
- 无参数函数版本和 `no_raise` 变体。
- `get()`、`unwrap()`、`__call__()`、`__bool__()`。

## 数据流

```text
输入值
  └── MEH.unit_ok(value)
      ├── map(pure_function)
      ├── bind(function_returning_meh)
      └── 失败时短路，保留错误
```

## 已验证状态

现有 MEH 测试覆盖构造、map、bind、失败短路、异常转换和集成流程。本次显式执行后，与文件操作测试合计 `62 passed`。

`ReturnValue` 没有独立测试，但文件操作模块大量间接使用它。

## 风险

- `bind()` 不捕获回调异常，这一行为由测试明确确认，但需要写入公共契约。
- `map_no_raise()` 在普通值分支直接返回原值，和标注的 `MEH[U]` 不一致。
- `map_no_raise_no_arg_func()` 可能把已有 `MEH` 包装为嵌套结果。
- `ReturnValue.unwrap()` 在失败时丢弃错误值。
- 两个结果类语义接近，但字段和错误传播方式不同。

## 建议

选择一个主结果类型，补充 `error` 属性、泛型错误类型和一致的 `map`/`bind` 契约。若保留两个类，应明确一个用于简单 I/O，另一个用于函数式链式处理。

