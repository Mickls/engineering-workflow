# Issue 工作流模板

```md
# Issue 工作流

## Freshness 元数据

- updated_at:
- source_commit:
- scan_scope:
  - issue tracker / repo docs / AGENTS.md / workflow docs
- evidence_paths:
  -
- watch_patterns:
  - AGENTS.md
  - .github/**
  - docs/**
  - README*
  - <artifact-root>/project/issue-workflow.md
- known_gaps:
  -

## 工作产物路由

- 工作产物根目录：
- Tolaria MCP 状态：available / unavailable / disabled / failed
- Tolaria vault：
- Tolaria project：
- fallback 路径：`.codex/engineering-workflow/`

## Issue 位置

- 类型：local markdown / GitHub / Linear / 其他
- 默认本地路径：`<artifact-root>/issues/`
- 外部链接或 tracker：

## 本项目 issue 结构

- 普通需求：`<artifact-root>/issues/REQ-YYYYMMDD-NNN_需求简述/`
- 大需求：`<artifact-root>/issues/EPIC-YYYYMMDD-NNN_主题简述/`
- handoff：`<artifact-root>/handoffs/`
- 原型：issue 绑定原型放对应需求目录；非 issue 绑定原型放 `<artifact-root>/prototypes/`
- 中文 review 辅助说明：英文主文档在 issue 目录时放同目录；英文主文档在项目正式目录时放 `<artifact-root>/review-notes/<mirrored-path>.zh-CN.md`
- 英文主文档触发类型：design/plan、exploration note、runbook、checklist、report、ADR、protocol、story、support content、其他需要用户 review 的英文文档

## 状态

- draft：
- reviewing：
- approved：
- doing：
- done：
- blocked：
- deferred：

## 规则

- 什么时候必须创建 issue：
- 什么时候可以跳过：
- design/plan 确认门禁：非轻量需求创建或更新 design/plan 后必须停止当前回合，等待用户后续消息确认；确认前不得编码、写测试、生成 migration/proto 或安排实现类任务。
- design 正文只保留当前有效方案：更新已有文档时删除上一版废弃概念、纠错痕迹和过程叙述；需要长期保留的否决方案放到 out-of-scope 或 ADR。
- no-doc 非轻量例外：如果用户明确要求跳过 issue 文档，仍需在回复或临时计划中列出最小关键约束、实现落点、验证入口，并在交付前逐条核销。
- 需求覆盖矩阵位置：`design.md` 放关键约束覆盖表，`plan.md` 放需求覆盖矩阵。
- UI 原型门禁：独立 UI 需求确认 design/plan 前，默认生成静态 HTML 原型到对应需求目录。
- 英文主文档规则：如果项目要求主文档使用英文，英文文档是权威来源；非轻量且需要用户 review 时，同步生成中文 review 辅助说明，并在说明中标注源文件、`source_commit` 或更新时间、生成时间和“英文原文为准”。
- duplicate translated report 规则：如果项目禁止重复翻译报告或双语协议，工作产物根目录下的中文 review aid 仍可生成，除非项目或用户明确禁止任何中文辅助文件；不得把 review aid 写进生产 artifact 目录。
- ignored 文件规则：fallback `.codex/engineering-workflow/` 默认不主动纳入 git；必要时先说明并等待用户确认。
```

要求：

- 除非用户或项目规则明确要求其他语言，issue 工作流文档正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、issue tracker 名、状态枚举和引用路径可以保留英文。
- 如果 Tolaria MCP 状态或 project 路径变化，需要 targeted refresh 本文件。
- 如果项目改用外部 issue tracker、状态标签或确认流程，需要 targeted refresh 本文件。
- 无法确认的 tracker 或标签映射写入 `known_gaps`，不要猜测。
