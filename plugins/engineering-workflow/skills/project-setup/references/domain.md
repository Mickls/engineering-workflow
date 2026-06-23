# Domain 文档规则

`.codex/engineering-workflow/context.md` 用于记录项目领域语言。它不是 spec、不是设计文档、不是实现说明。

推荐格式：

```md
# 项目领域上下文

## Freshness 元数据

- updated_at:
- source_commit:
- scan_scope:
  -
- evidence_paths:
  -
- watch_patterns:
  - docs/**
  - README*
  - domain docs / product docs / glossary sources
- known_gaps:
  -

## 领域语言

**术语**：
一到两句话定义这个领域概念。
_避免使用_：不建议使用的同义词
```

规则：

- 除非用户明确要求其他语言，领域上下文正文、标题、表格列名和状态解释都必须使用中文；领域 canonical term、代码标识符、文件名和引用路径可以保留英文。
- 只记录项目领域概念，不记录通用编程概念。
- 定义要短，说明它是什么，不解释实现。
- 当多个词表达同一概念时，选择一个 canonical term。
- 输出、测试名、issue 标题和方案中应优先使用 canonical term。
- 如果用户使用的术语和 `.codex/engineering-workflow/context.md` 冲突，先指出冲突并确认。
- 当产品文档、领域状态机、核心业务边界或术语来源变化后，需要 targeted refresh 本文件。
- 无证据或只在单次对话中出现的词，不要直接沉淀为 canonical term；先写入 `known_gaps` 或需求文档待确认项。

ADR 放在 `.codex/engineering-workflow/adr/`，仅记录：

- 难以逆转的架构或技术选择。
- 未来读者容易觉得奇怪的决策。
- 有真实替代方案和取舍的决策。
