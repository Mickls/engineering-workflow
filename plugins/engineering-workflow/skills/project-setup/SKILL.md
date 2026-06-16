---
name: project-setup
description: "用于为某个仓库初始化或更新工程协作上下文，包括 .codex 工作目录、常用命令、领域术语、ADR、测试环境、轻量任务定义和 out-of-scope 规则；首次在项目中使用 engineering-workflow 或发现项目上下文缺失时使用。"
---

# 项目工程上下文初始化

## 概述

本 skill 用于把“这个项目怎么协作”沉淀到仓库文档中，减少每个会话重复猜测。它不替代 `AGENTS.md`，而是生成项目级上下文，供需求、诊断、编码、测试和交付流程读取。

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
- 准备创建或更新哪些文件。

如果要改变已有目录约定，先获得用户确认。

如果项目上下文缺失较多，按三段式确认：

1. Issue tracker：本地 `.codex/engineering-workflow/issues/`、GitHub、GitLab、Linear 或其他。
2. 状态/标签词汇：`draft`、`reviewing`、`approved`、`doing`、`done`、`blocked`、`deferred` 是否需要映射到项目已有标签。
3. Domain docs：单上下文 `.codex/engineering-workflow/context.md`，还是多上下文 `.codex/engineering-workflow/context-map.md`。

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
- `.codex/engineering-workflow/project/contracts.md` 记录当前项目可遵从的工程契约，不记录没有证据的猜测；每条“已保证”都必须写证据位置。
- 如果框架、接口定义或依赖注入已经保证输入完成标准化、非法值被拦截或依赖存在，内部实现原则上不得重复做同类 trim/strip/normalize、空值/空内容判断或依赖存在性判断。
- 不确定的保证写入 `Still Unsafe Boundaries` 或待确认项，不要写成已生效契约。
- `.codex/engineering-workflow/context.md` 只写领域术语，不写实现细节。
- `.codex/engineering-workflow/adr/` 只记录难逆转、反直觉、有真实权衡的决策。
- `.codex/engineering-workflow/project/out-of-scope.md` 记录已明确拒绝或容易反复误提的方案。
- `.codex/engineering-workflow/` 默认是 agent 工作产物，不主动纳入 git；如用户要求共享其中部分文件，先说明纳入原因和 ignore 状态。

### 4. 完成后

汇报：

- 创建或更新的文件。
- 后续哪些 skill 会读取这些文件。
- 仍缺少哪些用户信息。

纯文档初始化不需要运行业务测试；可做回读检查或 markdown lint。
