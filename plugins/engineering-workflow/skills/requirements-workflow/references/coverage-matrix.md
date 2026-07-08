# 覆盖矩阵指南

覆盖矩阵用于防止 design/plan 写清楚但实现遗漏。

## 关键约束类型

- `behavior`：用户可见行为。
- `boundary`：边界条件，例如 root 外、exclude、权限、租户。
- `compatibility`：旧配置、旧接口、旧数据兼容。
- `safety`：数据删除、幂等、并发、权限、安全。
- `architecture`：项目实现路径契约，例如统一实例化、DI/provider、generated code、schema/migration、事务边界、异步/手动生成流程。
- `manual`：无法自动化但必须验证的人工路径。

## 状态

- `planned`：已计划，尚未实现。
- `implemented`：已有实现落点，尚未验证。
- `verified`：已有实现和验证证据。
- `manual-only`：只能手动验证，已写明步骤和观察点。
- `blocked`：被信息、环境或用户决策阻塞。
- `not-applicable`：有证据证明不适用。

## 核销规则

- 交付前不得存在未解释的 `planned`。
- 高风险约束缺少验证证据时，不得说完成。
- 如果实现时发现新约束，先更新 design/plan，再继续。
- `architecture` 约束必须有代码审查证据或验证证据；正确路径依赖用户手工生成、迁移或部署时，状态应保留为 `blocked` / `manual-only` 并说明下一步，不能通过手改生成产物、绕开 DI/provider 或降低项目边界来改成 `verified`。
