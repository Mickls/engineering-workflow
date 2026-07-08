# Commit 规则

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
