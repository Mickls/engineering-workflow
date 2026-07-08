---
name: requirements-workflow
description: "用于需求分析、功能或 bugfix 范围确认、已有行为修改、issue/design/plan 文档、需求拆分，以及已确认需求发生变化的场景；除非任务明确属于轻量任务，否则编码前应先使用。"
---

# 需求工作流

## 目标

先理解需求和现有实现，再决定怎么改。本 skill 只做需求入口、硬门禁和 reference 路由；详细写作规范按需读取 `references/`。

默认工作产物写入目标仓库 `.codex/engineering-workflow/`。正文、标题、表格列名和状态解释默认中文；文件名、命令、API、代码标识符和状态枚举可保留英文。

## 何时使用

- 新功能、bugfix、重构、接口变更、数据结构变更或流程变更。
- 用户描述还不够明确，需要对齐术语、边界、验收标准。
- 需要创建或更新 `.codex/engineering-workflow/issues/` 下的 `design.md` / `plan.md`。
- 用户中途修改需求，可能影响已确认方案。
- 需求跨模块、跨多天或需要拆分子需求。

可跳过完整 issue 文档的轻量任务：纯解释、代码 review、格式化、注释、简单文案、无行为变化的小整理。跳过文档不等于盲改，最终仍需说明轻量判断、修改范围和验证方式。

## 必须先读

非轻量需求创建或更新 `design.md` / `plan.md` 前，先检查项目上下文：

- `.codex/engineering-workflow/project/project-profile.md`
- `.codex/engineering-workflow/project/commands.md`
- `.codex/engineering-workflow/project/contracts.md`
- `.codex/engineering-workflow/project/issue-workflow.md`
- `.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`

如果缺失、freshness 元数据缺失、超出 `scan_scope`、命中 `watch_patterns` / `known_gaps`，先使用 `project-setup bootstrap`、`refresh` 或 `targeted-refresh`。细则见 [context-readiness.md](references/context-readiness.md)。

## 澄清访谈

- 能通过代码、测试、配置、README、项目上下文或相邻实现确认的事实，先自行查证。
- 影响产品语义、实现路径、验收标准、兼容性、风险取舍、UI/交互、数据保留、权限、安全或交付范围的决策，交给用户确认。
- 一次只问一个问题，并给出推荐答案和取舍影响。
- 未达成 shared understanding 前，不创建最终 design/plan，不进入编码，不安排实现类任务。

细则见 [clarification-interview.md](references/clarification-interview.md) 和 [clarification-checklist.md](references/clarification-checklist.md)。

## 复杂度选择

| 类型 | 适用场景 | 文档要求 |
| --- | --- | --- |
| 轻量需求 | 纯解释、只读 review、格式/注释/文案、无行为变化的小整理 | 不创建 issue |
| 普通需求 | 单个功能或 bugfix、单条主调用链、影响范围清晰 | 创建一个 `REQ-*`，包含 `README.md`、`design.md`、`plan.md` |
| 大需求 / 跨模块需求 | 多阶段、多模块、多里程碑、依赖或风险明显 | 创建 `EPIC-*` 和子需求目录 |

不确定时先按普通需求处理。如果 plan 膨胀到无法独立实现或验证，使用 `issue-slicing` 拆成垂直切片。

## 需求设计硬门禁

- 修改型需求必须追溯入口、调用方、被调用方、数据来源、返回值、错误处理、副作用和已有测试。
- 新增型需求必须查阅相邻模块，理解项目术语，并参考相似实现。
- 设计必须覆盖完整功能闭环；除非用户明确要求 MVP，不得把必要能力降级为 MVP、后置项或非目标范围。
- 新增能力按 `required`、`defer-with-trigger`、`out-of-scope` 分类，避免 speculative scope 进入关键约束。
- `design.md` 必须包含关键约束覆盖表；`plan.md` 必须把每个约束映射到实施和验证。
- no-doc 非轻量例外仍需列出最小关键约束、预计落点和验证入口，交付前逐条核销。

细则见 [scope-and-overimplementation.md](references/scope-and-overimplementation.md)、[issue-structure.md](references/issue-structure.md)、[design-plan-authoring.md](references/design-plan-authoring.md) 和 [coverage-matrix.md](references/coverage-matrix.md)。

## UI 原型门禁

独立 UI 需求在确认 `design.md` / `plan.md` 前，必须生成静态 HTML 原型，并与文档一起交给用户 review。原型只用于确认视觉结构、交互意图和状态，不进入生产 lint/test/build 或反复精修循环。

细则见 [ui-prototype-gate.md](references/ui-prototype-gate.md)；复杂状态机、业务规则、数据模型或 API 形状可配合 `prototyping` 的 logic prototype。

## 用户确认门禁

创建或更新 `design.md` / `plan.md` 后必须停止当前回合，请用户 review 和确认。确认前不得编码、写测试、生成 migration/proto，或安排任何实现类/代码审查类工作。

只有用户明确要求跳过文档确认、或明确要求“写完方案后直接实现”，才可以越过本门禁，并且必须在回复中说明。细则见 [confirmation-and-change-gates.md](references/confirmation-and-change-gates.md)。

## 多语言文档

如果项目要求主文档使用英文，英文主文档是权威来源。非轻量且需要用户 review 的英文 durable artifact，必须在 `.codex/engineering-workflow/` 下生成或同步中文 review 辅助说明。细则见 [multilingual-review-aid.md](references/multilingual-review-aid.md)。

## 外部资料

第三方库、框架、SDK、OpenAPI、数据库特性或可能随版本变化的 API，优先使用官方文档确认；项目内部业务逻辑以仓库代码、测试和内部文档为准。引用外部资料时，在 `design.md` 中记录关键链接、版本或结论。
