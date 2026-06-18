# Project Contracts 模板

`.codex/engineering-workflow/project/contracts.md` 用于记录当前项目已经由语言、框架、入口定义、依赖注入、模块系统、generated code 或 fixture 保证的工程契约。它不是通用教程，也不是愿望清单；每条保证都要有证据位置。

```md
# Project Contracts

## Scope

- 主要语言/运行时：
- 主要框架：
- 主要入口类型：
- 适用模块：
- 最近更新：

## Freshness

- updated_at:
- source_commit:
- scan_scope:
  -
- evidence_paths:
  -
- watch_patterns:
  -
- known_gaps:
  -

## Request / Input Normalization

| 入口/框架能力 | 已保证内容 | 证据位置 | 内部实现规则 |
| --- | --- | --- | --- |
|  |  |  |  |

## Validation Boundaries

| 入口/接口定义 | 已拦截内容 | 证据位置 | 内部实现规则 |
| --- | --- | --- | --- |
|  |  |  |  |

## Dependency Guarantees

| 依赖/资源 | 保证来源 | 证据位置 | 内部实现规则 |
| --- | --- | --- | --- |
|  |  |  |  |

## Still Unsafe Boundaries

| 边界 | 不保证内容 | 需要本地校验的位置 | 原因 |
| --- | --- | --- | --- |
|  |  |  |  |

## Refresh Notes

| 触发来源 | 影响契约 | 处理结果 | 更新时间 |
| --- | --- | --- | --- |
|  |  | refreshed / downgraded-to-unsafe / needs-evidence |  |

## Defensive Code Audit Patterns

| 类型 | 项目适用模式 | 说明 | 状态 |
| --- | --- | --- | --- |
| string-normalization |  | trim/strip/normalize/coercion 等重复标准化候选 | active / disabled |
| empty-check |  | nil/null/undefined/None/empty collection 等空值或空内容判断候选 | active / disabled |
| dependency-guard |  | 对已保证存在的依赖或资源重复判空候选 | active / disabled |
| default-fallback |  | 无证据默认值兜底候选 | active / disabled |
```

规则：

- 按语义记录契约，不绑定单一语言；Go、TypeScript、Python、JVM、C#、Rust 等写法只能作为项目模式示例。
- `Freshness` 必须记录当前契约的证据范围；无法获取 git commit 时写 `unknown` 和原因。
- `watch_patterns` 应覆盖会改变契约的入口、schema、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置和相关文档。
- 当当前任务涉及的入口、模块或命令不在 `scan_scope` 中时，先 targeted refresh，再决定能否信任旧契约。
- “已保证内容”必须来自代码、schema、middleware、framework docs、generated code、bootstrap、constructor、fixture 或其他可检查证据。
- 如果请求参数已经在入口完成标准化，内部 service/use-case/domain 层不得重复做同类标准化。
- 如果接口定义已经拦截空值或非法值，内部实现不得重复做同类空值、空内容或格式判断。
- 如果依赖已由构造函数、DI container、module provider、framework lifecycle、generated code 或 fixture 保证存在，内部方法不得重复判断依赖是否存在。
- public/exported API、外部数据读取、反序列化、旧数据兼容、第三方回调、并发/lifecycle 边界仍可保留本地校验，但必须记录在 `Still Unsafe Boundaries` 或对应设计文档中。
- 证据不足时不要写成“已保证”；写入 `Still Unsafe Boundaries` 或待确认项。
- 如果 refresh 后发现旧保证不再成立，删除或降级对应保证，并在 `Refresh Notes` 记录原因。
