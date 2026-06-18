# Project Profile 模板

```md
# Project Profile

## Freshness

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
- 是否需要 issue/design/plan：
- 轻量任务定义：
- 高风险任务定义：

## 重要路径

- 需求文档：`.codex/engineering-workflow/issues/`
- 项目契约：`.codex/engineering-workflow/project/contracts.md`
- 项目术语：`.codex/engineering-workflow/context.md`
- ADR：`.codex/engineering-workflow/adr/`
- 测试文档：
- 本地环境文档：

## 风险提示

- 常见误解：
- 不应触碰的路径：
- 需要用户确认的操作：
```

要求：

- `Freshness` 记录项目画像的来源，不要只写更新时间。
- `watch_patterns` 只保留当前项目真实存在或合理相关的模式，避免照搬无关技术栈。
- 项目结构、主要框架、工作约定或高风险任务定义变化后，需要 targeted refresh 本文件。
