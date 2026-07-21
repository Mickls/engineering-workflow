# Engineering Workflow

这是一套可分享的 Codex 工程化工作流配置，包含：

- `AGENTS.md`：维护本仓库时给 agent 读取的 repo-local 说明。
- `global/AGENTS.md`：安装到 `~/.codex/AGENTS.md` 的全局 agent 行为入口和 skill 路由。
- `plugins/engineering-workflow`：Codex plugin，内含项目初始化、需求、普通诊断、线上问题排查、原型、需求拆分、架构审查、通用编码、测试、工程交接、验证交付等 skills。
- `.agents/plugins/marketplace.json`：本目录自带的本地 marketplace。

工作流用项目上下文、interview 前的完整 discovery、可继承的 decision ledger、真实场景驱动的低负担澄清、风险触发的 AFK/HITL 切片、编码前验收场景、实现路径契约、完整链路测试和基于证据的交付门禁，减少重复确认、疲劳等待、“测试全过但实际不可用”、实现偏离和不必要的人工 review。

skill 的 frontmatter `description` 只承担 progressive disclosure 的路由职责，前置说明何时使用和必要边界；`SKILL.md` 正文保留核心流程、硬门禁和 reference 路由，详细 checklist、模板和语言规则放入按需读取的 `references/`。`agents/openai.yaml` 的 `default_prompt` 只提供一句调用示例，不复制 skill 流程。

运行时工作产物默认写入目标仓库 `.codex/engineering-workflow/` 并保持 ignored。正文默认中文；项目要求英文主文档时保持英文权威，并在该目录提供需要 review 的中文辅助说明。

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
  review-notes/
```

这些文件默认用于当前 agent 协作和用户 review，不属于生产代码。除非用户明确要求共享某些文件，否则不要把 `.codex/engineering-workflow/` 强行加入 git。

非轻量需求先创建 `README.md(status=clarifying)` 和 `clarification.md`。AI 在 interview 前完成主要入口、跨模块 owner、standing constraints 和第一层条件分支调查，维护带语义 key、scope、继承和例外的 decision ledger；新问题先去重，用户纠错先审计全部依赖。用户只确认行为、取舍和风险，项目已有模式覆盖的技术细节由 AI 负责。用户批准总结或明确授权按总结设计并实现后，才形成权威 `design.md` 和 `plan.md`。

实现计划按用户可观察闭环标记 AFK/HITL，并记录 interaction budget、临时逐单元 review 的截止条件及资源边界。验收场景在编码前确定；AFK 是批准后的默认执行方式，只有新用户决定、行为偏离、证据缺口、手动步骤、未覆盖风险或 budget 命中时暂停。上下文压缩后复用带 source commit 的 evidence ledger；原验收完成后立即交付，额外发现拆成 follow-up。HITL 和最终交付先提供普通语言的行为/风险 review 包，再附技术证据。

## 安装

在本目录执行：

```bash
codex plugin marketplace add "$PWD"
codex plugin add engineering-workflow@engineering-workflow
mkdir -p ~/.codex
cp global/AGENTS.md ~/.codex/AGENTS.md
```

如果 `codex plugin list` 仍显示旧的 `engineering-workflow@personal` 为 installed/enabled，先执行：

```bash
codex plugin remove engineering-workflow@personal
```

该命令只移除旧安装配置和 cache，不删除 personal marketplace 中的源码目录。

`global/AGENTS.md` 是面向全局安装的通用入口，只包含业务项目也需要遵守的常驻规则和 skill 路由。根目录 `AGENTS.md` 只用于维护本仓库，不要复制到 `~/.codex/AGENTS.md`。

安装后新开一个 Codex thread，让 Codex 重新加载 plugin 和 `AGENTS.md`。

## 更新

修改 `plugins/engineering-workflow` 后，使用 plugin-creator helper 更新 cachebuster，再重新安装：

```bash
python3 /Users/jiangcheng/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py plugins/engineering-workflow
codex plugin add engineering-workflow@engineering-workflow
```

如果 Codex 仍未加载新内容，新开 thread 再验证。

## 校验

修改本仓库后可运行：

```bash
scripts/validate-workflow.sh
```

该脚本检查 plugin/marketplace JSON、skill frontmatter、description routing contract、reference 链接、规则 ownership、global/skill context budget，以及 `agents/openai.yaml` 的单句、长度和 `$skill-name` 门禁。

校验脚本本身的正反向测试：

```bash
python3 -m unittest discover -s tests -v
ruby -Itest test/validate_agent_metadata_test.rb
```

交付前可运行最小正确实现审计：

```bash
scripts/audit-minimal-correct.sh
```

该脚本扫描当前 diff 中新增依赖、抽象、wrapper、配置、模板字段和疑似 hand-rolled native / stdlib 能力等候选。它是启发式审计，默认只报告候选并返回 0，不替代 lint/test/build、需求覆盖核销或人工判断。安装后的 plugin 会同时携带 `scripts/audit-minimal-correct.sh`，业务项目没有本地同名脚本时可由 agent 从 plugin root 调用。

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
scripts/validate-agent-metadata.rb
scripts/audit-minimal-correct.sh
scripts/check-workflow-rule-sync.py
tests/
test/
plugins/engineering-workflow/
  .codex-plugin/plugin.json
  scripts/
    audit-minimal-correct.sh
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
