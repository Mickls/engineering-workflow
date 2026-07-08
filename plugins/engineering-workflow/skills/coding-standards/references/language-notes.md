# 语言补充规则

## Go

- 使用 `context.Context` 传递取消、deadline 和 request scope。
- 遵循项目已有 `gofmt`、`go test`、`go vet`、`golangci-lint` 和生成代码流程。
- 依赖变更后判断是否需要 `go mod tidy`。
- 检查 major version import path 变化。
- 不启动没有生命周期和错误处理策略的 goroutine。
- 除非已经完整追溯所有调用方，否则 exported package 函数应视为边界。

## TypeScript / JavaScript

- 遵循项目已有类型严格程度；不要随意使用 `any`、类型断言或忽略类型错误。
- 异步逻辑必须正确 `await`、return 或 catch。
- 前端状态、数据请求、路由、表单和组件拆分沿用项目现有模式。
- 依赖变更使用项目已有包管理器，并同步对应 lockfile。
- 不把类型修复伪装成运行时逻辑修复。

## Python

- 遵循项目已有类型标注、dataclass/pydantic/schema 和异常处理风格。
- 使用 context manager 管理文件、连接、锁和临时资源。
- 不为局部传值滥用 dict/dataclass；跨边界时再定义稳定结构。
- 依赖变更同步项目使用的 `requirements`、`pyproject`、lockfile 或环境配置。

## Java / Kotlin / JVM

- 遵循项目已有 service、repository、DTO、exception、transaction 和 DI 风格。
- 不绕过已有 validation、transaction、security 或 mapper 边界。
- 依赖变更同步 Gradle/Maven 配置和 lock/version catalog。
