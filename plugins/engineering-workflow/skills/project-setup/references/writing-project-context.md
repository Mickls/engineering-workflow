# 项目上下文写作规则

## 通用规则

- 不把项目上下文写成通用教程。
- 不记录 secret、token、密码或隐私数据。
- 每个 project 文档都要记录 freshness 元数据；如果某项无法获取，写 `unknown` 和原因。
- `.codex/engineering-workflow/` 默认是 agent 工作产物，不主动纳入 git；如用户要求共享其中部分文件，先说明纳入原因和 ignore 状态。

## contracts.md

`.codex/engineering-workflow/project/contracts.md` 记录当前项目可遵从的工程契约，不记录没有证据的猜测。

每条“已保证”都必须写证据位置。

如果框架、接口定义或依赖注入已经保证输入完成标准化、非法值被拦截或依赖存在，内部实现原则上不得重复做同类 trim/strip/normalize、空值/空内容判断或依赖存在性判断。

不确定的保证写入 `Still Unsafe Boundaries` 或待确认项，不要写成已生效契约。

## context / ADR / out-of-scope

- `.codex/engineering-workflow/context.md` 只写领域术语，不写实现细节。
- `.codex/engineering-workflow/adr/` 只记录难逆转、反直觉、有真实权衡的决策。
- `.codex/engineering-workflow/project/out-of-scope.md` 记录已明确拒绝或容易反复误提的方案。

## 英文主文档

如果项目要求英文主文档，`.codex/engineering-workflow/project/issue-workflow.md` 应记录：

- 英文主文档规则。
- 会触发 review aid 的 artifact 类型。
- 中文 review 辅助说明路径约定。
- duplicate translated report 规则是否影响 `.codex` review aid。
