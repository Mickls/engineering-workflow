# Engineering Workflow Repo Instructions

## 1. 仓库定位

本仓库是 `engineering-workflow` Codex plugin 和全局 AGENTS 模板的源仓库。

- plugin 源码位于 `plugins/engineering-workflow/`。
- 可安装到用户全局的 AGENTS 模板位于 `global/AGENTS.md`。
- 根目录 `AGENTS.md` 只说明如何维护本仓库，不应复制到 `~/.codex/AGENTS.md`。
- 已安装 plugin、Codex cache 和用户本地 `~/.codex/AGENTS.md` 都是安装产物，不是维护源。

## 2. 修改原则

- 所有规则、skill、模板、README 和 marketplace 修改都先落在本仓库。
- 未经用户确认，不直接修改 `~/.codex/plugins/cache/`、`~/.codex/AGENTS.md` 或其他已安装产物。
- 不把 `.codex/` 下的工作产物纳入 git；它只用于本仓库内的需求草稿、review、handoff 和运行期记录。
- 不使用 `git add -f` 纳入 ignored 文件，除非用户明确要求并确认原因。
- 默认使用中文回复，技术名词、命令、代码标识符保留英文。

## 3. 文件职责

- `global/AGENTS.md`：用户安装到 `~/.codex/AGENTS.md` 的全局协作规则。只能写所有业务项目都适用的原则、skill 路由和硬门禁。
- `AGENTS.md`：本文件，只用于指导 agent 如何维护本仓库。
- `README.md`：面向用户和分享对象，说明安装、更新、维护源、工作产物目录和校验方式。
- `.agents/plugins/marketplace.json`：本仓库自带 marketplace。
- `plugins/engineering-workflow/.codex-plugin/plugin.json`：plugin manifest。
- `plugins/engineering-workflow/skills/*`：各工程化 skill。
- `scripts/validate-workflow.sh`：校验入口。
- `scripts/validate-workflow.py`：skill 结构和 reference 链接校验逻辑。

## 4. 维护流程

修改本仓库时：

1. 先确认改动属于 repo-local 维护说明、global AGENTS、plugin manifest、skill、reference、README 还是脚本。
2. 如果改动影响用户全局行为，修改 `global/AGENTS.md`，不要把维护仓库专属内容写进去。
3. 如果改动影响某个 skill 的执行规则，同时检查对应 `agents/openai.yaml` 的 prompt 是否需要同步。
4. 如果改动影响产物目录、安装方式或分享方式，同步更新 `README.md`。
5. 如果新增 skill、reference 或校验规则，同步更新校验脚本或 README 内容列表。

### Skill 编辑规范

- `SKILL.md` 只作为入口文件，保留触发后必须立刻知道的目标、适用场景、硬门禁和 `references/` 路由。
- 不把长 checklist、模板、状态解释、语言特化规则、细化流程、大段示例或背景说明继续堆进 `SKILL.md`；这些内容默认放入同一 skill 的 `references/`。
- 新增或保留 `SKILL.md` 正文内容前，先判断它是否每次触发该 skill 都必须加载；如果只是特定分支、特定语言、特定文档或特定验证阶段才需要，必须下沉到 reference。
- 每个 `references/*.md` 必须由同一 skill 的 `SKILL.md` 直接链接，并说明何时读取；不要创建隐藏 reference 或多级 reference 路由。
- `SKILL.md` frontmatter 只允许 `name` 和 `description`；触发条件尽量放在 `description`，正文不重复写大段触发说明。
- 单个 `SKILL.md` 超过 100 行视为入口膨胀，需要拆分或压缩，除非先调整校验脚本并说明原因。

## 5. 验证

修改后至少运行：

```bash
scripts/validate-workflow.sh
git diff --check
```

如果修改了 plugin manifest 或 marketplace，确保 JSON 校验通过。

如果修改了 `agents/openai.yaml`，确保 YAML 解析通过。

如果修改了 plugin 结构，优先运行系统 `plugin-creator` 的 `validate_plugin.py`；如果本机缺少 `PyYAML`，使用临时 venv，不污染项目或全局 Python。

## 6. 交付说明

最终回复需要说明：

- 改了哪些 repo 文件。
- 是否影响 `global/AGENTS.md`。
- 是否影响 plugin skills 或 manifest。
- 执行了哪些校验命令。
- 是否同步了本地 Codex 安装产物；默认应为未同步。
