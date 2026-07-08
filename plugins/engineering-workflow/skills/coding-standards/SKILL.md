---
name: coding-standards
description: "用于实现、修改或 review 任意语言的项目代码，包括调用链理解、复用优先、校验位置、错误处理、日志、数据库/migration、依赖变更、资源/并发处理、项目风格对齐，以及语言特化规则。"
---

# 编码规范

## 概述

按现有项目风格写代码。这个 skill 适用于所有编程语言和技术栈；语言特化规则只在当前项目使用该语言时补充适用。

核心原则：

- 先理解现有实现，再修改代码。
- 追求最小正确实现，先复用，再实现。
- 校验放在调用链顶层或真实外部边界。
- 不为了“保险”堆防御式代码。
- 错误不能静默通过，不用无证据兜底隐藏未知问题。
- 关键路径要为排查保留足够 traceability 和 observability。
- 项目契约已保证的输入、依赖和生命周期，内部实现必须信任，不重复防御。
- 不做无关重构，不引入无关抽象。
- 让实现贴合已确认的 design/plan、最小关键约束清单和项目既有风格。

## 工作顺序

修改生产代码前：

- 阅读相关入口和周边实现。
- 读取项目上下文：`.codex/engineering-workflow/project/project-profile.md`、`.codex/engineering-workflow/project/commands.md`、`.codex/engineering-workflow/project/contracts.md`、`.codex/engineering-workflow/project/issue-workflow.md`、`.codex/engineering-workflow/context.md` 或 `.codex/engineering-workflow/context-map.md`、相关 `.codex/engineering-workflow/adr/`。
- 如果关键上下文缺失、freshness 元数据缺失、当前任务命中 stale 信号或涉及未扫描范围，先使用 `project-setup bootstrap`、`refresh` 或 `targeted-refresh`；用户禁止写入时记录临时项目契约和风险，不得凭空发明项目术语或重复校验规则。
- 找到同项目中的相似代码。
- 识别已有 helper、service、repository/DAO、client、错误风格、日志风格和测试。
- 确认当前语言、框架、包管理器、lint/test/build 命令和生成代码流程。
- 确认哪些输入已经在调用链顶层完成校验。
- 将修改范围限制在当前需求需要的行为上。
- 如果存在 `.codex/engineering-workflow/issues/` 下的 issue/design/plan，先读取关键约束覆盖表和需求覆盖矩阵，不允许只凭总体描述开始编码。
- 如果用户要求跳过文档且任务为非轻量，先读取或建立最小关键约束清单、实现落点和验证入口；没有这些约束时不得开始编码。
- 在选方案前执行“最小正确实现阶梯”，确认没有更简单且正确的既有能力、标准库、框架或平台原生能力可以覆盖本需求。

## Context Freshness Gate

编码前必须判断项目上下文是否足够新：

- 读取 `contracts.md`、`commands.md`、`project-profile.md` 中的 `Freshness`、`scan_scope`、`evidence_paths`、`watch_patterns` 和 `known_gaps`。
- 当前改动涉及 route/controller/handler/resolver、CLI/job、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置时，检查这些来源是否在 `scan_scope` 中。
- 如果 git `HEAD` 与 `source_commit` 不同，且变更文件命中 `watch_patterns`，先 targeted refresh。
- 如果无法判断 freshness，非轻量编码默认先 targeted refresh；轻量只读或纯文档任务可说明低置信风险后继续。

缺少或过期的项目契约不能被当作“上游已保证”的证据。此时要么刷新契约，要么把相关输入、依赖或生命周期保证降级为未知边界，再沿调用链寻找真实证据。

## 实现覆盖门禁

非轻量需求编码时，必须把实现和已确认 design/plan 或最小关键约束清单逐条对齐。

编码前：

- 从 `design.md` / `plan.md` 提取所有关键约束 ID；如果是 no-doc 例外，从临时计划或回复中的最小关键约束清单提取约束。
- 对即将修改的入口、函数、接口、job 或流程，搜索它们在 design/plan 中出现的位置，避免漏掉同名入口的边界要求。
- 对照项目契约画像，确认哪些输入、依赖或生命周期已经由框架、接口定义、构造函数、依赖注入、模块系统、generated code 或 fixture 保证。
- 明确本轮代码改动会覆盖哪些约束，哪些约束只由测试、文档或人工验证覆盖。

