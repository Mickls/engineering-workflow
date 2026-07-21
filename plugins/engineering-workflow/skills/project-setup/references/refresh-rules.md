# Refresh 规则

## Freshness 元数据

项目上下文不能只看文件是否存在，还要判断是否可能过期。上下文文件应记录：

- `updated_at`：最后更新时间。
- `source_commit`：可用 git 时记录扫描依据的 `HEAD`。
- `scan_scope`：本次扫描覆盖的模块、入口、配置、命令或文档范围。
- `evidence_paths`：支撑结论的文件或目录。
- `watch_patterns`：这些路径变化时应重新检查的模式。
- `known_gaps`：证据不足、未扫描或需要用户确认的内容。

## 触发信号

触发 refresh 或 targeted-refresh 的信号：

- 当前 git `HEAD` 与 `source_commit` 不同，且变更文件命中 `watch_patterns`。
- 本次任务会修改或依赖 route/controller/handler/resolver、CLI/job 入口、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置。
- 当前任务涉及的模块、入口或命令不在 `scan_scope` 中。
- `known_gaps` 命中当前任务。
- 非轻量任务无法读取 freshness 元数据。
- 非 git 项目中，证据文件 mtime 晚于上下文文件，或无法判断 freshness。

`source_commit` 与当前 `HEAD` 不同本身不等于 stale；必须结合两者之间的变更路径、当前工作树和 `watch_patterns` 判断。

证据不足时不要把旧结论当成当前事实。应把相关保证降级到 `Still Unsafe Boundaries`、`known_gaps` 或临时风险说明，再决定是否补充本地校验。

## 同一任务内复用

首次 readiness 检查后记录任务级证据：检查时的 `HEAD`、相关工作树路径、已读 project/context 文件、覆盖的 `scan_scope`、命中的 `watch_patterns` / `known_gaps` 和 readiness 结果。

后续 requirements、coding、testing 和 verification 可以复用该证据，不重复读取和刷新全部上下文。以下任一条件出现时证据失效并重新检查：

- 任务范围扩展到未覆盖的入口、模块、命令或契约。
- `HEAD` 或工作树新增变化命中相关 project 文档的 `watch_patterns`。
- 新信息命中 `known_gaps`，或原证据文件被删除、替换、生成或迁移。

上下文压缩、会话恢复、模型切换或跨天继续本身不使 readiness evidence 失效。恢复时先读取当前 issue 的 decision ledger / design / plan / handoff，核对 `source_commit`、scan scope、standing constraints、工作区状态和 known gaps；这些未变化时禁止重新做全仓或全调用链广泛搜索。

如果账本、代码和状态文档互相冲突，执行一次集中 targeted refresh，修正当前有效事实和依赖后再继续；不得在每个用户回答后零散重搜或边问边修文档。

每个 project 文档的 `watch_patterns` 只覆盖会改变该文档结论的来源；能列具体入口、配置或文档时，不使用整个仓库或全部 skills 的宽泛模式。

## 模式选择

- 缺失用 `bootstrap`。
- 命中局部 stale 信号用 `targeted-refresh`。
- 大范围变化用 `refresh`。
- 用户只读调查或禁止写入时用 `audit-only`。

## 需要确认的决策

默认不要为了创建 `.codex/engineering-workflow/` 工作产物而打断用户。只有存在真实决策点时才确认：

- Issue tracker：本地 `.codex/engineering-workflow/issues/`、GitHub、GitLab、Linear 或其他。
- 状态/标签词汇是否需要映射到项目已有标签。
- Domain docs：单上下文 `context.md`，还是多上下文 `context-map.md`。
- 非默认写入目录或是否纳入 git。
- 英文主文档对应的中文 review 辅助说明是否需要放在默认位置以外。
- 项目是否存在“禁止 duplicate translated reports / bilingual protocol variants”规则。
