# Context 和实现覆盖

## Context Freshness

编码前读取：

- `.codex/engineering-workflow/project/project-profile.md`
- `.codex/engineering-workflow/project/commands.md`
- `.codex/engineering-workflow/project/contracts.md`
- `.codex/engineering-workflow/project/issue-workflow.md`
- `.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`

检查 `Freshness`、`scan_scope`、`evidence_paths`、`watch_patterns` 和 `known_gaps`。

如果当前改动涉及 route/controller/handler/resolver、CLI/job、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置，确认这些来源在 `scan_scope` 中。缺少或过期的契约不能当作“上游已保证”的证据。

## 实现覆盖

非轻量需求编码时，必须把实现和已确认 design/plan 或 no-doc 最小关键约束清单逐条对齐。

编码前：

- 提取所有关键约束 ID。
- 对即将修改的入口、函数、接口、job 或流程，搜索它们在 design/plan 中出现的位置。
- 对照项目契约画像，确认哪些输入、依赖或生命周期已经由框架、接口定义、构造函数、依赖注入、模块系统、generated code 或 fixture 保证。
- 明确代码改动覆盖哪些约束，哪些约束只由测试、文档或人工验证覆盖。

编码后：

- 回填实际代码落点和状态。
- 每个关键约束必须处于 `implemented`、`verified`、`manual-only`、`blocked` 或 `not-applicable`。
- `not-applicable` 必须写证据。
- 存在未解释的 `planned`、`todo`、空实现落点或空验证入口时，不得进入完成声明。