编码中：

- 每改一个核心入口或共享 helper，回看它关联的约束 ID，确认没有只实现 happy path。
- 遇到 design/plan 没写清或实现不可行的约束，暂停并说明冲突，不要用自认为合理的实现替代。
- 不为了覆盖矩阵新增无关代码；矩阵用于防漏，不用于扩大范围。

编码后：

- 在 `plan.md`、对应 issue 记录或 no-doc 最小约束清单中回填实际代码落点和状态。
- 每个关键约束必须处于 `implemented`、`verified`、`manual-only`、`blocked` 或 `not-applicable` 之一。
- `not-applicable` 必须写证据，例如调用链不可达、需求已变更、用户确认不做。
- 存在未解释的 `planned`、`todo`、空实现落点或空验证入口时，不得进入完成声明。

## 最小正确实现阶梯

实现功能时按以下顺序寻找最小且正确的方案。这里的“最小”是减少不必要的自定义代码、依赖、抽象和文件数，不是牺牲正确性。

1. 确认这个需求是否必须构建。现有行为、配置、文档、已有脚本、平台能力或清晰手动流程已经覆盖时，说明证据并避免新增实现。
2. 当前项目已有工具函数、通用模块、repository/DAO、service、client、组件、helper、测试 fixture 或错误处理模式能覆盖时，复用它们，不重新发明。
3. 当前语言的标准库、运行时、框架原生能力、数据库约束、浏览器或平台 native feature、系统命令或项目已采用的官方工具能覆盖时，优先使用。
4. 项目已经引入的第三方库能覆盖时，使用既有依赖，不为局部便利新增依赖。
5. 只有以上都不成立时，写最小必要的自定义实现。

最小正确实现要求：

- 不新增 speculative abstraction、未确认配置项、单实现 interface / factory / strategy、只做浅层转发的 wrapper，或“以后可能用”的扩展点。
- 不为了在局部链路上传递少量值而新增中间类型、目录或协议。
- 不为几行稳定标准库、框架或平台能力能完成的事情新增依赖。
- 如果用户要求复杂方案但简单方案已能覆盖目标，应先交付或设计简单方案，并在 design/plan 或回复中说明何时需要升级。
- 用户明确要求完整方案、已确认的完整功能闭环、高风险边界和合规要求不能被“最小实现”降级为 MVP。

不能为了少写代码删除或弱化：

- trust boundary validation、权限、安全、租户隔离和资源归属。
- 防止数据丢失、重复写入、幂等破坏或状态不一致的错误处理。
- 并发、异步、资源释放和生命周期安全。
- accessibility、真实硬件或真实环境校准。
- 用户明确要求保留的行为。
- 非平凡逻辑的验证入口。

新增依赖必须说明：

- 它解决什么问题。
- 为什么项目已有能力、标准库或既有依赖不足。
- 运行时、维护、license、兼容性和体积风险。
- lockfile、生成代码或构建配置是否需要同步更新。
- 依赖变更后的验证结果。

## 校验位置

外部输入应在调用链顶层校验：

- `HTTP/RPC handler`、controller、route、resolver。
- `CLI` 命令入口。
- `event/job` 接收处、定时任务入口、消息消费处、webhook。
- 前端表单提交、URL/query 解析、跨窗口/跨线程消息入口。
- 会被当前模块外部使用的 public/exported API。
- 序列化、反序列化、文件、网络和数据库读取的边界。

顶层校验示例按语义分类，不绑定单一语言：

- nil / null / undefined / None / Optional empty / 空请求 / 空集合。
- 用户输入字符串或结构化输入的 trim / strip / normalize / 格式化 / 类型转换。
- 枚举合法性。
- 必填 ID。
- 分页边界。
- 权限、租户范围和资源归属。
- 外部数据结构版本和兼容性。

内部函数不重复做防御式校验，除非：

- 该函数本身就是外部边界。
- 确实存在未校验的不安全路径能到达这里。
- 项目已有模式要求该边界本地校验。
- 不校验会让合法内部调用不可避免地产生 panic、crash 或未捕获异常。

