# Humanize Tech Writing

把 AI 生成的中文技术文字改回工程师日常会写的语言。

这个 skill 专门处理 **项目说明文件和代码注释**，重点不是“把文章写得更像人”，而是去掉：

- AI 生造词和自造复合名词
- `赋能 / 闭环 / 承接 / 拉齐 / 收口 / 底层逻辑` 一类工程黑话
- `能力 / 机制 / 体系 / 方案` 等没有具体内容的抽象词
- `优化 / 提升 / 完善` 等没有说明实际改动的模糊动词
- 翻译腔、讲义腔、模板化总结
- 只是把代码翻译成中文的无效注释
- 用注释记录“这次改了什么”的 AI 习惯

同时严格保留正式技术术语、项目术语、标识符、API 字段和已有事实。

## 例子

### AI 生造词

改前：

> 对失败态进行统一承接，提升异常感知度。

改后：

> 请求失败时统一返回错误信息，让调用方能区分失败原因。

### 工程黑话

改前：

> 通过缓存能力承接下游抖动，形成完整兜底闭环。

改后：

> 下游超时时读取缓存，避免请求直接失败。

### 无效代码注释

改前：

```java
// 获取用户
User user = userService.getUser(id);
```

代码已经说明了动作，这条注释应该直接删除。

更值得保留的是代码本身看不出的原因：

```java
// 下游偶发超时，因此这里保留最近一次成功结果作为回退。
```

## 设计原则

这个 skill 不把所有“专业词”都当 AI 黑话。

例如 `幂等`、`回源`、`透传`、`背压`、`熔断`、`最终一致性` 在正确语境里都是正常技术术语。判断优先级是：

1. 用户明确指定的术语
2. 项目 glossary、`AGENTS.md`、`CONTRIBUTING.md` 和设计文档中的既有术语
3. 代码和接口中稳定出现的领域术语
4. 行业通用技术术语
5. 普通中文

只有缺少这些依据、又能直接说清动作时，才把“高级词”改成普通表达。

## 18 类检查规则

| # | 规则 | 典型问题 |
|---|---|---|
| 1 | 自造复合名词 | `失败态承接`、`异常感知度` |
| 2 | 互联网黑话 | `赋能`、`闭环`、`拉齐`、`收口` |
| 3 | 空泛容器词 | `能力`、`机制`、`体系`、`方案` |
| 4 | 名词化过重 | `对参数进行校验` |
| 5 | 模糊动词 | `优化`、`提升`、`完善` |
| 6 | 给局部逻辑发明概念 | `弱信号保护策略` |
| 7 | 不写执行主体 | `失败后会重试` |
| 8 | 不写触发条件 | `系统会回退到缓存` |
| 9 | 不写实际结果 | `提升稳定性` |
| 10 | 同义词轮换 | 同一对象轮换叫请求/任务/作业 |
| 11 | 无依据强度词 | `显著`、`大幅`、`精准`、`高效` |
| 12 | 营销腔和隐喻 | `保驾护航`、`丝滑`、`最后一道防线` |
| 13 | 模板化过渡 | `首先`、`值得注意的是`、`综上所述` |
| 14 | 金句式对比 | `不是 X，而是 Y` |
| 15 | 欧化翻译腔 | `错误将会被统一地记录` |
| 16 | 注释翻译代码 | `// 获取用户` |
| 17 | 注释记录改动历史 | `// 新增缓存逻辑` |
| 18 | 注释过多 | 每个 if / getter 都解释一遍 |

完整规则和改前/改后示例见 [`SKILL.md`](./SKILL.md)。

# 安装

整个 skill 的运行时核心是 `SKILL.md`。

## Codex：放进项目中长期生效

Codex 会发现项目里的 `.agents/skills/<skill-name>/SKILL.md`。因此最直接的做法是把这个 skill 放进仓库：

```text
your-project/
├── AGENTS.md
└── .agents/
    └── skills/
        └── humanize-tech-writing/
            └── SKILL.md
```

例如把本仓库作为 subtree、submodule，或者在项目初始化脚本中复制 `SKILL.md` 到上述目录。

项目级 skill 的好处是它跟 Git 仓库一起走，团队成员和 Codex 的不同会话都能看到同一套规则。

## 让它对文档和注释更稳定地自动生效

只安装 skill 并不意味着每次任务都一定会选择它。建议在目标项目根目录的 `AGENTS.md` 增加：

```md
## Technical writing

When creating or modifying Chinese technical documentation or code comments,
use the `humanize-tech-writing` skill before finishing the task.

Prefer plain, established engineering language. Remove AI-coined terminology,
unnecessary abstractions, vague jargon, marketing language, and comments that
only restate the code.

Preserve identifiers, API fields, protocol names, established technical terms,
string constants, and project-specific terminology unless the user explicitly
asks to change them.
```

这样分工比较清楚：

- `AGENTS.md` 决定 **什么时候要应用这套规则**
- `SKILL.md` 决定 **具体怎么检查和改写**

## 其他 Agent

这个仓库使用标准 `SKILL.md` 结构。对于支持 Agent Skills 的工具，把整个目录放到该工具的项目级 skill 目录即可。

如果工具只支持项目说明文件，也可以直接引用 `SKILL.md`，并在对应的项目指令文件中要求：修改中文技术文档或代码注释时应用它。

## Claude Code 插件

仓库保留 Claude Code plugin manifest，可通过仓库 marketplace 安装：

```text
/plugin marketplace add keru-s/humanize-tech-writing
/plugin install humanize-tech-writing@humanize-tech-writing
```

# 使用方式

显式调用时可以说：

```text
用 humanize-tech-writing 检查这次修改里的 README 和代码注释。
```

或者：

```text
把 docs/design.md 里明显的 AI 生造词改成人类工程师正常会写的表达，技术术语不要动。
```

也可以只做 review：

```text
用 humanize-tech-writing review 当前 diff，只列出明显影响理解或 AI 味很重的技术文字，不要直接修改。
```

# 适用范围

适合：

- README / docs
- ADR / RFC / 架构和设计说明
- JavaDoc / docstring
- 行内和块注释
- API / 配置 / 运维说明
- AI Coding Agent 自动生成的说明文字

不适合：

- 市场文案、公众号、小说等通用写作
- 自动重命名类、方法、字段
- 在不了解领域上下文时“大扫除”项目术语

# 与上游项目的关系

本项目 fork 自 [jiji262/humanizer-chinese](https://github.com/jiji262/humanizer-chinese)，后者又基于 [blader/humanizer](https://github.com/blader/humanizer) 的思路做了中文本土化。

原项目面向通用中文写作，包含 36 类 AI 写作模式。本 fork 从 `2.0.0` 起改为 **技术写作专项 skill**：保留其中对中文 AI 腔有用的判断，同时重新设计了生造词、工程黑话、术语保护和代码注释规则。

感谢原作者对中文 AI 写作模式的整理。本项目继续使用 MIT License。

# 版本历史

- **2.0.0** — 从通用中文 Humanizer 改为技术写作专项 skill。重点处理 AI 生造词、工程黑话、抽象名词化、技术表达不具体以及无效代码注释；增加项目术语保护和项目级安装方式。
