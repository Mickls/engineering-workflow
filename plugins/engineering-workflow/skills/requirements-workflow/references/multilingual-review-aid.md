# 多语言 Review 辅助说明

如果用户或项目规则要求主文档使用英文：

- 英文 `README.md`、`design.md`、`plan.md` 或项目正式文档是权威来源，不得擅自改成中文。
- 对非轻量且需要用户 review 的英文文档，必须生成或更新中文 review 辅助说明，帮助中文用户理解和确认。
- 触发范围不限于 `.codex` issue 文档，也包括项目自定义 durable artifacts，例如 exploration note、feature inventory、runbook、checklist、report、ADR、protocol、story、support content。

## 默认位置

- 英文主文档位于 `.codex/engineering-workflow/issues/<REQ-or-EPIC>/`：中文辅助说明优先写在同目录，例如 `design.review.zh-CN.md`、`plan.review.zh-CN.md` 或 `review-notes.zh-CN.md`。
- 英文主文档位于项目正式目录：中文辅助说明写入 `.codex/engineering-workflow/review-notes/<mirrored-path>.zh-CN.md`，保留原路径层级，避免污染生产文档目录。

## 内容要求

中文辅助说明不是逐字翻译，不作为实现权威。应包含：

- 英文源文件路径。
- `source_commit` 或更新时间。
- 生成时间。
- “英文主文档为准”的声明。
- 中文摘要。
- 关键决策。
- 关键约束。
- 风险。
- 待确认问题。
- review 建议。

如果项目规则禁止 duplicate translated reports 或 bilingual protocol variants，`.codex/engineering-workflow/` 下的中文 review aid 不视为重复报告或双语协议。只有项目或用户明确禁止任何中文辅助文件时，才跳过生成，并在最终回复说明原因。
