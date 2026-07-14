---
name: requirements-workflow
description: "当任务涉及需求分析、新功能或 bugfix 范围、已有行为修改、issue/design/plan，或已确认需求发生变化时使用；除明确轻量任务外，编码前应先触发。"
---

# 需求工作流

## 目标

先理解需求和现有实现，再决定怎么改。本 skill 只做需求入口、硬门禁和 reference 路由；详细写作规范按需读取 `references/`。

工作产物默认写入目标仓库 `.codex/engineering-workflow/`，正文默认中文。

## 必须先读

非轻量需求开始澄清前，检查 `.codex/engineering-workflow/project/*` 和 context；缺失、stale、超出 `scan_scope` 或命中 gap 时先使用 `project-setup`。细则见 [context-readiness.md](references/context-readiness.md)。

## 设计前澄清门禁

- 非轻量需求先调查真实入口并创建 `README.md(status=clarifying)` 与 `clarification.md`；批准前不得创建或更新 design/plan。
- 能从代码、测试、配置和文档确认的事实先查证；不清楚的产品决策和重大技术决策一次只问一个，禁止猜测或推断批准。
- AI 完成动态设计树和反向遗漏检查后提交澄清核销总结；只有用户后续明确批准，才进入设计。
- 设计中发现会改变范围、行为、数据、接口、风险或验收的新问题时，重新打开澄清并确认受影响分支。

细则见 [clarification-interview.md](references/clarification-interview.md)、[clarification-checklist.md](references/clarification-checklist.md) 和 [clarification-template.md](references/clarification-template.md)。

## 复杂度选择

| 类型 | 适用场景 | 文档要求 |
| --- | --- | --- |
| 轻量需求 | 纯解释、只读 review、格式/注释/文案、无行为变化的小整理 | 不创建 issue |
| 普通需求 | 单个功能或 bugfix、单条主调用链、影响范围清晰 | 创建一个 `REQ-*`；先写 clarification，批准后写 design/plan |
| 大需求 / 跨模块需求 | 多阶段、多模块、多里程碑、依赖或风险明显 | 创建 `EPIC-*` 和子需求目录 |

不确定时先按普通需求处理。如果 plan 膨胀到无法独立实现或验证，使用 `issue-slicing` 拆成垂直切片。

## 需求设计硬门禁

- 修改型需求必须追溯入口、调用方、被调用方、数据来源、返回值、错误处理、副作用和已有测试。
- 新增型需求必须查阅相邻模块，理解项目术语，并参考相似实现。
- 设计必须覆盖完整功能闭环；除非用户明确要求 MVP，不得把必要能力降级为 MVP、后置项或非目标范围。
- 新增能力按 `required`、`defer-with-trigger`、`out-of-scope` 分类，避免 speculative scope 进入关键约束。
- `design.md` 只能包含已查证事实和已确认决定，并包含关键约束覆盖表；`plan.md` 必须把每个约束映射到实施和验证。
- no-doc 非轻量例外仍需列出最小关键约束、预计落点和验证入口，交付前逐条核销。

细则见 [scope-and-overimplementation.md](references/scope-and-overimplementation.md)、[issue-structure.md](references/issue-structure.md)、[design-plan-authoring.md](references/design-plan-authoring.md) 和 [coverage-matrix.md](references/coverage-matrix.md)。创建文档时使用 [design-template.md](references/design-template.md)、[plan-template.md](references/plan-template.md)；英文主文档需要中文 review 辅助说明时使用 [review-notes-template.md](references/review-notes-template.md)。

## UI 原型门禁

独立 UI 需求在澄清核销批准前生成静态 HTML 原型，用于确认视觉结构、交互意图和状态；logic prototype 也必须绑定一个明确的澄清问题。原型不进入生产 lint/test/build 或反复精修循环。

细则见 [ui-prototype-gate.md](references/ui-prototype-gate.md)；复杂状态机、业务规则、数据模型或 API 形状可配合 `prototyping` 的 logic prototype。

## 用户确认门禁

澄清批准后才能创建或更新 design/plan；文档完成后必须再次停止，请用户 review 和确认。设计批准前不得编码、写测试、生成 migration/proto，或安排实现类工作。

只有用户明确要求跳过文档确认、或明确要求“写完方案后直接实现”，才可以越过本门禁，并且必须在回复中说明。细则见 [confirmation-and-change-gates.md](references/confirmation-and-change-gates.md)。

## 多语言文档

如果项目要求主文档使用英文，英文主文档是权威来源。非轻量且需要用户 review 的英文 durable artifact，必须在 `.codex/engineering-workflow/` 下生成或同步中文 review 辅助说明。细则见 [multilingual-review-aid.md](references/multilingual-review-aid.md)。

## 外部资料

第三方库、框架、SDK、OpenAPI、数据库特性或可能随版本变化的 API，优先使用官方文档确认；项目内部业务逻辑以仓库代码、测试和内部文档为准。引用外部资料时，在 `design.md` 中记录关键链接、版本或结论。
