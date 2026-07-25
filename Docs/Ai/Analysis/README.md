> [!INFO]
> 文档：项目分析索引  
> 分析时间：2026-07-25 14:42:49 JST (UTC+09:00)  
> 分析基线：Git `ee6f15d`，项目版本 `1.2.4`

# 项目分析文档

本目录记录 `702361946_dependency` 的项目结构、架构、公共接口、构建配置、测试状态和风险。各部分独立成文，功能模块统一放在 `modules` 子目录。

## 文档结构

```text
Docs/Ai/Analysis/
├── README.md
├── 01-project-overview.md
├── 02-directory-structure.md
├── 03-architecture.md
├── 04-foundation.md
├── 05-packaging-and-dependencies.md
├── 06-public-api.md
├── 07-testing-and-quality.md
├── 08-risks-and-recommendations.md
└── modules/
    ├── README.md
    ├── error-handling.md
    ├── file-operations.md
    ├── pygame.md
    ├── pyside6.md
    ├── qr.md
    ├── sqlite3.md
    └── tkinter.md
```

## 阅读顺序

1. [项目概览](01-project-overview.md)
2. [目录结构](02-directory-structure.md)
3. [架构与依赖关系](03-architecture.md)
4. [基础层分析](04-foundation.md)
5. [打包与依赖](05-packaging-and-dependencies.md)
6. [公共 API](06-public-api.md)
7. [测试与质量](07-testing-and-quality.md)
8. [风险与建议](08-risks-and-recommendations.md)
9. [模块索引](modules/README.md)

## 分析范围

- `pyproject.toml`、根包入口和 GitHub Actions。
- `src/dependency/_foundation` 全部实现。
- `src/dependency/modules` 下 7 个功能模块。
- `test` 下现有测试。
- `dist` 中已有 `1.2.2`、`1.2.3`、`1.2.4` 构建产物。

