# 命令模板

```md
# 命令

## Freshness 元数据

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

## Lint 命令

- 命令：
- 适用范围：
- 成本/耗时：

## 测试命令

- 单元测试：
- 集成测试：
- 指定 package / suite：
- 需要的环境：

## Build / Typecheck 命令

- 命令：
- 何时必须运行：

## Format 命令

- 命令：
- 禁止使用的格式化命令：

## 备注

- 不稳定测试：
- 需要外部服务的测试：
- 常见失败处理：
```

要求：

- 除非用户或项目规则明确要求其他语言，命令文档正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、package script 名、状态枚举和引用路径可以保留英文。
- 只记录当前项目真实可用或有明确证据的命令。
- 如果命令来自 CI、README、package scripts 或 Makefile，需要在 `evidence_paths` 中标明。
- package manager、lockfile、CI、构建配置或测试环境变化后，需要 targeted refresh 本文件。
- 无法确认的命令写入 `known_gaps`，不要把猜测命令写成事实。