如果不确定数据是否安全，先向上追溯到原始来源，再决定是否加校验。如果上游已经保证非空、类型正确或完成标准化，下游应信任该契约。

### 防御式代码候选

以下是需要审查的候选类别，具体写法随语言和框架变化：

- `string-normalization`：重复 trim、strip、normalize、大小写转换、空白折叠、类型 coercion。
- `empty-check`：重复 nil、null、undefined、None、Optional empty、空字符串、空集合、空对象判断。
- `dependency-guard`：对已由构造函数、依赖注入、模块系统、框架生命周期、generated code 或 fixture 保证存在的 service、repository/DAO、client、config、logger、context、component/provider 反复判空。
- `default-fallback`：无证据地把缺失、非法或异常输入替换成默认值继续执行。
- `error-wrapping` / `logging`：多层重复 wrapping、重复日志或重复错误映射。
- `silent-error`：空 catch、忽略 error/exception、只记录日志但继续执行、吞掉 async/goroutine/task 错误。
- `masked-retry-degrade`：无证据重试、降级、跳过步骤或返回缓存值，使真实错误不再暴露。

这些候选不是一律禁止。保留它们必须有边界证据：public/exported API、外部数据读取、反序列化、旧数据兼容、第三方回调、并发/lifecycle 安全、真实未校验入口，或项目明确要求的本地防线。

如果 `.codex/engineering-workflow/project/contracts.md` 已说明某类输入已标准化、非法值已拦截或依赖已保证存在，内部实现不得重复做同类防御。发现新入口不满足契约时，先更新契约或 design/plan，再决定是否补校验。

### Fail Fast 和可观测性

- 不用 fallback、默认值、空 catch、`return nil`、`return true`、忽略 promise/future/task/goroutine 错误等方式让未知错误继续流转。
- 合法的 fallback 必须来自明确业务契约，例如旧数据兼容、用户明确选择的降级模式、外部依赖失败时已确认的产品行为；同时要留下可观测信号。
- 如果错误会跨边界暴露给用户或调用方，边界层应按项目风格映射成可理解响应；内部仍要保留错误类型、错误码、上下文或 cause，不能只返回笼统失败。
- 难以定位的问题不要做表面修复。先补充 targeted log、metric、trace、事件记录或复现 harness；如果当前信息不足，应明确说明缺少哪些观测点和下一步如何补。
- 新增观测点应服务具体假设或关键路径，不“到处打日志”。临时 debug instrumentation 必须可 grep、可清理；长期日志必须符合项目日志风格。

### 契约变更回写

编码完成后检查本次 diff 是否改变项目契约来源：

- 新增或调整入口、schema、middleware、validation、OpenAPI/proto、GraphQL、表单规则。
- 新增或调整 DI/bootstrap、constructor、module provider、framework lifecycle、generated code。
- 修改 lint/test/build/package/CI 配置。
- 修改领域术语、状态机、核心业务边界或跨模块约定。

如果命中这些变化，交付前必须使用 `project-setup targeted-refresh` 更新对应 `contracts.md`、`commands.md`、`project-profile.md`、`context.md` 或 ADR，并刷新 metadata。用户禁止写入 `.codex/engineering-workflow/` 时，需要在最终回复中说明未回写的上下文和剩余风险。

### 新增防御式代码审查

编码后检查本次 diff 是否新增防御式代码候选：

- 每个新增候选必须能指向边界证据。
- 无证据候选必须删除，或把校验移动到真实边界。
- no-doc 非轻量任务也必须在临时约束清单或最终回复中列出新增候选和保留理由。
- 不能用“保险”“避免 panic”“更稳”替代调用链证据。

### 存量清理流程

用户要求清理重复防御代码、收敛重复校验或简化调用链时：

1. 先界定范围：单个入口、调用链、package/module 或明确文件集。
2. 扫描候选：按当前项目语言、框架和项目契约查找 `string-normalization`、`empty-check`、`dependency-guard`、`default-fallback`、`error-wrapping`、`logging`。
3. 分级处理：
   - `keep-boundary`：外部边界、public/exported API、反序列化、旧数据兼容、安全边界，保留。
   - `remove-redundant`：上游或项目契约已保证，当前判断无独立价值，删除。
   - `move-to-boundary`：校验需要存在但位置错误，移动到入口或真实边界。
   - `needs-evidence`：调用链或契约证据不足，不动。
