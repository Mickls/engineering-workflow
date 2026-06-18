# Commands 模板

```md
# Commands

## Freshness

- updated_at:
- source_commit:
- scan_scope:
  - package scripts / Makefile / task runner / CI config / README
- evidence_paths:
  -
- watch_patterns:
  - Makefile
  - package.json
  - pnpm-lock.yaml
  - yarn.lock
  - package-lock.json
  - pyproject.toml
  - requirements*.txt
  - go.mod
  - go.sum
  - pom.xml
  - build.gradle*
  - Cargo.toml
  - Cargo.lock
  - .github/**
  - .gitlab-ci.yml
  - README*
- known_gaps:
  -

## Lint

- 命令：
- 适用范围：
- 成本/耗时：

## Test

- 单元测试：
- 集成测试：
- 指定 package / suite：
- 需要的环境：

## Build / Typecheck

- 命令：
- 何时必须运行：

## Format

- 命令：
- 禁止使用的格式化命令：

## Notes

- 不稳定测试：
- 需要外部服务的测试：
- 常见失败处理：
```

要求：

- 只记录当前项目真实可用或有明确证据的命令。
- 如果命令来自 CI、README、package scripts 或 Makefile，需要在 `evidence_paths` 中标明。
- package manager、lockfile、CI、构建配置或测试环境变化后，需要 targeted refresh 本文件。
- 无法确认的命令写入 `known_gaps`，不要把猜测命令写成事实。
