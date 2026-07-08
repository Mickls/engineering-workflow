# 验证命令

## lint

编码后运行项目对应 lint。全项目 lint 成本过高时，可以只检查改动文件或受影响 package，但必须说明检查范围。

如果不知道 lint 命令：

- 检查项目 scripts、Makefile、CI 配置、package scripts 或语言工具链。
- 仍找不到时，说明未找到 lint 命令。

## 测试

运行与本次改动相关的测试：

- 受影响 package 测试。
- 覆盖调用链的 feature 或 integration 测试。
- bugfix 的回归测试。
- 触及共享行为时的更大范围测试。

如果不知道测试命令：

- 检查项目 scripts、Makefile、CI 配置、README、package scripts 和语言工具链。
- Go 项目中判断应运行 package 级 `go test ./...`，还是更窄范围的 `go test ./path`。
- 仍找不到时，说明未找到测试命令，并列出检查过的位置。

如果测试失败，先使用 `testing-policy` 判断应修改测试还是生产代码。

## build / typecheck / compile

以下情况需要运行 build、typecheck 或 compile：

- interface 发生变化。
- 生成代码发生变化。
- 依赖发生变化。
- build tags 或配置发生变化。
- 测试没有充分编译受影响范围。

如果不知道 build 或 typecheck 命令，检查项目 scripts、Makefile、CI 配置、README、package scripts 和语言工具链。Go 项目中判断 `go test` 是否已经编译受影响 package，或是否还需要 `go build ./...`。

## 纯文档变更

纯文档变更可接受的验证包括：

- 回读检查。
- markdown lint。
- 链接/路径检查。
- 项目结构校验。

如果代码 lint/test/build 不适用，明确说明原因。
