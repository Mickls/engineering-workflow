---
name: project-setup
description: "用于为某个仓库初始化或更新工程协作上下文，包括 issue 目录、常用命令、领域术语、ADR、测试环境、轻量任务定义和 out-of-scope 规则；首次在项目中使用 engineering-workflow 或发现项目上下文缺失时使用。"
---

# 项目工程上下文初始化

## 概述

本 skill 用于把“这个项目怎么协作”沉淀到仓库文档中，减少每个会话重复猜测。它不替代 `AGENTS.md`，而是生成项目级上下文，供需求、诊断、编码、测试和交付流程读取。

默认写入：

```text
docs/agents/
  project-profile.md
  commands.md
  domain.md
  issue-workflow.md
  out-of-scope.md
CONTEXT.md
docs/adr/
```

如果仓库已有等价位置，应沿用已有位置，不强行迁移。

## 使用时机

- 首次在某个项目使用 `engineering-workflow`。
- 需求、测试或交付规则反复缺少项目命令、术语或 issue 约定。
- 用户要把本工作流分享给另一个项目或朋友使用。
- 项目有多个模块、多个测试环境或复杂领域术语。

轻量一次性任务不必运行本 skill。

## 流程

### 1. 探查

先只读检查：

- 根目录 `AGENTS.md`、`.codex/`、`docs/`、`issue/`、`.github/`、Makefile、package scripts、CI 配置。
- `CONTEXT.md`、`CONTEXT-MAP.md`、`docs/adr/` 是否存在。
- README、开发文档、测试文档、部署文档。
- 当前仓库的 lint/test/build 命令和 integration 环境要求。

### 2. 给出发现和建议

向用户简短说明：

- 已发现哪些项目约定。
- 缺少哪些会影响后续 agent 工作的上下文。
- 准备创建或更新哪些文件。

如果要改变已有目录约定，先获得用户确认。

### 3. 写入项目上下文

使用以下参考模板：

- [project-profile.md](references/project-profile.md)
- [commands.md](references/commands.md)
- [domain.md](references/domain.md)
- [issue-workflow.md](references/issue-workflow.md)
- [out-of-scope.md](references/out-of-scope.md)

规则：

- 不把项目上下文写成通用教程。
- 不记录 secret、token、密码或隐私数据。
- `CONTEXT.md` 只写领域术语，不写实现细节。
- ADR 只记录难逆转、反直觉、有真实权衡的决策。
- `out-of-scope.md` 记录已明确拒绝或容易反复误提的方案。

### 4. 完成后

汇报：

- 创建或更新的文件。
- 后续哪些 skill 会读取这些文件。
- 仍缺少哪些用户信息。

纯文档初始化不需要运行业务测试；可做回读检查或 markdown lint。
