# 动态设计树遗漏检查

本文件不是固定访谈模板。以下维度只供 AI 在提交澄清核销总结前静默检查；先从真实入口和调用链展开，只有发现实际缺口时才查证或逐题询问。

- 当前行为、目标行为和必须保留的行为是否有证据。
- breadth discovery 是否覆盖当前真实入口、跨模块 owner、主要失败路径、standing constraints 和第一层条件分支，并达到 `discovery-complete`。
- 每个候选问题是否已分类为 current / introduced / conditional / speculative，并证明从真实场景可达。
- 每个问题是否已有推荐、依赖影响和候选答案后的下一步，达到 `prepared` 后才进入 interview。
- 是否按 `semantic_key` 检查了父需求决定、standing constraints 和同义问题；没有 `exception evidence` 时是否仍在重复询问。
- 用户纠正结论后是否先审计了所有 dependents，而不是只修改当前问题。
- 是否把项目已有模式能决定的内部实现细节错误地转交用户。
- 当前是否只有一个 active question；解释、理解、确认、授权和暂缓状态是否分离。
- 用户是否能只读普通语言场景和可见后果做决定，而无需先读代码或理解专业术语。
- 真实用户、入口、调用方、被调用方、数据来源、返回值和副作用是否覆盖。
- existing / non-existing、empty / invalid、手动 / 自动、同步 / 异步等真实分支是否遗漏。
- 失败、超时、重试、并发、幂等、补偿和恢复是否会改变设计。
- 数据、旧配置、旧 API、迁移、回填和兼容读取是否受影响。
- 权限、租户、资源归属和 trust boundary 是否受影响。
- 跨服务 owner、外部依赖、部署和人工流程是否已确认。
- 可观测性、发布、回滚、验收和测试入口是否完整。
- 是否新增了未经解释的术语、表、状态、API、依赖或抽象。
- 是否把 speculative edge 误当成 required，或把 certain defect 降为风险说明。
- 是否仍有决定藏在假设、TODO、后置项或“实现时决定”中。
- interaction budget 是否合理；超预算是否说明 discovery 不足、问题可合并或应切换 delegated/recommended-default。
- interview 中是否因普通回答重新做广泛搜索、全量 refresh 或阻塞式状态回填。
- 用户表示疲劳、暂停或含糊继续时，是否错误推断了批准。

确实不适用的维度无需写入 `clarification.md` 或向用户逐项报告。完成检查后，只在核销总结中陈述实际覆盖范围和剩余未知。
