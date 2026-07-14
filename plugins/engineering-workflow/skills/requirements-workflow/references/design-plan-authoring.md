# Design / Plan 写作

正式 `design.md` 和 `plan.md` 只描述澄清批准后的当前有效方案，不记录推理过程、纠错痕迹、废弃概念、未确认假设或待用户决定的问题。

## design.md

至少包含：

- 需求背景：问题来源、当前行为、目标用户或业务场景。
- 需求总结：本次要改变什么，不改变什么，完成后的可观察结果。
- 详细需求：完整业务闭环、功能规则、数据流、接口定义、数据表结构、proto/API 变更、错误处理、兼容性、权限、边界条件、相关文档或引用。
- 输入契约 / 校验边界：读取 `.codex/engineering-workflow/project/contracts.md`，记录当前需求适用的输入标准化、validation 边界、依赖保证、仍不安全边界和证据位置。
- 上下文 readiness：记录读取或刷新了哪些 project 文档、freshness 状态、`scan_scope` 是否覆盖当前入口，以及哪些 `known_gaps` 仍影响实现。
- 关键约束覆盖表。
- 非目标范围。
- 验收标准。
- clarification 来源和批准状态。
- 已确认前提。
- 兼容性策略。
- 完整性检查：说明是否覆盖完整功能；如果存在阶段拆分或后置能力，说明原因和恢复路径。

如果涉及数据库、接口、消息、配置或外部依赖，必须讨论清楚，不能只写概念。

如果涉及跨模块调用、统一实例化、DI/bootstrap、module provider、generated code、schema/migration、事务边界、异步/手动生成流程或项目层级边界，必须把适用项目契约写进关键约束覆盖表。每条契约要么成为约束 ID，要么在 design 中标记 `not-applicable` 并写证据；不得只在背景或 Context readiness 中笼统说明“遵循项目规范”。

如果写作过程中发现新的重大决定或影响实现路径的未知，停止写作并重新打开澄清。不要写“原本计划 / 上一版方案 / 后来改为 / 已废弃 / 曾考虑”等过程叙述，除非用户明确要求复盘。被否决方案如果未来容易误提，记录到 clarification、out-of-scope 或 ADR。

## 关键约束覆盖表

关键约束包括：

- 用户明确说“必须”“不能”“应当”的行为。
- 会导致数据丢失、权限绕过、重复写入、状态错乱、兼容性破坏的边界。
- 自动流程和手动流程语义不同的地方。
- existing / non-existing、empty / invalid、root 内外、include / exclude、sync / async、old / new config 等容易遗漏的分支。
- 已由项目契约保证的输入标准化、空值/空内容拦截和依赖存在性保证。
- 项目契约要求的实现路径，例如统一 DI/provider、constructor 注入、generated code 只改 source、schema/migration 手动流程、事务和异步边界。
- `验收标准` 中每一条可观察行为。

格式：

```md
| ID | 类型 | 关键约束 | 影响入口/调用链 | 实现要求 | 验证意图 |
| --- | --- | --- | --- | --- | --- |
| C-001 | boundary | ... | ... | ... | ... |
```

一条约束只表达一个必须被实现或验证的事实。无法自动测试的约束仍保留 ID，并写清手动验证或代码审查证据。

## plan.md

至少包含：

- 总目标和验收标准。
- 任务拆分和执行顺序。
- 每个任务的修改范围、依赖关系、产出、验证方式。
- 涉及的文件或模块。
- 需求覆盖矩阵。
- 已接受风险、环境阻塞和关闭条件；不得保留用户决策型开放问题。
- 完整功能交付路径。

需求覆盖矩阵必须把 `design.md` 的每个约束 ID 映射到实施和验证：

```md
| 约束 ID | 实施步骤 | 预计代码落点 | 测试/验证入口 | 状态 |
| --- | --- | --- | --- | --- |
| C-001 | Step 2 | path/to/file.go:function | integration test / manual command | planned |
```

如果某个实施步骤没有关联任何约束，检查它是否属于无关扩展。编码阶段需要回填实际代码落点、测试名、验证命令和状态；最终交付前不得留下未解释的 `planned` / `todo`。

如果某个实施步骤会触发项目契约，例如修改 constructor/provider、wire/proto/ent/source schema、transaction helper、job/task、生成代码来源或统一实例化链路，`预计代码落点` 和 `测试/验证入口` 必须写明正确路径和手动阻塞点。正确路径需要用户手工生成时，计划状态应允许 `blocked` / `manual-only`，不能为了让当前工作树一次性编译而计划手改 generated output。
