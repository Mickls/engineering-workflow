---
name: verification-delivery
description: "用于声明任务完成前、代码或文档修改后、提交前，以及汇报 lint/test/build 结果、跳过检查、剩余风险和最终交付内容。"
---

# 验证和交付

## 目标

不能没有证据就说完成。最终回复必须说明做了什么、怎么验证、什么没验证、还有什么风险。

## 完成声明硬门禁

在说出或暗示“完成”、“已修复”、“通过”、“没有问题”之前：

1. 确认哪个命令或检查能证明这个结论。
2. 重新运行相关命令。
3. 阅读输出和退出状态。
4. 汇报真实结果。
5. 如果没有运行验证，说明原因。

不得依赖之前运行过的结果、推测、外部成功报告、部分命令输出或“应该会通过”。细则见 [completion-claims.md](references/completion-claims.md)。

## 必须核销

- 非轻量需求存在 issue/design/plan 时，声明完成前必须核销关键约束覆盖矩阵。
- no-doc 非轻量例外必须核销临时计划或回复中的最小关键约束清单。
- 对数据删除、权限、安全、幂等、并发、兼容性、手动/自动语义分歧等高风险约束，缺少验证证据时不得说“完成”或“已修复”。
- 如果本次 diff 改变入口、schema、validation、DI/bootstrap、命令、CI、领域术语或核心业务边界，交付前必须刷新 `.codex/engineering-workflow/project/*`，或说明用户禁止写入/无法刷新带来的风险。
- 如果本次 diff 触发统一实例化、DI/provider、generated code、schema/migration、事务、异步或手动生成流程契约，交付前必须逐条核销对应 `architecture` 约束；正确路径需要用户手工生成、迁移或部署时，只能声明 `blocked` / `manual-only` 和下一步，不能手改生成产物或绕开统一链路后宣称完成。
- 最小正确实现不能删除或弱化 trust boundary validation、错误处理、数据一致性、安全、accessibility、用户明确要求和必要验证；仅为 speculative flexibility 存在的候选应删除、内联，或降级为 design/plan 中的 `defer-with-trigger` / `out-of-scope`。

细则见 [delivery-checklists.md](references/delivery-checklists.md)。

## 代码和脚本改动检查

如果本次改动涉及生产代码、测试代码或脚本，交付前检查：

- 是否新增或清理了 `string-normalization`、`empty-check`、`dependency-guard`、`default-fallback`、`error-wrapping`、`logging` 等防御式代码候选。
- 是否绕过统一实例化、DI/provider、generated code、schema/migration、事务边界、异步/手动生成流程等项目契约。
- 是否新增依赖、抽象、wrapper、配置、模板字段、中间类型，或手写已有能力。
- 非轻量或中高风险任务默认运行 `scripts/audit-minimal-correct.sh`。

防御式代码和最小正确实现审计细则见 [delivery-checklists.md](references/delivery-checklists.md)。

## 验证命令

- 编码后运行项目对应 lint；全项目 lint 成本过高时，可以只检查改动文件或受影响 package，但必须说明范围。
- 运行与本次改动相关的测试：受影响 package 测试、完整调用链测试、bugfix 回归测试或共享行为更大范围测试。
- interface、生成代码、依赖、build tags、配置变化，或测试没有充分编译受影响范围时，运行 build/typecheck/compile。
- 纯文档变更可用结构校验、markdown/link/path 检查、回读检查，并说明代码 lint/test/build 不适用。

细则见 [validation-commands.md](references/validation-commands.md)。

## 特殊完成声明

bugfix、线上问题、数据误删、重复调用、幂等性或并发问题在声明“已修复”前，必须汇报复现入口、修复前失败证据、根因、修改摘要、同路径验证结果和剩余风险。缺少复现、根因或同路径验证时，只能说“已调查到当前状态”或“已做尝试”。

细则见 [completion-claims.md](references/completion-claims.md)。

## 最终回复默认包含

- 修改内容摘要。
- 关键文件路径。
- context readiness / freshness 检查和项目上下文回写结果。
- 已执行的 lint/test/build 命令及结果。
- 未执行的验证项、原因和风险。
- 需要用户继续确认或处理的事项。

小任务可以更短，但仍需包含验证事实。

## Commit

提交前检查暂存范围，只暂存本次任务需要纳入版本管理的文件。默认尊重 `.gitignore`、`.git/info/exclude` 和全局 ignore 规则；不要使用 `git add -f` 纳入 ignored 文件，除非用户明确确认。

commit 信息使用单行 Conventional Commit。细则见 [commit-rules.md](references/commit-rules.md)。
