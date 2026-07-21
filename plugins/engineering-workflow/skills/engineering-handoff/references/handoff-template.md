# 工程交接模板

```md
# 工程交接

## 当前目标

## 关键文档

- 需求设计：
- 实施计划：
- 覆盖矩阵：

## 决定与证据账本

- decision ledger：
- standing constraints：
- source commit / 工作树基线：
- scan scope / evidence paths：
- watch patterns / known gaps：
- 证据失效条件：

## 已完成

## 已修改文件

## 验证

## 未验证项和风险

## 工作区状态

## 建议后续 skills

## 下一步
```

要求：

- 除非用户或项目规则明确要求其他语言，handoff 文档正文、标题、表格列名和状态解释都必须使用中文；文件名、命令、API、代码标识符、状态枚举和引用路径可以保留英文。
- 只记录当前有效状态并引用权威文档，不复制长对话、废弃推理或完整代码搜索结果。
- 恢复时 source commit、scope 和失效条件均未变化，应直接复用账本；存在冲突时集中 refresh 一次。
