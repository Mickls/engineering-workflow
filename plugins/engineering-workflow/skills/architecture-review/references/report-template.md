# 架构审查报告模板

```md
# 架构审查

## 审查范围

- 入口：
- 相关模块：
- 读取的 context / ADR：

## 候选改进

### 候选 1：标题

- 涉及文件：
- 当前问题：
- 建议方案：
- 预期收益：
- 风险：
- 推荐强度：strong / worth-exploring / speculative

## 优先建议

先做什么，为什么。
```

除非用户或项目规则明确要求其他语言，架构审查报告正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。

如果生成 HTML 报告，默认写入 `<artifact-root>/reports/architecture-review-<timestamp>.html`，或在用户要求临时文件时写入系统 temp 目录。不要写入生产代码路径。
