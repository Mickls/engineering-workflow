# 实施计划模板

```md
# 实施计划

## 总目标

## 完整功能交付路径

- 是否分阶段：
- 每个阶段如何共同达成完整功能：
- MVP 后续补齐条件：

## 需求覆盖矩阵

| 约束 ID | 实施步骤 | 预计代码落点 | 测试/验证入口 | 状态 |
| --- | --- | --- | --- | --- |
| C-001 | Step 1 |  |  | planned |

## 项目上下文 readiness / freshness

- 读取的 project 文档：
- 上下文 readiness 状态：ready / bootstrapped / refreshed / targeted-refreshed / audit-only / skipped
- freshness 判断依据：source_commit / scan_scope / evidence_paths / watch_patterns / known_gaps
- 本需求是否改变项目契约来源：
- 交付前需要回写的上下文：
- 本需求触发的实现路径契约：
- 正确路径需要用户手工生成/迁移/部署的步骤：

## 防御式代码审查 / 清理候选

| 候选 | 类型 | 证据来源 | 处理 | 验证 |
| --- | --- | --- | --- | --- |
|  | string-normalization / empty-check / dependency-guard / default-fallback / error-wrapping / logging | project contracts / 调用链 / public API | keep-boundary / remove-redundant / move-to-boundary / needs-evidence |  |

## 实施步骤

### 1. 步骤标题

- 修改范围：
- 目标：
- 产出：
- 依赖：
- 覆盖约束：
- 验证：

## 验证命令

## 最终回填状态

| 约束 ID | 实际落点 | 验证证据 | 状态 |
| --- | --- | --- | --- |
| C-001 |  |  | planned |

## 已接受风险和实施阻塞
```

要求：

- 除非用户或项目规则明确要求其他语言，`plan.md` 的正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。
- 如果项目规则要求 `plan.md` 使用英文，英文 `plan.md` 是权威来源；同时生成或更新同目录 `plan.review.zh-CN.md`，记录源文件路径、`source_commit` 或更新时间、生成时间、权威来源声明、中文实施摘要、关键步骤、覆盖约束、验证入口、风险和待确认问题。
- 每个 design 约束 ID 必须出现在 `需求覆盖矩阵`。
- `plan.md` 只能在 clarification 获得明确批准后创建；不得保留需要用户决定的开放问题。
- 非轻量需求必须填写“项目上下文 readiness / freshness”；缺失或过期时，先 bootstrap/refresh，或记录用户禁止写入时的临时契约和风险。
- 如果本需求会修改入口、schema、validation、DI/bootstrap、命令、CI、领域术语或核心业务边界，必须在计划中列出交付前回写的 project 文档。
- 如果本需求触发统一实例化、DI/provider、generated code、schema/migration、事务、异步或手动生成流程契约，必须在 `需求覆盖矩阵` 中列出正确实现路径、允许的停点和禁止绕过方式；正确路径需要用户手工生成时，相关约束交付状态应写 `blocked` / `manual-only`，不得写成已完整 verified。
- 如果本需求涉及新增或清理防御式代码，必须填写“防御式代码审查 / 清理候选”；无候选时写明已检查。
- 一个测试可以覆盖多个约束，不要为了表格制造低价值测试。
- 实现后回填实际代码落点、测试名、命令和状态。
- 独立 UI 需求必须包含“UI 原型确认”步骤和原型路径。
- 实施中发现会改变 design 的新问题时，先重新打开 clarification，不得把决定藏在实施步骤中。
- 交付前不得留下未解释的 `planned` / `todo`。
