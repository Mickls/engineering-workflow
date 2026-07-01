# 需求设计模板

```md
# 需求设计

## 需求背景

## 需求总结

## 详细需求

## 输入契约 / 校验边界

- 项目契约来源：`<artifact-root>/project/contracts.md`
- 上下文 readiness：ready / bootstrapped / refreshed / targeted-refreshed / audit-only / skipped
- freshness：updated_at / source_commit / scan_scope / known_gaps
- 本需求涉及范围是否在 scan_scope 内：
- 已由入口或框架保证的标准化：
- 已由入口或接口定义拦截的非法输入：
- 已由构造函数、依赖注入、模块系统、框架生命周期、generated code 或 fixture 保证存在的依赖：
- 仍需本地校验的不安全边界：
- 本需求不得新增的重复防御式代码：

## 完整功能 / MVP 边界

- 本次是否为完整功能：
- 如果是 MVP，完整功能范围和后续补齐条件：
- 分阶段交付时每个后置项的原因、触发条件和恢复路径：

## 范围分类 / 过度实现检查

| 范围项 | 分类 | 当前处理 | 触发条件 / 不做理由 |
| --- | --- | --- | --- |
|  | required / defer-with-trigger / out-of-scope |  |  |

## 关键约束覆盖表

| ID | 类型 | 关键约束 | 影响入口/调用链 | 实现要求 | 验证意图 |
| --- | --- | --- | --- | --- | --- |
| C-001 | behavior |  |  |  |  |

## 数据结构 / 接口 / 配置

## UI 原型

- 原型路径：
- 覆盖状态：
- 未覆盖交互：
- 需要用户确认的问题：

## 兼容性策略

## 非目标范围

## 验收标准

## 关键假设

## 完整性检查
```

要求：

- 除非用户或项目规则明确要求其他语言，`design.md` 的正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。
- 如果项目规则要求 `design.md` 使用英文，英文 `design.md` 是权威来源；同时生成或更新同目录 `design.review.zh-CN.md`，记录源文件路径、`source_commit` 或更新时间、生成时间、权威来源声明、中文摘要、关键决策、关键约束、风险和待确认问题。
- `design.md` 是当前有效方案文档，不是推理日志或变更流水；不要写上一版方案、废弃概念、纠错痕迹或“原本/后来改为”等过程叙述。
- 更新已有 `design.md` 时，重写受影响章节并删除旧方案残留；只在当前方案需要时链接 ADR、out-of-scope 或 handoff，不在正文复述废弃方案。
- `关键约束覆盖表` 不能省略。
- 如果存在 `<artifact-root>/project/contracts.md`，必须在“输入契约 / 校验边界”中引用适用契约和 freshness；不存在或过期时，非轻量需求先用 `project-setup bootstrap` / `targeted-refresh`，除非用户禁止写入。
- 如果用户禁止创建或更新当前工作产物根目录，必须写清临时项目契约、证据来源、unknown 项和风险。
- 已由项目契约保证的标准化、validation 或依赖存在性，不得在内部实现中重复防御；如确需重复，必须在约束表写明新的未覆盖入口或安全理由。
- `范围分类 / 过度实现检查` 用于区分 `required`、`defer-with-trigger` 和 `out-of-scope`；未被用户要求且缺少当前业务证据的 speculative feature 不得进入关键约束覆盖表。
- `defer-with-trigger` 必须写清触发条件和恢复路径；不得用 YAGNI 隐藏完整功能闭环中的必要能力。
- 每个“必须/不能/即使/除非”都应检查是否需要单独约束 ID。
- 验收标准中的每条行为都应能追溯到约束 ID。
- 独立 UI 需求必须记录 `<artifact-root>/issues/<REQ>/prototype.html` 或等价原型路径。
- 如果用户明确要求跳过文档，非轻量任务仍需保留最小关键约束清单供交付核销。
