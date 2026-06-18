---
name: verification-delivery
description: "用于声明任务完成前、代码或文档修改后、提交前，以及汇报 lint/test/build 结果、跳过检查、剩余风险和最终交付内容。"
---

# 验证和交付

## 概述

不能没有证据就说完成。最终回复必须把做了什么、怎么验证、什么没验证、还有什么风险讲清楚。

## 完成声明门禁

在说出或暗示“完成”、“已修复”、“通过”、“没有问题”之前：

1. 确认哪个命令或检查能证明这个结论。
2. 重新运行相关命令。
3. 阅读输出和退出状态。
4. 汇报真实结果。
5. 如果没有运行验证，说明原因。

不要依赖：

- 之前运行过的结果。
- 自己推测“应该正确”。
- 未经本地验证的外部成功报告。
- 部分命令输出。
- “应该会通过”的推理。

## 需求覆盖核销

非轻量需求如果存在 `.codex/engineering-workflow/issues/` 下的 issue/design/plan，声明完成前必须核销关键约束覆盖矩阵。非轻量 no-doc 例外必须核销临时计划或回复中的最小关键约束清单。

核销规则：

- 回读 `design.md` 的关键约束覆盖表和 `plan.md` 的需求覆盖矩阵。
- 每个关键约束 ID 必须有实际实现落点，或明确 `not-applicable` / `blocked` 证据。
- 每个关键约束 ID 必须有测试、手动验证、代码审查证据，或明确不可验证原因和风险。
- 对数据删除、权限、安全、幂等、并发、兼容性、手动/自动语义分歧等高风险约束，缺少验证证据时不得说“完成”或“已修复”。
- 最终回复需要摘要说明覆盖情况；不必粘贴完整大表，但必须列出未覆盖、手动验证和高风险项。
- 如果实现过程中发现 design/plan 漏了关键约束，先更新文档并说明，不得把新行为藏在代码里。
- 如果用户要求跳过文档，最终回复仍需列出最小关键约束的实现落点、验证证据或未验证风险。

## 项目上下文交付门禁

声明完成前必须检查项目上下文状态：

- 是否读取了 `.codex/engineering-workflow/project/project-profile.md`、`commands.md`、`contracts.md`、`issue-workflow.md`、`context.md` 或 `context-map.md`。
- 这些上下文是否包含 freshness 元数据，且 `scan_scope` 覆盖当前任务。
- 本次 diff 是否触及 route/controller/handler/resolver、CLI/job、schema/OpenAPI/proto/GraphQL、middleware、validation、DI/bootstrap、module provider、generated code、package/build/test/CI 配置、领域术语或核心业务边界。

如果上下文缺失或 stale，且任务不是轻量只读，应在交付前使用 `project-setup bootstrap`、`refresh` 或 `targeted-refresh`。如果本次 diff 改变了项目契约来源，必须回写对应 project 文档并刷新 metadata。

最终回复需要说明：

- context readiness / freshness 检查结果。
- 创建、刷新或跳过的 `.codex/engineering-workflow/project/*` 文件。
- 如果用户禁止写入或无法判断 freshness，说明未回写项和剩余风险。

## 防御式代码审查

如果本次改动涉及生产代码、测试代码或脚本，应在交付前检查 diff 是否新增或清理了防御式代码候选：

- `string-normalization`：trim、strip、normalize、大小写转换、空白折叠、类型 coercion。
- `empty-check`：nil、null、undefined、None、Optional empty、空字符串、空集合、空对象。
- `dependency-guard`：对已由构造函数、依赖注入、模块系统、框架生命周期、generated code 或 fixture 保证存在的依赖重复判空。
- `default-fallback`：无证据默认值兜底。
- `error-wrapping` / `logging`：重复错误包装、重复日志或重复错误映射。

交付要求：

- 新增候选必须说明边界证据，或说明已删除/移动到真实边界。
- 清理存量候选必须说明删除、保留、移动和未动的分类结果。
- 如果项目存在 `.codex/engineering-workflow/project/contracts.md`，必须说明是否读取，以及哪些契约影响了本次判断。
- 未完成防御式代码审查时，不得声称代码改动已完成。

