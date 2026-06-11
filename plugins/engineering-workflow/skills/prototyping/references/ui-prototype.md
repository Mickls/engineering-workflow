# UI Prototype

用于回答“这个界面或交互应该是什么样”。

## 形态

- 独立 UI 需求优先遵循 `requirements-workflow`：创建静态 HTML 到 `.codex/engineering-workflow/issues/<REQ-or-EPIC>/prototype.html`。
- 非 issue 绑定的探索性原型默认放到 `.codex/engineering-workflow/prototypes/`。
- 只有项目已有 Storybook、playground、demo app、scratch route 或明确临时目录时，才可以嵌入现有环境判断真实密度和上下文。
- 不得把原型放入生产页面、生产路由或需要上线的代码路径；不得触发生产级 lint/test/build 循环。
- 可以生成多个差异明显的方案，但默认 2-3 个即可。
- 方案差异应是信息架构、布局、操作流或状态表达差异，不只是颜色和文案。
- 多 variant 原型可以使用 `?variant=`、底部切换栏或键盘快捷切换，但这些交互仅服务于需求确认。

## 必须覆盖

- 默认态。
- 关键操作态。
- 空态、错误态、成功态中与需求确认相关的状态。
- 移动端或窄屏风险，如果该 UI 会在这些场景使用。

## 交付

- 给出可打开路径或本地 URL。
- 说明每个 variant 的意图。
- 记录未覆盖的真实数据、权限、接口、性能、生产组件复用等限制。
- 用户选择后删除未采用原型，或把结论写回 design/plan。
- 原型只做有限自检；非阻塞视觉精修不进入反复 review/fix 循环。