4. 每次只清理有证据的一小组候选，不做全仓无脑删除。
5. 删除前后用完整调用链测试、编译/typecheck、现有回归测试或明确代码审查证据证明行为未变或符合预期变化。

当安全性依赖上游校验时，应在 plan、代码注释或最终说明中记录校验来源：

- 哪个顶层入口校验了输入。
- 哪些值在那里完成了标准化。
- 哪些路径无法到达当前函数。
- 哪些 public/exported API 被视为边界。
- 哪些依赖由构造函数、依赖注入、模块系统、框架生命周期、generated code 或 fixture 保证存在。

## 中间类型

不要为了在一条局部链路上传几个值就创建临时类型、DTO、interface、class 或 struct。

优先使用：

- 一个内聚函数内的局部变量。
- 已有对象、receiver、class 字段或上下文对象。
- 已有 request/context/state 对象。
- 值较少时的直接函数参数。

只有跨越真实边界时才定义新类型：

- 模块、package、service 或组件边界。
- 异步、线程、goroutine、worker 或消息边界。
- 序列化或反序列化。
- 稳定 API、interface、protocol 或 schema。
- 复杂状态通过命名结构能明显提升可读性。

## 项目风格

参考附近代码：

- handler/controller/service/repository/job/component 命名。
- interface、class、function、hook、module 的组织方式。
- error/exception/result 返回方式。
- 日志字段和日志层级。
- API/schema/proto/type 定义模式。
- 测试命名、fixture 和 mock 风格。
- transaction、query、cache 和 client 调用方式。

除非当前任务确实需要，不引入新的抽象、目录结构、命名体系、状态管理方式或框架模式。

## 错误处理

- 遵循已有 error type、exception、error code、wrapping、result 和返回值约定。
- 不吞错。
- 不写空 catch，不忽略返回的 error，不把异常只记日志后当作成功继续执行。
- 不把重要错误替换成缺少上下文的默认值。
- 不用无证据 fallback、重试、降级或缓存值掩盖未知问题；保留此类路径必须说明业务契约、触发条件和可观测信号。
- 在能帮助调用方诊断时补充上下文。
- 用户可见错误和内部错误应符合项目已有实践。
- 内部错误到边界层响应的映射应放在边界层，不要散落在共享 helper 深处。
- 避免每一层都重复记录同一个错误；优先在边界层或上下文最丰富的位置记录一次有意义的日志。
- 异步错误必须被正确 await/catch/return，不留下未处理 promise、future、task 或 goroutine 错误。

## 日志

- 只记录排查问题所需的业务上下文，优先覆盖入口、关键状态变化、外部依赖调用结果、异常分支和不可自动恢复的失败。
- 关键路径日志应能串起一次请求或任务，例如 request/correlation id、tenant/user/resource id、job/message id、操作阶段、状态前后值或外部依赖摘要；具体字段沿用项目风格。
- 不记录 secret、token、密码、完整隐私数据或大体量 payload。
- 移除临时 debug log、print、console.log 和断点残留。
- 不用噪音日志掩盖不清晰的控制流。
- 如果当前日志不足以证明根因或验证修复，先补 targeted observability 或向用户说明信息缺口，不假装修复已经成立。

## 数据库和 migration

schema 或 migration 变更必须显式考虑：

- 旧数据兼容。
- 发布过程中的前向/后向兼容。
- 是否需要回填。
- 回滚风险。
- 幂等性和重试行为。
- 数据影响范围。
- 多次部署场景下的 expand/contract 顺序。
- 新字段的 `NULL` / default 策略。
- 在线 DDL 或锁表风险。
- 索引创建策略，包括数据库支持时的并发或分批创建。
- 旧代码/新代码读写兼容。
- 回滚是反向 migration 还是 forward fix。
- 回填批大小、可恢复性和失败处理。

repository/DAO 代码应遵循项目已有模式：

- query 构造。
- transaction。
- lock。
- pagination。
- soft delete。
- 错误处理。

