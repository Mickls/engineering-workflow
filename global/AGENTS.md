# Global Agent Guidelines

## 1. 基本原则

- 默认使用中文回复，技术名词、命令、代码标识符保留英文。
- skill 产出的文档和最终交付默认使用中文；项目要求英文主文档时保持英文权威，并在 `.codex/engineering-workflow/` 提供需要 review 的中文辅助说明。
- 先理解需求、调用链和现有实现，再修改代码；优先遵循项目架构、命名、目录、测试和错误处理风格。
- 追求最小正确实现：先判断是否必须构建，再复用项目能力、标准库、框架/native feature 和已安装依赖；不得弱化 trust boundary validation、安全、数据一致性、accessibility 或必要验证。
- 错误不能静默通过；fallback、重试、降级或默认值必须有业务契约、边界证据和可观测信号。
- 关键路径应可追踪；观测不足时补 targeted 日志、trace、metric 或明确说明缺口。
- 不做无关重构，不扩大范围，不覆盖用户已有改动。
- 不默认套用 Superpowers、严格 TDD 或其他固定框架，除非用户、项目规则或任务需要。

## 2. 指令优先级

冲突时按以下顺序执行：

1. 系统、平台和工具的强制限制。
2. 当前对话中用户最新明确指令。
3. 当前仓库内更近的 `AGENTS.md`。
4. 用户全局 `AGENTS.md`。
5. agent 默认行为。

无法判断的冲突应说明并请求用户确认。

## 3. 工作产物边界

- 中间文档、需求、原型、handoff、报告和诊断记录默认写入目标仓库 `.codex/engineering-workflow/`。
- 英文主文档的中文 review aid 默认放在对应 issue 或 `review-notes/`，只用于理解和 review，不是新的权威来源。
- `.codex/engineering-workflow/` 默认是 ignored 的 agent 工作产物，不主动纳入 git，不使用 `git add -f`，也不为纳入它修改 ignore 规则。

## 4. Skill 路由

工程化细则由 `engineering-workflow` skills 管理；global AGENTS 只保留常驻原则、路由和 fail-safe，不管理 Codex runtime 或子 agent 生命周期。

| 场景 | 优先使用的 skill |
| --- | --- |
| 项目上下文初始化或刷新 | `engineering-workflow:project-setup` |
| 需求、bugfix 范围、design/plan、需求变更 | `engineering-workflow:requirements-workflow` |
| 普通 bug、失败测试、性能回退 | `engineering-workflow:diagnosis-workflow` |
| 生产事故、数据误删、幂等、并发、重复调用 | `engineering-workflow:incident-debugging` |
| UI、状态机、业务规则或数据模型原型 | `engineering-workflow:prototyping` |
| 大需求和 plan 垂直拆分 | `engineering-workflow:issue-slicing` |
| 架构、模块边界、测试 seam 和重构机会审查 | `engineering-workflow:architecture-review` |
| 编码实现、错误处理、数据库和依赖管理 | `engineering-workflow:coding-standards` |
| 测试设计、测试失败和新增/跳过判断 | `engineering-workflow:testing-policy` |
| 长任务工程交接 | `engineering-workflow:engineering-handoff` |
| lint/test/build、完成声明和最终交付 | `engineering-workflow:verification-delivery` |

- 非轻量编码先使用 `requirements-workflow`；进入实现时使用 `coding-standards`。
- 项目上下文缺失、stale、超出 `scan_scope` 或命中 `watch_patterns` / `known_gaps` 时，先使用 `project-setup`。
- 普通问题使用 `diagnosis-workflow`；生产事故和高风险数据/并发问题使用 `incident-debugging`。
- 涉及测试时使用 `testing-policy`；完成任何代码或文档修改后使用 `verification-delivery`。
- plan 过大时使用 `issue-slicing`；原型只用于回答明确问题，不直接进入生产实现。
- skill 缺失或不可读时说明原因，并按最近的仓库规则继续。

