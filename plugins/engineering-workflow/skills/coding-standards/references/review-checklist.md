# 交叉审查风险门禁

编码后，交付前先判断风险。

中高风险：

- 跨模块修改。
- API/schema/proto 变更。
- DB/migration。
- 权限/安全。
- 并发/异步。
- 错误链路变化。
- 核心业务流程。
- 依赖版本变更。
- public/shared helper 变更。
- 测试失败后的逻辑修复。

低风险：

- 纯文档。
- 注释。
- 格式。
- 简单文案。
- 局部命名。
- 无行为变化的整理。

中高风险代码必须进行更严格的 review。最小 checklist：

- 实现仍符合已确认的 design/plan。
- 关键约束覆盖矩阵中的每个 ID 都有实现落点或明确的不适用理由。
- 已考虑完整调用链。
- 已核销项目实现路径契约：统一实例化、DI/provider、generated code、schema/migration、事务边界、异步/手动生成流程没有被绕过。
- 如果正确路径需要用户手工生成、迁移或部署，diff 停在 source/schema/provider 侧并明确 blocked/manual step，没有手改 generated output 来伪造完成。
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
