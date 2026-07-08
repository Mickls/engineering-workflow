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

证据不足时不要把旧结论当成当前事实。应把相关保证降级到 `Still Unsafe Boundaries`、`known_gaps` 或临时风险说明，再决定是否补充本地校验。

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
