---
name: project-setup
description: "用于为某个仓库初始化或更新工程协作上下文，包括 .codex 工作目录、常用命令、领域术语、ADR、测试环境、轻量任务定义和 out-of-scope 规则；首次在项目中使用 engineering-workflow 或发现项目上下文缺失时使用。"
---

# 项目工程上下文初始化和刷新

## 概述

本 skill 用于把“这个项目怎么协作”沉淀到仓库文档中，减少每个会话重复猜测。它不替代 `AGENTS.md`，而是生成和刷新项目级上下文，供需求、诊断、编码、测试和交付流程读取。

除非用户明确要求其他语言，项目上下文文档、ADR、issue 约定、命令说明和风险说明的正文、标题、表格列名和状态解释都默认使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。

默认写入目标仓库的 agent 工作产物目录：

```text
.codex/engineering-workflow/
  context.md
  context-map.md
  adr/
  issues/
  handoffs/
  reports/
  prototypes/
  debug/
  project/
  project-profile.md
  commands.md
  contracts.md
  domain.md
  issue-workflow.md
  out-of-scope.md
```

如果仓库已有等价位置或用户指定其他目录，应沿用已有位置，不强行迁移；但需要说明偏离默认 `.codex/engineering-workflow/` 的原因。

## Context Readiness Gate

非轻量需求、代码修改、测试设计和交付声明前，需要确认项目上下文处于可用状态。关键上下文包括：

- `.codex/engineering-workflow/project/project-profile.md`
- `.codex/engineering-workflow/project/commands.md`
- `.codex/engineering-workflow/project/contracts.md`
- `.codex/engineering-workflow/project/issue-workflow.md`
- `.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`

如果关键上下文缺失，默认运行 `bootstrap` 模式创建最小可用上下文；不需要因为 `.codex/engineering-workflow/` 被 ignore 而询问用户。只有以下情况需要先确认：

- 用户明确禁止创建或更新 `.codex/engineering-workflow/`。
- 需要写入非默认位置或改变项目已有目录约定。
- 需要把 ignored 的 `.codex/engineering-workflow/` 文件纳入 git。
- 需要选择非默认 issue tracker、状态标签映射或多上下文结构。

如果用户明确要求不创建上下文，仍要在回复、临时计划或 no-doc 约束清单中记录最小项目契约、证据来源和剩余风险。

## 运行模式

- `bootstrap`：关键上下文缺失时使用。只读探查项目，创建最小可用 `project/*`、`context.md` 或 `context-map.md`，并写入 freshness 元数据。
- `refresh`：已有上下文明显过期或多个核心来源变化时使用。重新扫描受影响范围，更新过期章节，保留仍有效的旧结论。
- `targeted-refresh`：当前任务只涉及某个入口、模块、命令、schema、DI/bootstrap 或领域边界时使用。只刷新相关上下文和契约章节。
- `audit-only`：用户只想了解上下文状态、或禁止写入时使用。只报告缺失、过期、证据不足和建议，不写文件。

默认选择最小足够模式：缺失用 `bootstrap`，命中局部 stale 信号用 `targeted-refresh`，大范围变化用 `refresh`，只读调查用 `audit-only`。

## Freshness 判断

项目上下文不能只看文件是否存在，还要判断是否可能过期。上下文文件应记录：

- `updated_at`：最后更新时间。
- `source_commit`：可用 git 时记录扫描依据的 `HEAD`。
- `scan_scope`：本次扫描覆盖的模块、入口、配置、命令或文档范围。
- `evidence_paths`：支撑结论的文件或目录。
- `watch_patterns`：这些路径变化时应重新检查的模式。
- `known_gaps`：证据不足、未扫描或需要用户确认的内容。

触发 refresh 或 targeted-refresh 的信号：

- 当前 git `HEAD` 与 `source_commit` 不同，且变更文件命中 `watch_patterns`。
- 本次任务会修改或依赖 route/controller/handler/resolver、CLI/job 入口、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置。
- 当前任务涉及的模块、入口或命令不在 `scan_scope` 中。
- `known_gaps` 命中当前任务。
- 非轻量任务无法读取 freshness 元数据。
- 非 git 项目中，证据文件 mtime 晚于上下文文件，或无法判断 freshness。

证据不足时不要把旧结论当成当前事实。应把相关保证降级到 `Still Unsafe Boundaries`、`known_gaps` 或临时风险说明，再决定是否补充本地校验。

## 使用时机

- 首次在某个项目使用 `engineering-workflow`。
- 非轻量任务、代码修改或测试设计前，发现关键上下文缺失。
- 读取项目上下文时发现 freshness 元数据缺失、命中 stale 信号或当前任务超出 `scan_scope`。
- 需求、测试或交付规则反复缺少项目命令、术语或 issue 约定。
- 本次改动会改变入口契约、validation、DI/bootstrap、命令、核心领域术语或重要业务边界。
- 用户要把本工作流分享给另一个项目或朋友使用。
- 项目有多个模块、多个测试环境或复杂领域术语。

