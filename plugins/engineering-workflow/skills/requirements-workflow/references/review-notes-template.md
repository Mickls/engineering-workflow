# 中文 Review 辅助说明模板

用于主文档必须使用英文、但需要中文用户参与 review 的场景。该文档是理解辅助，不是权威来源。

适用对象不只包括 `design.md` / `plan.md`，也包括项目自定义的英文 durable artifact，例如 exploration note、runbook、checklist、report、ADR、protocol、story、support content 或其他需要用户 review 的英文文档。

```md
# 中文 Review 辅助说明

## 元信息

- 英文源文件：
- 权威来源：英文源文件为准
- source_commit / 更新时间：
- 生成时间：
- 适用范围：

## 中文摘要

## 关键决策

## 关键约束

| 约束 ID | 中文说明 | 对应英文位置 | Review 关注点 |
| --- | --- | --- | --- |
| C-001 |  |  |  |

## 风险和待确认问题

## Review 建议
```

要求：

- 不逐字翻译英文主文档，不复制成第二份权威文档。
- 必须明确英文源文件路径和“英文源文件为准”。
- 如果项目规则禁止 duplicate translated reports 或 bilingual protocol variants，本文件仍应作为当前工作产物根目录下的 review aid 生成；它不是重复报告，也不进入生产文档目录。
- 重点解释背景、结论、关键约束、风险、待确认问题和用户需要 review 的点。
- 英文主文档更新后，必须检查本说明是否过期；无法同步时，在最终回复中说明风险。
