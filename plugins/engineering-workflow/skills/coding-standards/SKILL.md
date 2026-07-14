---
name: coding-standards
description: "当任务进入项目代码实现、修改或 code review 阶段时使用；涉及 validation、错误处理、日志、数据库/migration、依赖、资源或并发时也应触发，不用于纯需求分析。"
---

# 编码规范

## 目标

按现有项目风格写最小正确实现。本 `SKILL.md` 只保留入口规则和硬门禁；详细规范按任务类型读取 `references/`。

## 核心原则

- 先理解现有实现，再按已确认约束做最小正确改动，优先复用项目能力、标准库、框架/native feature 和既有依赖。
- 校验放在调用链顶层或真实外部边界。
- 不为了“保险”堆防御式代码；项目契约已保证的输入、依赖和生命周期，内部实现必须信任。
- 错误不能静默通过，不用无证据兜底隐藏未知问题。
- 关键路径要为排查保留足够 traceability 和 observability。
- 不做无关重构，不引入无关抽象。
- 实现必须贴合已确认的 design/plan、no-doc 最小关键约束清单和项目既有风格。

## 编码前必须做

- 阅读相关入口、相似实现、已确认 design/plan 或 no-doc 约束清单。
- 读取项目 commands、contracts 和 context；缺失、stale 或超出扫描范围时先使用 `project-setup`。
- 确认语言、框架、lint/test/build、生成流程，以及哪些输入已在真实边界校验。
- 识别本次 diff 触发的 DI/provider、generated code、schema/migration、事务、异步或手动流程约束 ID。

细则见 [context-and-coverage.md](references/context-and-coverage.md)。

## 实现硬门禁

- 每改一个核心入口或共享 helper，回看它关联的约束 ID，避免只实现 happy path。
- 遇到 design/plan 没写清或实现不可行的约束，暂停并说明冲突，不用自认为合理的实现替代。
- 不新增 speculative abstraction、未确认配置项、单实现 interface / factory / strategy、浅层 wrapper，或“以后可能用”的扩展点。
- 不为几行稳定标准库、框架或平台能力能完成的事情新增依赖。
- 不绕过项目实现路径契约：不得在 action/handler/helper 内临时重建应由统一实例化提供的依赖，不得手改 generated output 代替 source/schema/provider 变更，不得为了让当前工作树临时编译通过而跳过 codegen/migration/wire 等真实流程。
- 正确路径需要用户手工生成、迁移或部署时，保留 source/schema/provider 侧变更并把约束状态标为 `blocked` / `manual-only`；不得用绕过方式把它伪装成已验证完成。
- 不为了少写代码删除或弱化 trust boundary validation、权限、安全、数据一致性、幂等、并发、资源释放、accessibility 或必要验证。
- 编码后在 plan、issue 记录或 no-doc 最小约束清单中回填实际代码落点和状态。

细则见 [minimal-correct-implementation.md](references/minimal-correct-implementation.md)。

## 校验和防御式代码

- 外部输入应在 handler/controller/resolver、CLI、event/job、webhook、前端提交、public API、序列化/反序列化、文件、网络和数据库读取等真实边界校验。
- 内部函数不重复做防御式校验，除非它本身是外部边界、存在未校验路径、项目模式要求本地校验，或合法内部调用会不可避免地产生未捕获异常。
- 新增 `string-normalization`、`empty-check`、`dependency-guard`、`default-fallback`、`silent-error`、无证据 retry/degrade 等候选时，必须有边界证据；否则删除或移动到真实边界。
- 清理存量防御式代码时按 `keep-boundary`、`remove-redundant`、`move-to-boundary`、`needs-evidence` 分类。

细则见 [validation-and-defensive-code.md](references/validation-and-defensive-code.md)。

## 错误、日志和可观测性

- 遵循项目已有 error type、exception、error code、wrapping、result 和响应映射约定。
- 不吞错，不写空 catch，不忽略返回的 error，不把异常只记日志后当作成功继续执行。
- 不用无证据 fallback、重试、降级或缓存值掩盖未知问题；合法 fallback 必须有业务契约、触发条件和可观测信号。
- 关键路径日志只记录排查所需的业务上下文，不记录 secret、token、密码、完整隐私数据或大 payload。
- 临时 debug log、print、console.log 和断点残留必须清理。

细则见 [error-logging-observability.md](references/error-logging-observability.md)。

## 任务特化规则

- 数据库 / migration、资源释放、异步并发、依赖变更：见 [database-resources-dependencies.md](references/database-resources-dependencies.md)。
- Go、TypeScript / JavaScript、Python、Java / Kotlin / JVM 语言补充：见 [language-notes.md](references/language-notes.md)。
- 中高风险代码交付前 review checklist：见 [review-checklist.md](references/review-checklist.md)。
