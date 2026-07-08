# 错误、日志和可观测性

## Fail Fast

- 不用 fallback、默认值、空 catch、`return nil`、`return true`、忽略 promise/future/task/goroutine 错误等方式让未知错误继续流转。
- 合法 fallback 必须来自明确业务契约，例如旧数据兼容、用户明确选择的降级模式、外部依赖失败时已确认的产品行为；同时要留下可观测信号。
- 如果错误会跨边界暴露给用户或调用方，边界层应按项目风格映射成可理解响应；内部仍要保留错误类型、错误码、上下文或 cause。
- 难以定位的问题不要做表面修复。先补充 targeted log、metric、trace、事件记录或复现 harness；如果当前信息不足，应明确说明缺少哪些观测点和下一步如何补。

## 错误处理

- 遵循已有 error type、exception、error code、wrapping、result 和返回值约定。
- 不吞错。
- 不写空 catch，不忽略返回的 error，不把异常只记日志后当作成功继续执行。
- 不把重要错误替换成缺少上下文的默认值。
- 不用无证据 fallback、重试、降级或缓存值掩盖未知问题。
- 在能帮助调用方诊断时补充上下文。
- 用户可见错误和内部错误应符合项目已有实践。
- 内部错误到边界层响应的映射应放在边界层。
- 避免每一层都重复记录同一个错误；优先在边界层或上下文最丰富的位置记录一次有意义的日志。
- 异步错误必须被正确 await/catch/return。

## 日志

- 只记录排查问题所需的业务上下文，优先覆盖入口、关键状态变化、外部依赖调用结果、异常分支和不可自动恢复的失败。
- 关键路径日志应能串起一次请求或任务，例如 request/correlation id、tenant/user/resource id、job/message id、操作阶段、状态前后值或外部依赖摘要；具体字段沿用项目风格。
- 不记录 secret、token、密码、完整隐私数据或大体量 payload。
- 移除临时 debug log、print、console.log 和断点残留。
- 不用噪音日志掩盖不清晰的控制流。
- 如果当前日志不足以证明根因或验证修复，先补 targeted observability 或向用户说明信息缺口，不假装修复已经成立。
