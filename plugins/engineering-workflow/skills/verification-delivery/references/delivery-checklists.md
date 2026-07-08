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

## 项目上下文

声明完成前检查：

- 是否读取了 `.codex/engineering-workflow/project/project-profile.md`、`commands.md`、`contracts.md`、`issue-workflow.md`、`context.md` 或 `context-map.md`。
- 这些上下文是否包含 freshness 元数据，且 `scan_scope` 覆盖当前任务。
- 本次 diff 是否触及入口、schema、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置、领域术语或核心业务边界。

如果上下文缺失或 stale，且任务不是轻量只读，应在交付前使用 `project-setup bootstrap`、`refresh` 或 `targeted-refresh`。如果本次 diff 改变项目契约来源，必须回写对应 project 文档并刷新 metadata。

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
