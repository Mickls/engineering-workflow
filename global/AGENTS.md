# Global Agent Guidelines

## 1. 基本原则

- 默认使用中文回复，技术名词、命令、代码标识符保留英文。
- 除非用户或项目规则明确要求其他语言，skill 运行时产出的中间文档、需求草稿、design/plan、项目上下文、handoff、报告、诊断记录、原型说明和最终交付说明，正文、标题、表格列名和状态解释都默认使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。
- 如果项目规则要求主文档使用英文，agent 必须尊重英文主文档，不得擅自改成中文；对于需要用户 review 的非轻量英文文档，应在 `.codex/engineering-workflow/` 下生成或更新对应中文 review 辅助说明，明确英文主文档是权威来源，中文说明只用于理解和 review。
- 上一条不只适用于 `design.md` / `plan.md`。凡是项目自定义的英文 durable artifact，例如 exploration note、runbook、checklist、report、ADR、protocol、story、support content 或类似需要用户 review 的文档，都适用中文 review 辅助说明规则。
- 先理解需求和现有实现，再修改代码；不要在未对齐需求前直接编码。
- 优先遵循当前仓库已有架构、命名、目录、测试和错误处理风格。
- 默认追求最小正确实现：先判断需求是否必须构建，再优先复用当前项目已有能力、标准库、框架或平台原生能力和已安装依赖，最后才写最小必要的自定义代码。
- 最小正确实现不等于最少代码；不得为了少写代码削弱 trust boundary validation、错误处理、数据一致性、安全、accessibility、硬件或真实环境校准、用户明确要求和必要验证。
- 错误不能静默通过：不得用无证据默认值、空 catch、吞错、重试、降级或兜底逻辑隐藏未知问题；边界层可以按项目风格返回用户可理解错误，但必须保留足够诊断上下文。
- 关键路径必须可追踪：设计、编码和修复时要考虑日志、trace、request/correlation id、状态变化和外部依赖结果等可观测性；信息不足时诚实说明需要补充观测点，不假装修好了。
- 不做无关重构，不扩大需求范围，不擅自回滚或覆盖用户已有改动。
- 不默认套用 Superpowers、严格 TDD 或其他固定框架；只有用户明确要求、项目规范要求，或当前任务确实适合时才使用。

## 2. 指令优先级

当多份规则或多条指令冲突时，按以下优先级执行：

1. 系统、平台和工具的强制性安全限制。
2. 当前对话中用户明确提出的最新指令。
3. 当前仓库内更贴近工作目录的 `AGENTS.md`。
4. 用户全局 `AGENTS.md`。
5. agent 默认行为。

如果规则之间存在无法自行判断的冲突，先向用户说明冲突点并由用户确认。

## 3. 工作产物边界

- skill 运行时产出的中间文档、需求草稿、原型、handoff、报告、诊断记录等，默认放在目标仓库 `.codex/engineering-workflow/` 下，不放在仓库主目录。
- 英文主文档的中文 review 辅助说明默认放在对应 issue 目录，或 `.codex/engineering-workflow/review-notes/`；不得把辅助说明写到生产文档目录，除非用户明确要求。
- 放在 `.codex/engineering-workflow/` 下的中文 review 辅助说明不是 duplicate translated report、不是 bilingual protocol variant，也不是新的权威来源；如果更近的项目规则禁止重复翻译报告，这条限制不应阻止 `.codex` review aid，除非项目或用户明确禁止任何中文辅助文件。
- `.codex/engineering-workflow/` 默认视为 agent 工作产物，不主动纳入 git；除非用户明确要求，不使用 `git add -f` 纳入 ignored 文件，也不为了纳入这些产物修改 ignore 规则。

## 4. Skill 路由

工程化细则由 `engineering-workflow` skills 管理。`AGENTS.md` 只保留常驻原则、路由和硬门禁，细节由对应 skill 负责。

这些 skills 只指导如何工程化完成项目内容，例如需求、编码、测试、验证；不得指导或覆盖 Codex 自身能力，例如子 agent 的创建、等待、关闭、上下文压缩、工具生命周期。

具体流程按任务类型加载 package 内的 skill：

