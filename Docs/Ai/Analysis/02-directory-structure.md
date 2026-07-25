> [!INFO]
> 文档：目录结构分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 分析范围：仓库目录与源码包布局

# 目录结构

```text
dependency/
├── .github/workflows/          # GitHub Actions，仅构建发行包
├── build/                      # 本地构建中间产物
├── dist/                       # wheel 与 sdist
├── log/                        # 运行时日志
├── src/
│   └── dependency/
│       ├── __init__.py         # 顶层入口，只导出 foundation
│       ├── _foundation/        # 基础设施层
│       └── modules/
│           ├── _error_handling/
│           ├── _file_operations/
│           ├── _pygame/
│           ├── _pyside6/
│           ├── _QR/
│           ├── _SQLite3/
│           └── _tkinter/
├── test/
│   ├── _error_handling/
│   └── _file_operations/
├── pyproject.toml              # 构建、项目元数据、可选依赖
├── mypy.ini                    # 本地绝对路径配置
└── README.md                   # 简要使用说明
```

## 根目录职责

| 路径 | 职责 | 现状 |
| --- | --- | --- |
| `.github/workflows` | 自动化构建 | 只运行 `python -m build` |
| `src` | 可发布源码 | 主体代码所在地 |
| `test` | 单元测试 | 只覆盖两个模块 |
| `dist` | 历史发行物 | 保存 1.2.2 到 1.2.4 |
| `build` | 构建中间目录 | 应视为生成物 |
| `log` | 默认日志目录 | 导入和运行代码时产生 |

## 包目录特征

`src/dependency/modules` 没有 `__init__.py`。源码环境依靠命名空间包行为和各模块 `_get_package.py` 对 `sys.path` 的修改完成导入。这使目录结构同时承担了源码组织和运行时路径引导两种职责。

每个功能模块基本遵循以下结构：

```text
_module/
├── __init__.py
├── _get_package.py
├── 主要实现文件.py
└── README 或附属说明.md
```

但 `_error_handling` 没有 `_get_package.py`，`_pyside6` 和 `_file_operations` 又通过顶层 `modules._error_handling` 访问它，说明模块间依赖尚未使用统一的包内相对导入方式。

## 规模热点

- `_pyside6/_ui_control_handling.py`：约 1745 行，是最大单文件。
- `_pyside6/_component.py`：约 402 行。
- `_tkinter/_component.py`：约 373 行。
- `_pygame/_key_mapping.py`：约 360 行。
- `_SQLite3/_SQLite3.py`：约 330 行。

PySide6 控件处理文件是最明显的维护热点，适合按控件类型拆分。

