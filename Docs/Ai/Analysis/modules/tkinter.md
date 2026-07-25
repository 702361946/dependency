> [!INFO]
> 文档：`_tkinter` 模块分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 源码目录：`src/dependency/modules/_tkinter`

# `_tkinter`

## 职责

该模块封装 Tk/Toplevel 窗口，并通过 `TKComponent` 管理 Frame 内的组件注册和布局。

## 公共 API

- `Window`
- `TKComponent`

## `Window`

负责：

- 创建主窗口或子窗口。
- 设置标题、尺寸和缩放能力。
- 修改窗口属性。
- 显示、隐藏、关闭窗口。
- 启动 `mainloop()`。

内部 `info` 字典保存构造参数和日志器。

## `TKComponent`

内部维护：

```text
Frame
└── components
    └── name
        ├── type
        ├── Component
        └── pack
            ├── mode
            ├── x / y
            └── open
```

支持创建和部署：

- Button
- Text
- Message
- Entry
- Listbox

布局模式支持 `pack`、`grid` 和 `place`。

## 风险

- 创建子窗口时调用 `main_window.protocol("WM_DELETE_WINDOW", self.window.destroy())`，会立即执行 `destroy()`，而不是注册回调。
- `list()` 方法名覆盖 Python 内置名称。
- `frame_rige` 疑似 `frame_range` 或 `frame_rect` 的拼写问题。
- 组件参数和 Tk 原生布局参数只暴露少量子集。
- `components` 使用无类型约束的嵌套字典，维护成本较高。
- 没有 GUI 测试。
- 子窗口、Frame 和组件均直接创建真实 Tk 对象，难以隔离。

## 建议

先修正 `protocol` 回调，再用数据类表示组件记录。GUI 测试可将 Tk 创建和布局调用抽象成可替换工厂。