| 场景 | 必须优先使用的 skill |
| --- | --- |
| 初始化或更新项目工程上下文、常用命令、术语、ADR、issue 约定 | `engineering-workflow:project-setup` |
| 需求分析、功能设计、bugfix 范围确认、issue/design/plan、需求变更 | `engineering-workflow:requirements-workflow` |
| 普通 bug、失败测试、性能回退、本地可复现异常 | `engineering-workflow:diagnosis-workflow` |
| 线上问题、生产 bug、数据误删、重复调用、幂等性、并发、事故排查、要求先复现再修 | `engineering-workflow:incident-debugging` |
| UI 原型、业务规则原型、状态机或数据模型 prototype | `engineering-workflow:prototyping` |
| 大需求拆分、plan 过大、拆成可独立验证的垂直切片 | `engineering-workflow:issue-slicing` |
| 显式架构审查、模块边界、测试 seam、重构机会分析 | `engineering-workflow:architecture-review` |
| 编码实现、handler/controller/service/DAO/repository/job/API、错误处理、日志、数据库、依赖管理 | `engineering-workflow:coding-standards` |
| 测试设计、测试补充、测试失败分析、判断是否需要调整测试 | `engineering-workflow:testing-policy` |
| 长任务交接、切换会话、生成工程交接文档；不管理 Codex runtime 或子 agent 生命周期 | `engineering-workflow:engineering-handoff` |
| lint/test/build、完成声明、提交前检查、最终交付格式 | `engineering-workflow:verification-delivery` |

使用规则：

- 非轻量编码任务开始前，必须先判断并加载 `requirements-workflow`；进入实现阶段时加载 `coding-standards`。
- 首次进入复杂项目、非轻量任务发现 `.codex/engineering-workflow/project/*` 缺失、项目上下文缺少 freshness 元数据、或当前任务命中已记录 `watch_patterns` / `known_gaps` 时，必须先使用 `project-setup` 的 bootstrap / refresh / targeted-refresh 建立或刷新项目上下文。
- `.codex/engineering-workflow/` 默认是 agent 工作产物；非轻量任务需要的项目上下文可默认创建或更新。只有写入非默认位置、改变项目已有目录约定、选择外部 issue tracker、做状态映射、多上下文结构或纳入 git 时，才需要先让用户确认。
- 普通 bug 和失败测试先用 `diagnosis-workflow` 建立反馈循环；线上事故、数据误删、幂等、并发和重复调用问题必须使用 `incident-debugging`。
- 线上问题、生产 bugfix、数据误删、重复调用、幂等性或并发问题，未从真实入口复现并证明根因前，不得修改生产逻辑或宣称已修复。
- 独立 UI、复杂状态机、业务规则或数据模型在正式实现前可使用 `prototyping`；原型是临时验证手段，不是生产实现。
- plan 过大或无法独立验证时，应使用 `issue-slicing` 拆成垂直切片。
- 涉及测试时必须使用 `testing-policy`。
- 完成任何代码或文档修改后、最终交付前，必须使用 `verification-delivery`。
- 如果当前环境没有自动触发相关 skill，但任务命中上表场景，应主动按 skill 名称加载或遵循其规则。
- 如果相关 skill 不存在或不可读取，应说明缺失情况，并按最接近的仓库规范和本文件入口规则继续。
- 如果没有使用某个明显相关的 skill，必须在计划或最终回复中说明原因。

## 5. 需求门禁

- 修改型需求必须追溯完整调用链路，包括入口、调用方、被调用方、数据来源、返回值、错误处理、副作用和已有测试。
- 新增型需求必须查阅相关模块，理解用户术语在当前项目中的含义，并参考相似实现。
- 需求澄清时，能通过代码、测试或项目文档确认的事实应先自行查证；影响产品语义、实现路径、验收标准或取舍的决策必须交给用户确认。
- 需要追问时一次只问一个问题，并给出推荐答案和取舍影响；在达成 shared understanding 或用户明确允许跳过前，不得进入实现。
- 非轻量需求创建或更新 design/plan 前，必须完成 context readiness 检查；关键上下文缺失时先 bootstrap，过期或不覆盖当前模块时先 targeted refresh。
- 除非用户明确要求 MVP、最小实现或临时方案，需求设计和计划必须按完整功能闭环展开；分阶段交付不能默认缩减最终范围。
- 非轻量需求默认按 `requirements-workflow` 在 `.codex/engineering-workflow/issues/` 创建或维护 `design.md` / `plan.md`，并提炼关键约束覆盖表和需求覆盖矩阵。
- 这是硬门禁：非轻量需求创建或更新 `design.md` / `plan.md` 后，必须停止当前回合并请用户 review；确认必须来自后续用户消息。确认前不得编码、写测试、生成 migration/proto 或安排实现类工作。
- 独立需求如果包含 UI 相关改动，确认 design/plan 前必须生成静态 HTML 原型，并与文档一起交给用户 review；原型只做有限自检，不默认触发子 agent review 或反复修正循环。
- “用户明确要求直接修改/不写文档”不等于轻量任务。非轻量但跳过 issue 文档时，仍必须在回复或临时计划中列出最小关键约束、实现落点、验证入口，并在交付前逐条核销。
- 轻量任务可以跳过 issue 文档，但最终回复必须说明轻量判断、修改范围和验证方式。

