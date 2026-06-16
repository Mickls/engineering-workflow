# Engineering Workflow

这是一套可分享的 Codex 工程化工作流配置，包含：

- `AGENTS.md`：维护本仓库时给 agent 读取的 repo-local 说明。
- `global/AGENTS.md`：安装到 `~/.codex/AGENTS.md` 的全局 agent 行为入口和 skill 路由。
- `plugins/engineering-workflow`：Codex plugin，内含项目初始化、需求、普通诊断、线上问题排查、原型、需求拆分、架构审查、通用编码、测试、工程交接、验证交付等 skills。
- `.agents/plugins/marketplace.json`：本目录自带的本地 marketplace。

核心约束包括：项目上下文初始化、领域术语和 ADR 沉淀、需求关键约束覆盖表、plan 需求覆盖矩阵、实现回填、测试覆盖核销、反馈循环优先的诊断流程和交付前验证核销，用于减少 design/plan 写清楚但实现遗漏边界的情况。

项目初始化会记录 `.codex/engineering-workflow/project/contracts.md`，用于沉淀当前项目语言、框架、接口校验、输入标准化和依赖保证。后续实现应遵从这些项目契约，避免在内部逻辑重复写字符串标准化、空值/空内容判断、依赖存在性判断或无证据默认值兜底。

默认工作产物目录为目标仓库的 `.codex/engineering-workflow/`。需求文档、项目上下文、原型、handoff、报告和诊断记录默认写入该目录，不放在项目主目录。

## 维护原则

本仓库是 `engineering-workflow` 的唯一维护源。

- 所有规则、skill、模板和 README 修改都先提交到本仓库。
- 确认变更符合预期后，再同步到本地 Codex plugin 安装目录或重新安装 plugin。
- 不直接修改 Codex cache 中的 plugin 内容；cache 只视为安装产物。
- 被 `.gitignore` 忽略的运行期文件、缓存、构建产物、会话登记表、需求草稿、handoff、报告和临时原型默认不纳入版本管理。

## 工作产物目录

`engineering-workflow` skills 默认把中间产物写入：

```text
.codex/engineering-workflow/
  issues/
  project/
  context.md
  context-map.md
  adr/
  handoffs/
  reports/
  prototypes/
  debug/
```

这些文件默认用于当前 agent 协作和用户 review，不属于生产代码。除非用户明确要求共享某些文件，否则不要把 `.codex/engineering-workflow/` 强行加入 git。

## 安装

在本目录执行：

```bash
codex plugin marketplace add "$PWD"
codex plugin add engineering-workflow@engineering-workflow
mkdir -p ~/.codex
cp global/AGENTS.md ~/.codex/AGENTS.md
```

`global/AGENTS.md` 是面向全局安装的通用入口，只包含业务项目也需要遵守的常驻规则和 skill 路由。根目录 `AGENTS.md` 只用于维护本仓库，不要复制到 `~/.codex/AGENTS.md`。

安装后新开一个 Codex thread，让 Codex 重新加载 plugin 和 `AGENTS.md`。

## 更新

修改 `plugins/engineering-workflow` 后，建议更新 plugin 版本或 cachebuster，再重新安装：

```bash
codex plugin add engineering-workflow@engineering-workflow
```

如果 Codex 仍未加载新内容，新开 thread 再验证。

## 校验

修改本仓库后可运行：

```bash
scripts/validate-workflow.sh
```

该脚本检查 plugin JSON、marketplace JSON、skill frontmatter、`agents/openai.yaml` 和 reference 链接。

## 常见问题

### `hitl-loop.template.sh` 是什么？

`hitl-loop.template.sh` 是 human-in-the-loop 诊断循环模板，用于普通 bug 排查时强制 agent 先建立可观察反馈循环：复现、记录证据、提出可证伪假设、验证、再决定是否修改。它是模板文件，不是默认自动执行脚本；项目需要时可以复制或改造成适合当前仓库的检查脚本。

### 为什么区分 `diagnosis-workflow` 和 `incident-debugging`？

`diagnosis-workflow` 面向普通本地 bug、失败测试、性能回退和一般异常行为，核心是建立可靠反馈循环，避免猜测式修复。

`incident-debugging` 面向线上问题、生产 bug、数据误删、重复调用、幂等性、并发和事故排查。这类问题风险更高，必须从真实入口复现、证明根因，并用同一路径验证修复结果；因此需要比普通诊断更严格的完成声明和证据要求。

## 内容

```text
AGENTS.md
global/AGENTS.md
.agents/plugins/marketplace.json
scripts/validate-workflow.sh
scripts/validate-workflow.py
scripts/audit-defensive-code.sh
plugins/engineering-workflow/
  .codex-plugin/plugin.json
  skills/
    project-setup/
    requirements-workflow/
    diagnosis-workflow/
    incident-debugging/
    prototyping/
    issue-slicing/
    architecture-review/
    coding-standards/
    testing-policy/
    engineering-handoff/
    verification-delivery/
```
