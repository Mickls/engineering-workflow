# 澄清记录模板

```md
# 需求澄清记录

## 状态

- 当前状态：clarifying / awaiting-clarification-approval / clarification-approved / reopened
- 关联需求：
- 证据 freshness：

## 当前目标

## 已查证事实

| 事实 | 证据位置 | 影响分支 |
| --- | --- | --- |

## 动态设计树

## 问题地图

| ID | 来源 | 实际场景 | decision owner | 依赖 | 状态 |
| --- | --- | --- | --- | --- | --- |
| Q-001 | current / introduced / conditional |  | user / AI |  | discovered / explaining / ready-for-decision / understood / confirmed / delegated / deferred / invalidated |

## 当前问题

- active question：none / Q-001
- 为什么现在必须决定：
- 为什么不能由项目证据直接决定：
- 用户可见选项和代价：
- 推荐及可能错误的条件：
- 技术证据附录：

## 已确认决策

| ID | 决策 | 用户确认来源 | 依赖 | 状态 |
| --- | --- | --- | --- | --- |
| D-001 |  |  |  | still-valid / needs-reconfirmation / invalidated |

## 拒绝方向

## 风险

| 风险 | 分类 | 证据 | 处理 / 用户接受 |
| --- | --- | --- | --- |

## 未解决问题

## 澄清进度

- 当前问题：
- 已确认：
- 待确认：
- 暂缓：
- 新增问题：

## 反向遗漏检查

## 澄清核销总结

- 证据事实：
- 有效决定：
- 目标和边界：
- 设计树覆盖：
- 剩余未知：
- informed override：none / ...
- 批准状态：waiting / approved
```

规则：

- 只记录影响设计或验收的事实、决定和依赖，不逐字转录聊天。
- 问题进入地图前必须证明来源和实际场景；`speculative` 只记录到风险或拒绝方向，不成为用户问题。
- 对话中只允许一个 active question；`understood` 不等于 `confirmed`，`deferred` 不阻塞无依赖分支。
- 用户疲劳、暂停或含糊回复时保持原状态，不新增问题、不推断批准。
- 用户批准必须来自核销总结之后的明确消息；含糊表述保持 `waiting`。
- `clarification-approved` 后才能创建 design/plan。
- 重新打开时保留审计记录，重新汇总当前有效决定，不让 invalidated 内容进入 design。
