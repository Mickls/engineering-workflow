---
name: issue-slicing
description: "当需求、PRD、design/plan 或执行计划过大，无法由单个可独立实现和验证的交付闭环承载时使用；不用于按数据库、DAO、接口或前端做水平分层拆分。"
---

# Issue Slicing

## 概述

把大需求拆成可独立完成、可验证、可交付的垂直切片。水平任务可以存在，但不能成为唯一拆分方式。

## 拆分规则

优先按用户可观察行为拆：

- 每个切片尽量经过完整调用链。
- 每个切片完成后能被测试、演示或手动验证。
- 每个切片必须关联需求覆盖矩阵中的约束 ID。
- 拆分结果需要回写到 `.codex/engineering-workflow/issues/<REQ-or-EPIC>/plan.md`、`roadmap.md` 或对应需求记录，保持覆盖矩阵同步。
- 高风险数据变更、migration、proto/schema 可作为支撑任务，但必须服务于某个垂直切片。
- 不要把“写 DAO”“写 proto”“写测试”当成孤立交付，除非它们本身就是稳定 public contract 或基础设施任务。

## 输出格式

```md
| Slice | 类型 | 覆盖约束 | 完成后可观察结果 | 依赖 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
| S-001 | AFK/HITL | C-001,C-002 | ... | none | ... |
```

类型：

- `AFK`：行为、验收、项目模式和验证入口均已确认，可独立完成并在自审后继续下一切片。
- `HITL`：出现新决定、方案偏离、证据缺口、手动步骤、未覆盖风险或用户 review budget 命中，必须暂停。

拆分后需要请用户确认粒度、依赖和优先级。确认前不得直接进入编码；批准后的连续执行和停点细则见 [execution-review-boundaries.md](references/execution-review-boundaries.md)。
