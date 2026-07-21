# 交付检查清单

## 多语言文档

如果本次创建或更新了需要用户 review 的英文主文档：

- 确认英文主文档是权威来源。
- 确认触发范围包括 design/plan 和项目自定义 durable artifact。
- 确认对应中文 review 辅助说明已创建或同步更新到 `.codex/engineering-workflow/` 下。
- 中文辅助说明必须记录英文源文件路径、`source_commit` 或更新时间、生成时间，以及“英文主文档为准”的声明。
- 最终回复要求用户 review 英文主文档时，必须同时列出中文辅助说明路径；无法生成时说明原因、受影响文件和 review 风险。

## 需求覆盖核销

非轻量需求如果存在 issue/design/plan，声明完成前必须核销关键约束覆盖矩阵。no-doc 例外必须核销临时计划或回复中的最小关键约束清单。

规则：

- 每个关键约束 ID 必须有实际实现落点，或明确 `not-applicable` / `blocked` 证据。
- 每个关键约束 ID 必须有测试、手动验证、代码审查证据，或明确不可验证原因和风险。
- 高风险约束缺少验证证据时不得说“完成”或“已修复”。
- 如果实现过程中发现 design/plan 漏了关键约束，先更新文档并说明，不得把新行为藏在代码里。
- `architecture` 约束必须逐条核销：统一实例化、DI/provider、generated code、schema/migration、事务边界、异步/手动生成流程都要有 diff 证据或明确不适用证据。
- 正确路径需要用户手工生成、迁移或部署时，只能把对应约束报告为 `blocked` / `manual-only`，并说明下一步；不得为了交付闭环手改 generated output、绕开 provider/DI、跳过 schema/migration 来源或隐藏手动步骤。
- 行为约束的验证证据必须对应编码前已批准的验收场景；根据实现结果反向补写的场景不能作为独立证明。

## 用户 Review 包

- HITL 和最终交付先按 `review-packets.md` 提供普通语言的行为、目标关系、方案偏离、验收证据、剩余风险和最多三个用户 review 项。
- 文件列表、完整命令、diff 和专业技术细节放在技术证据区，不能成为理解用户可见行为的前提。
- 不重复执行历史、已废弃方案或逐步状态日志；只报告当前有效行为、偏离、证据和风险。

## 完成边界和 Follow-up

- 对照批准时冻结的验收场景判断当前需求是否完成，不用实现中新增的非阻塞改进持续推迟交付。
- 原验收已满足时将当前需求关闭；相邻缺陷、优化和未来能力建立 follow-up，并说明是否阻塞当前交付。
- 最终回复分别列出当前交付状态和 follow-up，不把“还有可优化项”表述成当前需求未完成。

## 项目上下文

声明完成前复用同一任务的 readiness evidence，并确认其 `scan_scope` 覆盖最终 diff。入口、schema、validation、DI/bootstrap、generated code、命令、CI、领域术语或核心边界变化命中相关 `watch_patterns` 时，使用 `project-setup` 更新对应文档；无相关变化时不重复 refresh。

本次 diff 触发统一实例化、DI/provider、generated code、schema/migration、事务、异步或手动流程时，design/plan 或 no-doc 清单必须已有对应 `architecture` 约束。

上下文压缩或恢复本身不要求重复 refresh；source commit、scope、watch patterns 和 known gaps 未变化时复用 decision/evidence ledger。

## 防御式代码审查

代码、测试代码或脚本改动需要检查 diff 是否新增或清理了：

- `string-normalization`
- `empty-check`
- `dependency-guard`
- `default-fallback`
- `error-wrapping` / `logging`

新增候选必须说明边界证据，或说明已删除/移动到真实边界。清理存量候选必须说明删除、保留、移动和未动的分类结果。

## 最小正确实现

如果本次改动涉及代码、测试、脚本、依赖、配置、skill 规则或项目 workflow，交付前检查是否新增：

- 依赖、版本升级、replace / override / resolution。
- 抽象、interface、factory、strategy、wrapper、adapter、service 层或目录结构。
- 配置项、feature flag、扩展点、模板字段或中间类型。
- 手写标准库、框架、数据库、浏览器或平台 native feature 已覆盖的能力。
- 为内部 helper 堆叠测试，而不是从稳定入口证明行为。

非轻量或中高风险任务默认运行：

```bash
scripts/audit-minimal-correct.sh
```

如果目标仓库没有同名脚本，使用当前 skill 所在 plugin root 的 `scripts/audit-minimal-correct.sh`，工作目录仍保持为目标仓库根目录。脚本是启发式审计，不替代 lint/test/build、需求覆盖核销或人工判断。
