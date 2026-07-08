# 防御式代码清理验证

清理重复防御式代码属于行为保持或契约收敛型重构。优先证明外部行为和项目契约，而不是为每个内部 guard 补低价值测试。

清理前先读取并确认 `.codex/engineering-workflow/project/contracts.md` freshness，确认哪些输入标准化、validation 边界或依赖保证已经由项目契约覆盖。契约缺失或过期时，先 targeted refresh，或把相关保证降级为 `needs-evidence`。

## 验证策略

- 删除内部重复标准化、空值/空内容判断或依赖存在性判断时，优先从真实入口验证无效输入仍在边界被拦截，有效输入仍能流转。
- 如果删除的是内部 helper 的重复 guard，不要为这个 helper 单独新增一组只证明实现细节的测试；优先运行覆盖该调用链的现有测试，或补一个能观察用户行为的链路测试。
- 如果 public/exported API 的本地校验要删除，视为行为变化；必须追溯所有调用方，通常应保留，除非 design/plan 明确确认它不再是边界。
- 如果项目缺少链路测试，保守清理：只删除有明确调用链证据和编译/typecheck 能证明的候选；其他标记为 `needs-evidence`。
- 对 `move-to-boundary`，测试应覆盖移动后的边界错误响应或校验结果，而不是旧内部函数的中间返回值。

汇报清理验证时说明：

- 清理范围和候选分类：`keep-boundary`、`remove-redundant`、`move-to-boundary`、`needs-evidence`。
- 哪些项目契约支持删除。
- 哪些测试或命令证明外部行为不变。
- 哪些候选因缺少证据未动。
