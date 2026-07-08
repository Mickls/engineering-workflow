# 校验位置和防御式代码

## 校验位置

外部输入应在调用链顶层校验：

- `HTTP/RPC handler`、controller、route、resolver。
- `CLI` 命令入口。
- `event/job` 接收处、定时任务入口、消息消费处、webhook。
- 前端表单提交、URL/query 解析、跨窗口/跨线程消息入口。
- 会被当前模块外部使用的 public/exported API。
- 序列化、反序列化、文件、网络和数据库读取的边界。

顶层校验包括 nil/null/undefined、空请求/空集合、字符串标准化、枚举合法性、必填 ID、分页边界、权限、租户范围、资源归属、外部数据结构版本和兼容性。

内部函数不重复做防御式校验，除非：

- 该函数本身就是外部边界。
- 确实存在未校验的不安全路径能到达这里。
- 项目已有模式要求该边界本地校验。
- 不校验会让合法内部调用不可避免地产生 panic、crash 或未捕获异常。

## 防御式代码候选

- `string-normalization`：重复 trim、strip、normalize、大小写转换、空白折叠、类型 coercion。
- `empty-check`：重复 nil、null、undefined、None、Optional empty、空字符串、空集合、空对象判断。
- `dependency-guard`：对已由构造函数、依赖注入、模块系统、框架生命周期、generated code 或 fixture 保证存在的 service、repository/DAO、client、config、logger、context、component/provider 反复判空。
- `default-fallback`：无证据地把缺失、非法或异常输入替换成默认值继续执行。
- `error-wrapping` / `logging`：多层重复 wrapping、重复日志或重复错误映射。
- `silent-error`：空 catch、忽略 error/exception、只记录日志但继续执行、吞掉 async/goroutine/task 错误。
- `masked-retry-degrade`：无证据重试、降级、跳过步骤或返回缓存值，使真实错误不再暴露。

这些候选不是一律禁止。保留它们必须有边界证据：public/exported API、外部数据读取、反序列化、旧数据兼容、第三方回调、并发/lifecycle 安全、真实未校验入口，或项目明确要求的本地防线。

## 存量清理

清理重复防御代码时：

1. 界定范围。
2. 扫描候选。
3. 分级处理：
   - `keep-boundary`：外部边界、public/exported API、反序列化、旧数据兼容、安全边界。
   - `remove-redundant`：上游或项目契约已保证，当前判断无独立价值。
   - `move-to-boundary`：校验需要存在但位置错误。
   - `needs-evidence`：调用链或契约证据不足，不动。
4. 每次只清理有证据的一小组候选。
5. 删除前后用完整调用链测试、编译/typecheck、现有回归测试或明确代码审查证据证明行为未变或符合预期变化。
