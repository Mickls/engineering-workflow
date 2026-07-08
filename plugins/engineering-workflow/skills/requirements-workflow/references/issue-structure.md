# Issue 结构

默认在目标仓库维护：

```text
.codex/engineering-workflow/issues/
```

该目录是 agent 工作产物，默认不主动纳入 git。除非用户明确要求共享这些文档，否则不要使用 `git add -f`，也不要为了纳入这些产物修改 ignore 规则。

## 普通需求

```text
.codex/engineering-workflow/issues/REQ-YYYYMMDD-NNN_需求简述/
  README.md
  design.md
  plan.md
```

## 大需求 / 跨模块需求

```text
.codex/engineering-workflow/issues/EPIC-YYYYMMDD-NNN_主题简述/
  README.md
  roadmap.md
  risks.md
  001_子需求A/
    README.md
    design.md
    plan.md
```

## 编号和状态

- 先检查现有 `.codex/engineering-workflow/issues/`，再决定新编号。
- 普通需求使用 `REQ-YYYYMMDD-NNN`，大需求使用 `EPIC-YYYYMMDD-NNN`。
- 需求简述保持短、可读、稳定。
- 当存在多个需求目录时，创建或更新 `.codex/engineering-workflow/issues/README.md`。
- 新需求写作时状态为 `draft`，准备给用户确认时改为 `reviewing`。
- 只有用户确认 design/plan，或明确要求继续实现时，状态才改为 `approved`。
- 开始实现时状态改为 `doing`。
- 只有存在验证证据后，状态才改为 `done`。
- 如果被阻塞，状态改为 `blocked`。

## README frontmatter

```md
---
id: REQ-YYYYMMDD-NNN
title: 需求标题
status: draft | reviewing | approved | doing | done | blocked | deferred
priority: P0 | P1 | P2
type: feature | fix | refactor | docs | chore
depends_on:
  - REQ-xxx
blocks:
  - REQ-yyy
updated_at: YYYY-MM-DD
---
```
