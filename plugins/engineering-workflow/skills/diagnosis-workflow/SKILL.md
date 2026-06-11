---
name: diagnosis-workflow
description: "用于普通 bug、失败测试、性能回退、难以解释的异常行为和本地可排查问题；要求先建立可靠反馈循环，再复现、提出可证伪假设、逐一验证、最小修复和回归验证。"
---

# 诊断工作流

## 概述

普通 bug 也不能靠猜。先建立能稳定证明问题存在的反馈循环，再定位根因。线上事故、数据误删、幂等、并发等高风险问题优先使用 `incident-debugging`；本 skill 处理更一般的本地诊断。

## 阶段

### 1. 建立反馈循环

优先级：

1. 从真实入口或 public contract 出发的 failing test。
2. `curl` / HTTP 脚本。
3. CLI 命令 + fixture。
4. 浏览器自动化脚本。
5. 捕获请求、事件或日志后的 replay。
6. 最小 harness。
7. property / fuzz / stress loop。
8. 人机协作脚本，参考 [hitl-loop.template.sh](scripts/hitl-loop.template.sh)。

反馈循环必须能观察用户描述的问题，而不是附近的另一个失败。

如果无法建立反馈循环，说明已尝试路径、缺失信息和下一步需要用户提供什么；不得直接猜测修复。

### 2. 复现

- 运行反馈循环。
- 捕获失败输出、错误、数据状态或副作用。
- 对不稳定问题，提高复现概率，而不是假装稳定。

### 3. 提出假设

修改代码前列出 3-5 个可证伪假设。

格式：

```text
如果 X 是根因，那么改变/观察 Y 会让 Z 发生。
```

每个探针只能对应一个假设，避免一次改变多个变量。

### 4. Instrument

- 优先 debugger / REPL / targeted log。
- debug log 必须带唯一前缀，例如 `[DEBUG-a4f2]`。
- 不要“到处打日志再 grep”。
- 性能问题先建立 baseline，再改代码。

### 5. 修复和回归

- 只改已证明根因。
- 如果存在正确测试 seam，先把最小复现固化成回归测试。
- 如果不存在正确 seam，记录这是架构或测试能力缺口。
- 修复后同时运行最小复现和原始反馈循环。

### 6. 清理和交付

- 删除所有 debug instrumentation，用唯一前缀 grep 确认。
- 删除或移动 throwaway harness。
- 汇报根因、验证命令、仍未覆盖风险。

测试失败处理遵循 `testing-policy`，交付声明遵循 `verification-delivery`。
