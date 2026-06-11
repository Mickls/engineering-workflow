---
name: engineering-handoff
description: "用于长任务中断、切换会话、交给另一个 agent 或需要压缩工程上下文时生成项目交接文档；只记录工程状态，不管理 Codex runtime 或子 agent 生命周期。"
---

# 工程交接

## 概述

生成可让下一个 agent 或未来自己继续工作的交接文档。它记录项目事实，不替代 Codex 上下文压缩，也不指导子 agent 生命周期。

## 写入位置

优先：

- 当前 issue 目录下：`handoff.md`。
- 没有 issue 时：系统 temp 目录。

不要把运行期缓存、secret 或无关日志写入交接。

## 内容

使用 [handoff-template.md](references/handoff-template.md)。

必须包含：

- 当前目标。
- 已确认的 design/plan 或约束矩阵路径。
- 已完成改动。
- 已运行验证和结果。
- 未验证项和风险。
- 当前工作区状态说明。
- 下一步建议。

不要复制已有文档的大段内容，引用路径即可。
