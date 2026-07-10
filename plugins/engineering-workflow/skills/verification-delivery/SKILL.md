---
name: verification-delivery
description: "用于声明任务完成前、代码或文档修改后、提交前，以及汇报 lint/test/build 结果、跳过检查、剩余风险和最终交付内容。"
---

# 验证和交付

## 目标

只有刚运行并读过结果的证据才能支持完成声明；最终回复必须区分已验证、未验证和剩余风险。

## 完成声明硬门禁

在说出或暗示“完成”、“已修复”、“通过”或“没有问题”之前：

1. 确认哪个命令或检查能证明结论。
2. 重新运行相关命令。
3. 阅读完整输出和退出状态。
4. 汇报真实结果。
5. 未运行的验证说明原因和风险。

不得依赖旧结果、推测、外部成功报告或部分输出。bugfix、incident 和 review 的特殊声明见 [completion-claims.md](references/completion-claims.md)。

## 交付核销

- 对照已确认 design/plan 或 no-doc 清单核销每个关键约束；高风险约束缺少证据时不得声明完成。
- 检查最终 diff 没有绕过统一实例化、DI/provider、generated code、schema/migration、事务或异步/手动生成流程；人工步骤报告 `blocked` / `manual-only`。
- diff 改变入口、schema、validation、DI/bootstrap、命令、CI、领域术语或核心边界时，交付前刷新对应项目上下文。
- 代码或脚本改动检查防御式代码、错误处理、依赖、抽象和最小正确实现；非轻量或中高风险任务运行 `scripts/audit-minimal-correct.sh`。

完整检查项见 [delivery-checklists.md](references/delivery-checklists.md)。

## 验证和汇报

- 按 diff 风险运行 lint、test、build/typecheck/compile；纯文档使用结构、链接、路径和回读检查。
- 验证命令的选择与跳过规则见 [validation-commands.md](references/validation-commands.md)。
- 最终回复包含修改摘要、关键路径、已运行命令和结果、未验证项、剩余风险以及需要用户处理的事项。

## Commit

提交前只暂存本次任务文件，尊重 ignore 规则，不使用 `git add -f` 绕过边界。commit 使用单行 Conventional Commit；细则见 [commit-rules.md](references/commit-rules.md)。