## 5. 跨流程 Fail-Safe

- 非轻量需求先完成 breadth discovery、standing constraints 和 decision ledger，新问题先去重，达到 `discovery-complete` 后才进入逐题 interview；普通回答不触发广泛重搜，用户纠错先审计全部依赖。用户疲劳时停止低价值提问，并只在已授权范围内切换推荐代理；新的行为、不可逆风险和长期边界仍交给用户。
- design/plan 只能写已查证事实和已确认决定。用户明确授权“按总结设计并实现”时，文档自检后可直接实施；否则 design/plan 创建后等待确认。已批准范围内的“继续”授权 AFK 连续执行，不代表批准新决定。
- 行为切片编码前确定真实入口、用户可见结果和关键副作用的验收场景；AFK 是批准后默认模式。出现新用户决定、行为偏离、证据缺口、手动步骤、未覆盖风险或 budget 命中时升级 HITL；临时逐单元 review 必须有截止和恢复条件。
- 生产事故未从真实或等价顶层入口复现并证明根因前，不修改生产逻辑，也不宣称已修复。
- 编码和交付不得绕过统一实例化、DI/provider、generated code、schema/migration、事务或异步/手动生成流程；正确路径需要人工动作时报告 `blocked` / `manual-only`。
- validation 放在真实外部边界；不吞错，不用无证据 fallback、retry 或 degrade 掩盖未知问题。
- 行为变更优先从用户入口或稳定 public contract 验证，不能用内部 helper 测试替代完整 workflow。
- 只有刚运行并读过输出和退出状态的检查才能支持“完成”“通过”或“已修复”；未验证项必须明确说明。
- HITL 和最终交付先用普通语言汇报行为、目标关系、方案偏离、验收证据和剩余风险，最多列三个需要用户处理或判断的 review 项；技术细节随后提供。
- 上下文压缩后优先复用带 `source_commit` 的 decision/evidence ledger；scope 和失效条件未变化时不全量重搜。测试、构建和手工生成按自然里程碑集中，遵守缓存和资源预算。
- 当前批准的验收场景通过后立即交付并关闭需求；非阻塞新发现建立 follow-up，不持续扩大原完成定义。
- diff 改变入口、schema、validation、DI/bootstrap、命令、CI、领域术语或核心边界时，交付前刷新对应项目上下文。

## 6. 子 Agent 边界

- 非轻量工程任务开始调查或实现前，先识别可独立推进的工作线。跨仓库或跨模块、存在两条以上独立调查/实现线，或预计串行检索会显著膨胀主上下文时，必须主动调用 Codex 原生子 agent 做并行调查、分工或交叉 review，无需用户逐次要求。
- 主 agent 保留需求理解、standing constraints、decision ledger、跨工作线取舍和最终综合；子 agent 使用有边界的任务返回结论与证据，避免在主上下文重复装载大段代码和调查过程，并降低频繁上下文压缩。
- 只有任务轻量、工作线强耦合、存在写入冲突、无法形成有边界的独立任务或工具不可用时可以不使用。必须在计划或交付中说明具体原因；工具未暴露时不得静默退化为长时间串行检索。
- engineering-workflow 不定义子 agent 的创建、等待、关闭或上下文生命周期。

## 7. 验证、安全和 Commit

- 修改后运行与 diff 匹配的 lint/test/build；无法运行时说明原因和风险。
- 禁止未经确认执行批量删除、强制回滚、重置分支、发布、部署或安全策略变更。
- 不回滚或覆盖用户已有改动，不把 unrelated changes 纳入本次 review、暂存或提交。
- 被 ignore 的必要交付物应先解释并等待确认，不使用 `git add -f` 绕过边界。
- 提交前检查暂存范围；commit 使用单行 Conventional Commit：`feat`、`fix`、`docs`、`style`、`refactor`、`test` 或 `chore`。
