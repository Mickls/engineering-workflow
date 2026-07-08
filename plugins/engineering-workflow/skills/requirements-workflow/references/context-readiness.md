# Context Readiness

创建或更新非轻量 `design.md` / `plan.md` 前，检查项目上下文是否可用。

## 必要文件

- `.codex/engineering-workflow/project/project-profile.md`
- `.codex/engineering-workflow/project/commands.md`
- `.codex/engineering-workflow/project/contracts.md`
- `.codex/engineering-workflow/project/issue-workflow.md`
- `.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`

## Freshness

读取 `updated_at`、`source_commit`、`scan_scope`、`evidence_paths`、`watch_patterns`、`known_gaps`。

需要 refresh 的信号：

- 当前需求涉及未扫描模块。
- 命中 `known_gaps`。
- 涉及 route/controller/handler/resolver、CLI/job、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、generated code、package/build/test/CI 配置等契约来源。
- git `HEAD` 与 `source_commit` 不同，且变更文件命中 `watch_patterns`。

## 处理

- 关键上下文缺失：运行 `project-setup bootstrap`。
- 上下文可能过期：运行 `project-setup targeted-refresh`。
- 多个核心来源变化或无法界定影响范围：运行 `project-setup refresh`。
- 用户禁止写入 `.codex/engineering-workflow/`：在临时计划中记录项目契约、证据来源、未知项和风险。

不要为了默认创建或更新 `.codex/engineering-workflow/` 打断用户。只有非默认路径、外部 issue tracker、状态映射、多上下文结构或纳入 git 等真实决策点才需要确认。
