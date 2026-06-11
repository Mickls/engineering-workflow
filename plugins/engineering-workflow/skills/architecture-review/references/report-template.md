# Architecture Review Report 模板

```md
# Architecture Review

## Scope

- 入口：
- 相关模块：
- 读取的 context / ADR：

## Candidates

### Candidate 1: 标题

- Files:
- Problem:
- Proposal:
- Benefits:
- Risks:
- Recommendation: strong / worth-exploring / speculative

## Top Recommendation

先做什么，为什么。
```

如果生成 HTML 报告，默认写入 `.codex/engineering-workflow/reports/architecture-review-<timestamp>.html`，或在用户要求临时文件时写入系统 temp 目录。不要写入生产代码路径。