如果项目已有 repository/DAO 边界，不要在业务逻辑或 UI 层散落 SQL。

## 资源、异步和并发处理

- I/O、数据库、RPC 和长耗时操作应按项目风格传递取消信号、deadline 或 request context。
- 当前层已经接收 context、signal、request scope 或 lifecycle 时，应尊重取消和超时。
- rows、response body、文件、stream、subscription、timer 和其他 closer/disposable 必须在所有路径释放。
- error 路径需要 rollback transaction，除非项目 helper 已经处理。
- 不启动没有生命周期、取消路径和错误处理策略的 goroutine、thread、worker、task 或 subscription。
- 不用 sleep 做同步；优先使用语言或项目已有的同步、事件和测试 helper。

## 依赖变更

- 不为小便利功能新增依赖。
- 不随意升级版本。
- 说明为什么需要该依赖，以及为什么现有方案不足。
- 依赖变更后运行相关验证。
- 同步 package manager 对应的 lockfile。
- 避免没有解释的 replace、override、resolution、exclude 或本地路径依赖。
- 新增库时考虑 license、传递依赖、包体积和运行时影响。
- 如果依赖影响 generator、schema、API 或类型定义，同步生成并验证生成代码。

## 语言特化规则

### Go

- 使用 `context.Context` 传递取消、deadline 和 request scope。
- 遵循项目已有 `gofmt`、`go test`、`go vet`、`golangci-lint` 和生成代码流程。
- 依赖变更后判断是否需要 `go mod tidy`。
- 检查 major version import path 变化。
- 不启动没有生命周期和错误处理策略的 goroutine。
- 除非已经完整追溯所有调用方，否则 exported package 函数应视为边界。

### TypeScript / JavaScript

- 遵循项目已有类型严格程度；不要随意使用 `any`、类型断言或忽略类型错误。
- 异步逻辑必须正确 `await`、return 或 catch。
- 前端状态、数据请求、路由、表单和组件拆分沿用项目现有模式。
- 依赖变更使用项目已有包管理器，并同步对应 lockfile。
- 不把类型修复伪装成运行时逻辑修复。

### Python

- 遵循项目已有类型标注、dataclass/pydantic/schema 和异常处理风格。
- 使用 context manager 管理文件、连接、锁和临时资源。
- 不为局部传值滥用 dict/dataclass；跨边界时再定义稳定结构。
- 依赖变更同步项目使用的 `requirements`、`pyproject`、lockfile 或环境配置。

### Java / Kotlin / JVM

- 遵循项目已有 service、repository、DTO、exception、transaction 和 DI 风格。
- 不绕过已有 validation、transaction、security 或 mapper 边界。
- 依赖变更同步 Gradle/Maven 配置和 lock/version catalog。

## 交叉审查风险门禁

编码后，交付前先判断风险：

- 中高风险：跨模块修改、API/schema/proto 变更、DB/migration、权限/安全、并发/异步、错误链路变化、核心业务流程、依赖版本变更、public/shared helper 变更、测试失败后的逻辑修复。
- 低风险：纯文档、注释、格式、简单文案、局部命名、无行为变化的整理。

中高风险代码必须进行更严格的 review。这个 skill 只定义工程 review 标准，review 如何执行属于运行时或流程决策，不由本 skill 定义。

最小 review checklist：

- 实现仍符合已确认的 design/plan。
- 关键约束覆盖矩阵中的每个 ID 都有实现落点或明确的不适用理由。
- 已考虑完整调用链。
- 校验位于正确边界，且没有不必要的重复校验。
- 新增防御式代码候选已有边界证据；存量清理候选已有 keep/remove/move/needs-evidence 分类。
- 没有新增 silent fallback、吞错、无证据重试或降级；确需保留时已有业务契约和可观测信号。
- public/exported/shared 函数对所有调用方仍然安全。
- 错误、日志、返回值符合项目风格。
- 关键路径具备足够 traceability；根因不明的问题没有被表面修复掩盖。
- 数据库和 migration 兼容性风险已处理。
- 依赖变更有理由且已验证。
- 资源清理和并发/异步生命周期安全。
- 测试覆盖目标行为路径，或已记录跳过测试的理由。
- 已记录 lint/test/build 验证结果。