轻量一次性只读任务不必运行本 skill，但如果缺少项目上下文，需要说明结论置信度较低。

## 流程

### 1. 探查

先只读检查：

- 根目录 `AGENTS.md`、`.codex/`、`docs/`、`issue/`、`.github/`、Makefile、package scripts、CI 配置。
- `.codex/engineering-workflow/project/`、`.codex/engineering-workflow/context.md`、`.codex/engineering-workflow/context-map.md`、`.codex/engineering-workflow/adr/` 是否存在。
- 旧位置 `docs/agents/`、`CONTEXT.md`、`CONTEXT-MAP.md`、`docs/adr/` 是否存在；如果已有且项目依赖它们，先说明迁移风险，不要擅自移动。
- README、开发文档、测试文档、部署文档。
- 当前仓库的 lint/test/build 命令和 integration 环境要求。
- 当前项目语言、框架和入口契约：route/controller/handler/resolver/CLI/job、middleware、binding、schema、OpenAPI/proto、GraphQL、表单校验、依赖注入、模块系统、bootstrap、generated code 和测试 fixture。
- 哪些输入已在边界完成 trim/strip/normalize、类型转换、必填/非空/枚举/范围/权限/租户/资源归属校验；哪些依赖已由构造函数、DI container、framework lifecycle、module provider 或 fixture 保证存在。
- 哪些外部数据边界仍不安全：数据库旧数据、缓存、消息、文件、网络响应、反序列化、用户脚本、第三方回调等。

### 2. 给出发现和建议

向用户简短说明：

- 已发现哪些项目约定。
- 缺少哪些会影响后续 agent 工作的上下文。
- 当前选择的运行模式：`bootstrap`、`refresh`、`targeted-refresh` 或 `audit-only`。
- 准备创建、更新或只审计哪些文件。

如果要改变已有目录约定，先获得用户确认。

默认不要为了创建 `.codex/engineering-workflow/` 工作产物而打断用户。只有存在真实决策点时才确认：

- Issue tracker：本地 `.codex/engineering-workflow/issues/`、GitHub、GitLab、Linear 或其他。
- 状态/标签词汇：`draft`、`reviewing`、`approved`、`doing`、`done`、`blocked`、`deferred` 是否需要映射到项目已有标签。
- Domain docs：单上下文 `.codex/engineering-workflow/context.md`，还是多上下文 `.codex/engineering-workflow/context-map.md`。
- 非默认写入目录或是否纳入 git。

如果这些选择不阻塞当前任务，先按默认本地 `.codex/engineering-workflow/` 写入，并在文档中记录默认假设。

### 3. 写入项目上下文

使用以下参考模板：

- [project-profile.md](references/project-profile.md)
- [commands.md](references/commands.md)
- [contracts.md](references/contracts.md)
- [domain.md](references/domain.md)
- [issue-workflow.md](references/issue-workflow.md)
- [out-of-scope.md](references/out-of-scope.md)

规则：

- 不把项目上下文写成通用教程。
- 不记录 secret、token、密码或隐私数据。
- 每个 project 文档都要记录 freshness 元数据；如果某项无法获取，写 `unknown` 和原因。
- `.codex/engineering-workflow/project/contracts.md` 记录当前项目可遵从的工程契约，不记录没有证据的猜测；每条“已保证”都必须写证据位置。
- 如果框架、接口定义或依赖注入已经保证输入完成标准化、非法值被拦截或依赖存在，内部实现原则上不得重复做同类 trim/strip/normalize、空值/空内容判断或依赖存在性判断。
- 不确定的保证写入 `Still Unsafe Boundaries` 或待确认项，不要写成已生效契约。
- `.codex/engineering-workflow/context.md` 只写领域术语，不写实现细节。
- `.codex/engineering-workflow/adr/` 只记录难逆转、反直觉、有真实权衡的决策。
- `.codex/engineering-workflow/project/out-of-scope.md` 记录已明确拒绝或容易反复误提的方案。
- `.codex/engineering-workflow/` 默认是 agent 工作产物，不主动纳入 git；如用户要求共享其中部分文件，先说明纳入原因和 ignore 状态。

### 4. 契约变更回写

如果当前任务修改了会改变项目契约的文件，交付前需要回写对应上下文：

- 新增或调整入口、schema、middleware、validation、OpenAPI/proto、GraphQL、表单规则。
- 新增或调整 DI/bootstrap、constructor、module provider、framework lifecycle、generated code。
- 修改 lint/test/build/package/CI 配置。
- 修改领域术语、状态机、核心业务边界或跨模块约定。

回写时优先使用 `targeted-refresh`，只更新受影响章节和 freshness 元数据。不能确认的保证必须降级为 `known_gaps` 或 `Still Unsafe Boundaries`。

### 5. 完成后

汇报：

- 创建或更新的文件。
- 采用的运行模式和 freshness 判断结果。
- 后续哪些 skill 会读取这些文件。
- 仍缺少哪些用户信息。

纯文档初始化不需要运行业务测试；可做回读检查或 markdown lint。