## lint

编码后运行项目对应的 lint。

如果全项目 lint 成本过高，可以只检查改动文件或受影响 package，但必须明确说明检查范围。

如果不知道 lint 命令：

- 检查项目 scripts、Makefile、CI 配置、package scripts 或 Go 工具链。
- 仍找不到时，说明未找到 lint 命令。

## 测试

运行与本次改动相关的测试：

- 受影响 package 测试。
- 覆盖调用链的 feature 或 integration 测试。
- bugfix 的回归测试。
- 触及共享行为时的更大范围测试。

如果不知道测试命令：

- 检查项目 scripts、Makefile、CI 配置、README、package scripts 和语言工具链。
- Go 项目中判断应运行 package 级 `go test ./...`，还是更窄范围的 `go test ./path`。
- 仍找不到时，说明未找到测试命令，并列出检查过的位置。

如果测试失败，先使用 `testing-policy` 判断应修改测试还是生产代码。

## build / typecheck / compile

以下情况需要运行 build、typecheck 或 compile 检查：

- interface 发生变化。
- 生成代码发生变化。
- 依赖发生变化。
- build tags 或配置发生变化。
- 测试没有充分编译受影响范围。

如果不知道 build 或 typecheck 命令：

- 检查项目 scripts、Makefile、CI 配置、README、package scripts 和语言工具链。
- Go 项目中判断 `go test` 是否已经编译受影响 package，或是否还需要 `go build ./...`。
- 仍找不到时，说明未找到 build 命令，并列出检查过的位置。

如果任何验证失败或被跳过，不要声称任务已修复或通过。应汇报真实状态、失败命令、跳过命令、原因和风险。

纯文档变更可接受的验证包括：回读检查、可用时的 markdown lint、链接/路径检查，或明确说明代码 lint/test/build 不适用。

## bugfix / 线上问题完成声明

bugfix、线上问题、数据误删、重复调用、幂等性或并发问题在声明“已修复”前，必须汇报：

- 修复前复现入口和复现命令。
- 修复前失败证据，包括用户可见结果、错误、数据状态或副作用。
- 已证明的根因和关键代码位置。
- 修复后同一入口、同一触发条件或等价顶层流程的验证命令。
- 修复后通过证据。
- 未能覆盖的环境、数据、并发窗口或剩余风险。

如果没有修复前复现证据、根因证据或修复后同路径验证，只能说“已调查到当前状态”或“已做尝试”，不得说“已修复”“已解决”。

## review 汇报

如果进行了 review，汇报：

- review 范围。
- 关键发现。
- 采纳或拒绝了什么。
- 后续修改。

本 skill 只定义应汇报哪些验证和交付信息，不定义运行时工具行为。

## 最终回复格式

默认最终回复包含：

- 修改内容摘要。
- 关键文件路径。
- context readiness / freshness 检查和项目上下文回写结果。
- 已执行的 lint/test/build 命令及结果。
- 未执行的验证项、原因和风险。
- 需要用户继续确认或处理的事项。

小任务可以更简短，但仍需包含验证事实。

## Commit 信息

提交前必须检查暂存范围：

- 只暂存本次任务需要纳入版本管理的文件。
- 默认尊重 `.gitignore`、`.git/info/exclude` 和全局 ignore 规则。
- 除非用户明确要求，否则不得使用 `git add -f` / `git add --force` 将 ignored 文件强行纳入 git 管理。
- 不得为了提交 ignored 文件而修改 `.gitignore` 或 exclude 规则，除非这正是用户确认的任务内容。
- 如果不确定某个文件是否被忽略，使用 `git check-ignore -v <path>` 或 `git status --ignored` 确认。
- 如果 ignored 文件看起来像必要交付物，先向用户说明文件路径、忽略来源和纳入版本管理的理由，得到确认后再处理。
- 运行期文件、缓存、构建产物、日志、会话登记表、`.codex/engineering-workflow/` 中间产物、临时原型输出等如果已被 ignore，默认不提交，只在最终回复中说明其位置和用途。

需要提交 commit 时，使用单行 Conventional Commit：

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `test`
- `chore`

除非用户或仓库要求，否则不需要 commit body。