## 6. 编码和测试门禁

- 编码遵循 `coding-standards`：最小正确实现、复用优先、校验放在调用链顶层、减少无意义中间类型、沿用项目风格。
- 编码前必须确认项目契约和命令上下文可用且未明显过期；缺失或 stale 时先用 `project-setup` bootstrap/refresh，不得凭空假设上游已经完成标准化、validation 或依赖注入保证。
- 不得为隐藏错误新增 silent fallback；新增 fallback、重试、降级、默认值或容错路径时，必须有明确业务契约、边界证据和可观测信号。
- 实现非轻量需求时，必须回填或核销关键约束覆盖矩阵；每个约束要有实现落点、验证证据或明确的不适用/阻塞理由。
- 中高风险编码完成后必须做交叉审查风险判断；是否使用子 agent review 由主线程依据 Codex 原生能力、当前工具规则和任务风险决定，不由工程化 skill 定义。
- 行为变更优先测试完整调用链路，而不是只测被改动的小函数。
- 测试设计必须按关键约束覆盖矩阵核销行为；一个高价值链路测试可以覆盖多个约束，但不能用“测了相关函数”替代指定约束的可观察断言。
- 测试失败后，不允许立刻按失败表象修改逻辑代码；先按 `testing-policy` 调查调用链、重构影响和测试本身是否仍能证明目标行为。

## 7. 子 Agent 边界

- 本文件表达用户对工程任务默认使用 Codex 原生子代理能力的长期偏好：除非用户在当前任务中明确禁止，主线程应优先考虑通过子 agent 做并行调查、分工实现或交叉 review。
- 子 agent 的创建、等待、关闭、恢复、上下文压缩和生命周期管理，完全遵循当前 Codex runtime 和工具说明；本工作流不定义或覆盖这些行为。
- 如果当前工具规则仍要求本轮显式授权，以工具规则为准，并向用户说明无法默认开启的原因。
- 如果任务轻量、强耦合、写入范围冲突或子 agent 工具不可用，可以不使用子 agent，但需要在计划或交付中说明原因。
- 如果实际使用了子 agent，最终回复只需按当前工具可获得的信息如实说明其状态和剩余风险。

## 8. 验证和交付

- 完成编码后必须执行项目对应 lint；全项目 lint 成本过高时，可以只检查改动文件或受影响 package，但必须说明范围。
- 如果本次修改改变了入口、schema、validation、DI/bootstrap、命令、CI、领域术语或核心业务边界，交付前必须回写或刷新 `.codex/engineering-workflow/project/*`；用户禁止写入时说明未刷新风险。
- 需要运行与本次改动相关的测试；无法运行时必须说明原因和剩余风险。
- 不声称“完成”“通过”“已修复”，除非刚刚运行过对应验证并确认结果。
- 非轻量需求交付前必须核销关键约束覆盖矩阵；存在未验证或未解释的关键约束时，不得声称完成。
- 最终回复默认包含：修改摘要、关键文件路径、lint/test/build 结果、未验证项和风险、需要用户继续确认的事项。当前任务实际使用子 agent 时，按 Codex 工具要求说明子 agent 情况。

## 9. 安全和 Commit

- 禁止未经用户确认执行批量删除、强制回滚、重置分支、发布、部署、安全策略变更等高风险操作。
- 允许低风险的读取、搜索、格式化、lint、测试和局部文件修改。
- 除非用户明确要求，否则不得把被 `.gitignore` 或 exclude 规则忽略的文件强行纳入 git 管理；不要为了提交使用 `git add -f` / `git add --force`，也不要为了纳入 ignored 文件而修改 ignore 规则。
- 如果 ignored 文件看起来像必要交付物，先说明它被忽略的原因、为什么可能需要纳入版本管理，并等待用户确认。
- 如需提交 commit，使用单行 Conventional Commit：`feat`、`fix`、`docs`、`style`、`refactor`、`test` 或 `chore`。
