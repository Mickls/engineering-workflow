---
name: project-setup
description: "当首次在仓库中使用 engineering-workflow，或项目上下文缺失、stale、超出 scan_scope、命中 watch_patterns / known_gaps 时使用；已有新鲜且覆盖当前范围的上下文应复用。"
---

# 项目工程上下文初始化和刷新

## 目标

把“这个项目怎么协作”沉淀到仓库文档中，减少每个会话重复猜测。它不替代 `AGENTS.md`，而是生成和刷新项目级上下文，供需求、诊断、编码、测试和交付流程读取。

默认写入 `.codex/engineering-workflow/`；除非用户或项目规则明确要求其他语言，项目上下文文档、ADR、issue 约定、命令说明和风险说明默认中文。

## 默认目录

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
  review-notes/
  project/
```

如果仓库已有等价位置或用户指定其他目录，应沿用已有位置，不强行迁移。`.codex/engineering-workflow/` 默认是 agent 工作产物，不主动纳入 git。

## Context Readiness Gate

非轻量需求、代码修改、测试设计和交付声明前，需要确认关键上下文处于可用状态：

- `.codex/engineering-workflow/project/project-profile.md`
- `.codex/engineering-workflow/project/commands.md`
- `.codex/engineering-workflow/project/contracts.md`
- `.codex/engineering-workflow/project/issue-workflow.md`
- `.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`

关键上下文缺失时运行 `bootstrap`；命中 stale 信号时运行 `targeted-refresh` 或 `refresh`。同一任务已有仍覆盖当前 scope 的 readiness 证据时直接复用；失效条件见 [refresh-rules.md](references/refresh-rules.md)。只有用户禁止写入、需要非默认位置、纳入 git、外部 issue tracker 或多上下文结构时，才先确认。

## 运行模式

- `bootstrap`：关键上下文缺失时使用，创建最小可用 project 文档和 context。
- `refresh`：已有上下文明显过期或多个核心来源变化时使用。
- `targeted-refresh`：当前任务只涉及某个入口、模块、命令、schema、DI/bootstrap 或领域边界时使用。
- `audit-only`：用户只想了解上下文状态、或禁止写入时使用。

默认选择最小足够模式。细则见 [refresh-rules.md](references/refresh-rules.md)。

## 探查和写入

探查时关注：

- 根目录 `AGENTS.md`、README、开发/测试/部署文档、CI 配置、Makefile、package scripts。
- `.codex/engineering-workflow/project/`、context、context-map、ADR 是否存在。
- 当前项目语言、框架、入口契约、validation、DI/bootstrap、generated code 和测试 fixture。
- 哪些输入已在边界完成标准化/校验，哪些依赖已由构造函数、DI container、framework lifecycle、module provider 或 fixture 保证存在。
- 哪些外部数据边界仍不安全。

写入项目上下文时使用 references 模板：

- [project-profile.md](references/project-profile.md)
- [commands.md](references/commands.md)
- [contracts.md](references/contracts.md)
- [domain.md](references/domain.md)
- [issue-workflow.md](references/issue-workflow.md)
- [out-of-scope.md](references/out-of-scope.md)

项目上下文写作规则见 [writing-project-context.md](references/writing-project-context.md)。

## 契约变更回写

如果当前任务修改了入口、schema、middleware、validation、OpenAPI/proto、GraphQL、DI/bootstrap、constructor、module provider、generated code、lint/test/build/package/CI 配置、领域术语、状态机、核心业务边界或跨模块约定，交付前需要 targeted refresh 对应 project 文档。

## 完成汇报

汇报创建或更新的文件、采用的运行模式和 freshness 判断、后续哪些 skill 会读取这些文件，以及仍缺少哪些用户信息。纯文档初始化不需要运行业务测试，可做回读检查或 markdown/link/path 校验。
