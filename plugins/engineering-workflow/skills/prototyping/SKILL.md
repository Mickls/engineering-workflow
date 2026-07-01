---
name: prototyping
description: "用于在正式实现前构建 throwaway 原型验证 UI、交互、状态机、业务规则、数据模型或 API 形状；区分 UI prototype 和 logic prototype，并要求原型回答具体问题后删除或沉淀结论。"
---

# 原型工作流

## 概述

原型是临时代码，用来回答一个明确问题。它不是生产实现，不追求完整测试、错误处理或可维护抽象。

## 分支选择

- UI 问题：页面、组件、布局、流程、状态展示，读取 [ui-prototype.md](references/ui-prototype.md)。
- Logic 问题：状态机、业务规则、数据模型、API 形状，读取 [logic-prototype.md](references/logic-prototype.md)。

如果不确定，先说明假设；后端规则默认 logic，页面/组件默认 UI。

## 通用规则

- 写清原型要回答的问题。
- 跟随项目现有运行时和目录约定。
- 明确标记为 prototype，不放进生产路径。
- 默认写入当前工作产物根目录的 `prototypes/`；如果原型绑定某个需求，写入 `<artifact-root>/issues/<REQ-or-EPIC>/`。
- 默认不持久化；如必须持久化，使用 scratch DB 或清晰标记的临时文件。
- 只做足以帮助用户判断的有限自检。
- 原型阶段不触发生产级 lint/test/build，也不进入反复 review/fix 循环。
- 用户确认后，删除原型或把结论沉淀到 `<artifact-root>/issues/`、`<artifact-root>/adr/`、design 或正式实现计划。

## 与 requirements-workflow 的关系

独立 UI 需求仍遵循 `requirements-workflow` 的 UI 原型门禁：默认生成可直接打开的静态 HTML 到 `<artifact-root>/issues/<REQ-or-EPIC>/prototype.html`。本 skill 补充更细的 UI/logic 原型执行方法。
