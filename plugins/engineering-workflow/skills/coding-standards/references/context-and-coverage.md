# Context 和实现覆盖

## Context Freshness

编码前读取项目 project/context；同一任务已有覆盖当前入口和约束的 readiness evidence 时复用，并检查此后相关工作树变化是否命中 `watch_patterns`。

如果当前改动涉及 route/controller/handler/resolver、CLI/job、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置，确认这些来源在 `scan_scope` 中。缺少或过期的契约不能当作“上游已保证”的证据。

任务范围扩大、相关证据路径变化或命中 `known_gaps` 时，重新使用 `project-setup`；`source_commit` 不同但无相关路径变化时不重复 refresh。

## 实现覆盖

非轻量需求编码时，必须把实现和已确认 design/plan 或 no-doc 最小关键约束清单逐条对齐。

编码前：

- 提取所有关键约束 ID。
- 对即将修改的入口、函数、接口、job 或流程，搜索它们在 design/plan 中出现的位置。
- 对照项目契约画像，确认哪些输入、依赖或生命周期已经由框架、接口定义、构造函数、依赖注入、模块系统、generated code 或 fixture 保证。
- 对照项目契约画像，确认本次 diff 是否触发统一实例化、DI/provider、generated code、schema/migration、事务、异步或手动生成流程；触发时提取对应 `architecture` 约束 ID。
- 明确代码改动覆盖哪些约束，哪些约束只由测试、文档或人工验证覆盖。

编码后：

- 回填实际代码落点和状态。
- 每个关键约束必须处于 `implemented`、`verified`、`manual-only`、`blocked` 或 `not-applicable`。
- `not-applicable` 必须写证据。
- `architecture` 约束必须说明 diff 证据，例如只改 source/provider/schema、不手改 generated output、跨模块依赖通过 constructor/DI 注入、事务/异步边界仍沿用项目入口；正确路径需要用户手工生成时标记 `blocked` / `manual-only`。
- 存在未解释的 `planned`、`todo`、空实现落点或空验证入口时，不得进入完成声明。
