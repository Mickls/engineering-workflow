---
name: architecture-review
description: "用于显式请求架构审查、模块深度评估、测试 seam 分析、重构机会识别或代码越来越难改的场景；输出候选改进和风险，不默认修改生产代码。"
---

# 架构审查

## 概述

本 skill 用于发现架构摩擦，而不是顺手重构。只有用户明确要求架构审查、重构机会、模块边界分析，或某片代码多次导致 bug 且难以测试时使用。

## 输入

优先读取：

- 当前工作产物根目录下的 `context.md` / `context-map.md`。
- 相关 `adr/`。
- 当前工作产物根目录 `issues/` 中 design/plan 的约束矩阵。
- 近期 bug、测试困难点、重复修改点。

## 审查维度

- 模块是否有清晰 interface，还是浅层转发。
- 复杂度是否集中在可测试 seam 后面。
- 调用方是否需要知道太多实现细节。
- 是否为了测试抽出内部 helper，反而绕开真实行为。
- 变更是否需要同时改很多无关位置。
- 错误、事务、权限、状态机或副作用是否散落。
- 测试是否只能测内部函数，无法从稳定入口证明行为。
- 是否存在单实现 interface / factory / strategy、只做浅层转发的 wrapper / adapter / service，或为了未来可能变化而提前抽象。
- 是否手写了标准库、框架、数据库、浏览器或平台 native feature 已经覆盖的能力。
- 是否为一个调用点创建中间类型、DTO、目录、配置或依赖。
- 是否新增依赖只替代几行稳定标准库或项目已有能力。
- 测试是否为了内部 helper 堆叠，而不是从稳定入口证明用户行为。

## 输出

默认输出中文 markdown。需要落盘时写入当前工作产物根目录的 `reports/`；用户需要可视化时可用 [report-template.md](references/report-template.md) 生成临时 HTML 到当前工作产物根目录 `reports/` 或系统 temp 目录，不写入生产代码。除非用户或项目规则明确要求其他语言，报告正文、标题、表格列名和状态解释都使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。

每个候选项包含：

- 涉及文件。
- 当前摩擦。
- 建议方向。
- 预期收益：locality、leverage、testability。
- 风险。
- 推荐强度：strong / worth-exploring / speculative。

对 over-engineering 候选，建议方向应说明可删除、可内联、可替换为标准库 / native feature / 已有能力，或需要等待第二个真实用例再抽象。

不要在同一轮默认实施架构重构。用户选择候选项后，再进入 `requirements-workflow` 或 `issue-slicing`。
