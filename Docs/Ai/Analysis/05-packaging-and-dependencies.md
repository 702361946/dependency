> [!INFO]
> 文档：打包与依赖分析  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 配置来源：`pyproject.toml`、`dist`、GitHub Actions

# 打包与依赖

## 发布配置

| 项目          | 当前值                     |
|-------------|-------------------------|
| 发布名         | `702361946_dependency`  |
| 导入名         | `dependency`            |
| 当前配置版本      | `1.2.4`                 |
| 当前配置 Python | `>=3.12`                |
| 构建后端        | `setuptools.build_meta` |
| 基础依赖        | 无                       |

## 可选依赖

| Extra             | 依赖                                 |
|-------------------|------------------------------------|
| `pygame`          | `pygame >= 2.6.0`                  |
| `pyside6`         | `pyside6 >= 6.9.0`                 |
| `qr`              | `qrcode >= 8.0`、`pillow >= 11.0.0` |
| `file_operations` | `tomlkit >= 0.12.0`                |
| `sqlite3`         | 标准库，无额外包                           |
| `tkinter`         | 系统 Python 组件，无额外包                  |

## Setuptools 配置特征

- 使用手工 `packages` 列表，不会自动发现新模块。
- `package-dir` 重复列出每个包路径，维护成本较高。
- 存在 `dependency.modules._fo` 路径映射，但没有对应包声明和源码目录，疑似旧别名。
- `src/dependency/modules` 缺少 `__init__.py`，发行物中也没有 `dependency/modules/__init__.py`。
- Markdown 通过 `package-data` 随包发布。

## 构建产物一致性

`dist` 中已有 `1.2.2`、`1.2.3`、`1.2.4`。现有 `1.2.4` wheel 生成于 2026-07-08，而 `pyproject.toml` 修改时间更晚。

该 wheel 的元数据仍声明：

- `Requires-Python: >=3.10`
- extra 名称被规范化为 `file-operations`

当前源码配置则声明 Python `>=3.12`。因此仓库内 `1.2.4` 产物不能代表当前配置。

直接把该 wheel 加入 `sys.path` 时，`import dependency` 成功，但 `dependency.modules` 导入失败。普通 `pip install` 会解包 wheel，行为可能不同，但这仍说明父包结构没有显式定义。

## 自动化

GitHub Actions 当前只执行：

1. 检出代码。
2. 安装 Python 3.12。
3. 安装 `build`。
4. 构建 wheel 和 sdist。
5. 上传产物。

流程未执行测试、导入烟雾测试、类型检查或对 wheel 的安装验证。

## 建议

- 增加 `src/dependency/modules/__init__.py`。
- 改用 setuptools 自动包发现。
- 删除失效的 `_fo` 映射。
- 从单一来源生成发行版与运行时版本。
- CI 中先测试，再构建，再将 wheel 安装到干净环境执行导入测试。

