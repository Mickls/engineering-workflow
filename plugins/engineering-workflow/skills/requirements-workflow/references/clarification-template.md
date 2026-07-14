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
- 用户批准必须来自核销总结之后的明确消息；含糊表述保持 `waiting`。
- `clarification-approved` 后才能创建 design/plan。
- 重新打开时保留审计记录，重新汇总当前有效决定，不让 invalidated 内容进入 design。
