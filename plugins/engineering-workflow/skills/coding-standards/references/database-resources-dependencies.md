# 数据库、资源、并发和依赖

## 数据库和 migration

schema 或 migration 变更必须显式考虑：

- 旧数据兼容。
- 发布过程中的前向/后向兼容。
- 是否需要回填。
- 回滚风险。
- 幂等性和重试行为。
- 数据影响范围。
- 多次部署场景下的 expand/contract 顺序。
- 新字段的 `NULL` / default 策略。
- 在线 DDL 或锁表风险。
- 索引创建策略，包括数据库支持时的并发或分批创建。
- 旧代码/新代码读写兼容。
- 回滚是反向 migration 还是 forward fix。
- 回填批大小、可恢复性和失败处理。

repository/DAO 代码应遵循项目已有 query、transaction、lock、pagination、soft delete 和错误处理模式。已有 repository/DAO 边界时，不要在业务逻辑或 UI 层散落 SQL。

## 资源、异步和并发

- I/O、数据库、RPC 和长耗时操作应按项目风格传递取消信号、deadline 或 request context。
- 当前层已经接收 context、signal、request scope 或 lifecycle 时，应尊重取消和超时。
- rows、response body、文件、stream、subscription、timer 和其他 closer/disposable 必须在所有路径释放。
- error 路径需要 rollback transaction，除非项目 helper 已经处理。
- 不启动没有生命周期、取消路径和错误处理策略的 goroutine、thread、worker、task 或 subscription。
- 不用 sleep 做同步；优先使用语言或项目已有的同步、事件和测试 helper。

## 依赖变更

- 不为小便利功能新增依赖。
- 不随意升级版本。
- 说明为什么需要该依赖，以及为什么现有方案不足。
- 依赖变更后运行相关验证。
- 同步 package manager 对应的 lockfile。
- 避免没有解释的 replace、override、resolution、exclude 或本地路径依赖。
- 新增库时考虑 license、传递依赖、包体积和运行时影响。
- 如果依赖影响 generator、schema、API 或类型定义，同步生成并验证生成代码。
