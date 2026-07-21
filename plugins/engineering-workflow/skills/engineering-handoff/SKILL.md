---
name: engineering-handoff
description: "当长任务需要中断、切换会话、交给另一个 agent 或压缩工程上下文时使用；不用于管理 Codex runtime 或子 agent 生命周期。"
---

# 工程交接

## 概述

生成可让下一个 agent 或未来自己继续工作的交接文档。它记录项目事实，不替代 Codex 上下文压缩，也不指导子 agent 生命周期。

除非用户或项目规则明确要求其他语言，handoff 文档正文、标题、表格列名和状态解释都默认使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。

## 写入位置

优先：

- 当前需求目录下：`.codex/engineering-workflow/issues/<REQ-or-EPIC>/handoff.md`。
- 没有具体 issue 时：`.codex/engineering-workflow/handoffs/handoff-<timestamp>.md`。

`.codex/engineering-workflow/` 默认是 agent 工作产物，不主动纳入 git。不要把运行期缓存、secret 或无关日志写入交接。

## 内容

使用 [handoff-template.md](references/handoff-template.md)。

必须包含：

- 当前目标。
- 已确认的 design/plan 或约束矩阵路径。
- 当前有效 decision ledger、standing constraints、证据 `source_commit` 和失效条件。
- 已完成改动。
- 已运行验证和结果。
- 未验证项和风险。
- 当前工作区状态说明。
- 下一步建议。
- 建议后续使用的 skills。

不要复制已有文档的大段内容，引用路径即可。

上下文压缩或恢复后优先消费这份最小账本；`source_commit`、scope 和 watch patterns 未变化时复用已有证据，不重新扫描整个仓库。发现冲突时做一次集中 targeted refresh，不把恢复成本拆到后续每轮交互。
