---
name: testing-policy
description: "用于规划、编写、更新、运行或解释测试；处理测试失败；判断是否需要新增或跳过测试；以及用少量有证明力的完整调用链测试验证用户行为，而不是堆砌内部实现测试。"
---

# 测试策略

## 目标

测试要证明用户关心的行为或稳定 contract，而不是证明内部函数刚好返回某个中间值。一个有证明力的链路测试，优先于多个低价值的内部实现测试。

如果正在诊断 bug，先按 `diagnosis-workflow` 或 `incident-debugging` 建立反馈循环，再决定测试落点。

## 必须先读

规划、编写或解释非轻量测试前，读取项目 commands、contracts 和 context。同一任务已有覆盖当前测试入口、fixture 和命令的 readiness evidence 时复用；范围扩大、相关配置变化或命中 gap 时再使用 `project-setup`。

## 何时新增或更新测试

应新增或更新测试：

- 行为变化。
- bugfix。
- 重要边界条件。
- public API/proto/schema 变更。
- 数据库 query 或 migration 行为。
- 权限、租户、并发、错误处理、重试行为。
- 调试过程中发现的回归场景。

可跳过新增测试：

- 纯格式化、注释、简单文案、无行为变化的重命名。
- 现有测试已经覆盖的机械结构整理。

跳过测试时必须说明为什么没有行为影响、检查了哪条调用链或 public contract、现有相关测试是否覆盖该区域，以及仍运行了哪些检查。

## 测试入口硬门禁

- 优先从 `HTTP/RPC handler`、route、controller、resolver、event/job、CLI、页面/用户操作入口或 public package/module API 进入。
- 只有当低层入口本身是稳定 public contract、外层没有相关绑定/校验/权限/事务/副作用/错误映射，或已有测试覆盖外层时，才用 service/package/module 入口。
- 如果真实需求只能通过更高层 workflow 观察，不要只测试被改动的 helper。
- 用户明确要求完整链路时，不得降级为内部函数测试，除非先说明无法使用顶层入口的具体原因并获得确认。

细则见 [test-entry-and-value.md](references/test-entry-and-value.md)。

## 覆盖矩阵门禁

非轻量需求必须从 design/plan 的关键约束 ID 或 no-doc 最小约束清单出发设计测试。每个约束都必须有测试、手动验证、代码审查证据，或明确不可自动验证原因。

细则见 [coverage-matrix.md](references/coverage-matrix.md)。

## bugfix 和测试失败

- bugfix 测试必须先证明旧行为会失败，再证明修复后通过；无法证明时必须说明原因。
- 回归测试入口应与用户问题一致或等价，并断言用户可见结果和关键副作用。
- 测试失败后，不要立刻根据失败表象修改生产逻辑；先判断失败证明的是用户行为、测试不匹配，还是环境/不稳定问题。

细则见 [bugfix-and-failures.md](references/bugfix-and-failures.md)。

## 防御式代码清理验证

清理重复防御式代码时，优先证明外部行为和项目契约，而不是为每个内部 guard 补低价值测试。细则见 [defensive-cleanup-validation.md](references/defensive-cleanup-validation.md)。

## 汇报

测试结果汇报必须包含运行命令、结果、失败测试、失败分类、被测入口层级、为什么该入口足以证明目标行为，以及剩余风险。细则见 [reporting.md](references/reporting.md)。
