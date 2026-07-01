# 项目画像模板

```md
# 项目画像

## Freshness 元数据

- updated_at:
- source_commit:
- scan_scope:
  -
- evidence_paths:
  - README / docs / package config / build config / CI config
- watch_patterns:
  - README*
  - docs/**
  - .github/**
  - Makefile
  - package.json
  - pyproject.toml
  - go.mod
  - pom.xml
  - build.gradle*
  - Cargo.toml
- known_gaps:
  -

## 项目概览

- 项目类型：
- 主要语言/框架：
- 主要入口：
- 关键模块：

## 工作约定

- 默认响应语言：
- 主文档语言规则：
- 英文主文档触发类型：
- 中文 review 辅助说明位置：
- duplicate translated report / bilingual protocol 规则：
- 工作产物根目录：
- Tolaria MCP 状态：available / unavailable / disabled / failed
- Tolaria vault：
- Tolaria project：
- fallback 路径：`.codex/engineering-workflow/`
- 是否需要 issue/design/plan：
- 轻量任务定义：
- 高风险任务定义：

## 重要路径

- 需求文档：`<artifact-root>/issues/`
- 项目契约：`<artifact-root>/project/contracts.md`
- 项目术语：`<artifact-root>/context.md`
- ADR：`<artifact-root>/adr/`
- 测试文档：
- 本地环境文档：

## 风险提示

- 常见误解：
- 不应触碰的路径：
- 需要用户确认的操作：
```

要求：

- 除非用户或项目规则明确要求其他语言，项目画像正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。
- `Freshness` 记录项目画像的来源，不要只写更新时间。
- 工作产物根目录必须记录 Tolaria 探测结果；Tolaria 不可用时记录 fallback `.codex/engineering-workflow/`。
- `watch_patterns` 只保留当前项目真实存在或合理相关的模式，避免照搬无关技术栈。
- 项目结构、主要框架、工作约定或高风险任务定义变化后，需要 targeted refresh 本文件。
