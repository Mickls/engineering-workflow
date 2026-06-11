# 覆盖矩阵指南

覆盖矩阵用于防止 design/plan 写清楚但实现遗漏。

## 关键约束类型

- `behavior`：用户可见行为。
- `boundary`：边界条件，例如 root 外、exclude、权限、租户。
- `compatibility`：旧配置、旧接口、旧数据兼容。
- `safety`：数据删除、幂等、并发、权限、安全。
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
