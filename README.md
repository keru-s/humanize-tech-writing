# Humanize Tech Writing

把 AI 生成的中文技术文字改回工程师日常会写、团队成员容易理解的语言。

这个 Skill 面向 **项目技术文档和代码注释**。重点处理：

- AI 生造词和临时拼出的“概念名”
- `赋能 / 闭环 / 承接 / 拉齐 / 收口 / 底层逻辑` 一类空泛黑话
- `能力 / 机制 / 体系 / 方案` 等没有说明实际行为的抽象包装
- 需要读者先“解码”才能理解的隐喻、宣传式修辞和压缩标签
- 没有依据的 `优化 / 提升 / 显著 / 高效 / 稳定` 等说法
- 翻译腔、讲义腔、模板化总结和假对立
- 只是逐行翻译代码的无效注释

它同时强调 **语义安全**：保留事实、项目术语、正式技术术语、标识符、字面量，以及 MUST / SHOULD / MAY、可能 / 必须 / 不得等强弱语义。

## 核心原则

优先级从高到低：

1. 技术含义和事实正确
2. 项目术语和契约一致
3. 保留强弱语义、不确定性和边界条件
4. 清楚、具体、容易理解
5. 自然、简洁

### 具体化必须有来源

Skill 不会为了“把话说具体”而脑补实现。

例如原文只有：

> 优化失败场景处理。

如果代码、测试、接口定义和项目文档都没有说明具体怎么改，Skill 不应该擅自写成“超时后重试一次”或“返回某个错误码”。编辑时只改到证据支持的粒度；review 时可以指出这里缺少实际行为。

### 词形本身不是 AI 生造词的证据

`XX性 / XX化 / XX度 / XX链路` 在工程语境里大量存在正常术语，例如：

- 幂等性、原子性、可观测性
- 序列化、初始化、结构化
- 复杂度、相似度、置信度
- 调用链路、数据链路、全链路压测

只有一个词同时满足以下条件时，才优先拆成普通表达：

- 项目和行业里没有稳定含义
- 没有增加技术精度
- 只是把本可直接描述的动作或状态包装成新概念

### 优先字面事实，降低隐喻解码负担

“隐喻率”可以作为观察文风的信号，但 Skill 不使用机械阈值。真正检查的是：**读者是否必须先把修辞、黑话或形象标签翻译回字面含义，才能理解技术事实。**

项目明确使用的术语，以及在当前中文技术语境中足够稳定、精确的行业术语应保留。英文里存在对应概念，不代表中文直译就应该自动保留；例如项目没有明确使用 `配置漂移` 时，仍应判断“配置差异”“配置不一致”或更具体的事实是否更清楚。

对于没有稳定技术含义的表达，如果隐喻只增加气势、包装感或压缩程度，没有增加技术精度，则优先改成实际对象、动作、状态和关系。

例如：

- `写路径收口为管理后台` → `配置只能通过管理后台写入`
- `漂移可观测` → `可以发现配置差异`（项目未定义该术语时）

如果一个短标签隐藏了“谁做什么、对什么做、什么条件下做”，只有在上下文有依据时才展开；信息不足时不要为了去隐喻而脑补实现。

### 最小编辑

长期运行在 Coding Agent 中时，Skill 只修改真正有问题的文字：

- 不为了统一文风重写附近正常段落
- 不顺手重排无关章节
- 不为了避免重复给同一技术对象换名字
- 不修改标识符、API 字段、配置键、错误码和固定字符串

这样可以减少无意义的 diff noise。

## 不同文档使用不同规则

### README / ADR / RFC / 设计文档

重点是行为、约束、接口关系、取舍和有来源的设计理由。已有团队模板或章节顺序应保留。

### API / 文档注释

这里需要说明公开 contract，不能简单套用“注释只解释为什么”。根据接口需要保留：参数、返回值、异常、nullability、units、side effects、thread-safety、blocking behavior、ordering、lifecycle 和边界条件。

这类注释不限于某一种语言，例如 JavaDoc、Python docstring、JSDoc/TSDoc、KDoc、Rust doc comments、Go declaration comments、C# XML documentation comments 等都属于这个范围。

### 行内注释 / 块注释

优先记录代码本身看不出的原因、约束、不变量、兼容性、并发/顺序要求、临时 workaround 和容易踩坑的行为。

例如：

```java
// 获取用户
User user = userService.getUser(id);
```

代码已经表达了动作，这条注释通常可以直接删除。

不要为了“解释为什么”而猜一个设计理由。

长期代码注释也不应该记录 bug 排查过程、尝试过的方案或完整修复故事。若排查过程中发现了今天仍然成立的约束，只保留这个约束和必要原因；详细过程应留在 issue、PR、commit、ADR 或设计文档中。

### PR / changelog / migration guide

这些内容天然用于记录变更，可以直接写新增、删除、替换、兼容性变化和迁移步骤。长期代码注释中的“不要记录纯变更历史”规则不适用于它们。

## 写作风格

Skill 使用 plain language，优先普通词、具体动词、字面事实和项目已有术语。

会重点检查这些 AI 式表达，但不会机械禁词：

- `值得注意的是`
- `综上所述`
- `总而言之`
- `Bottom Line:`
- `In short:`
- `The simplest mental model is:`
- `Question? Answer.`
- `This isn't about X. It's about Y.`

`delve`、`foster`、`leverage`、`genuinely` 等英文词也按语境判断；存在更直接的表达时优先普通表达。

不会为了显得有洞察而主动制造 `不是 X，而是 Y` 的对立，也不会临时创造 `exact-head checks`、`editorial-row layouts` 这类项目中并不存在的复合标签。

同样，不会机械删除所有隐喻。判断标准不是词源，而是当前表达是否让读者多做一次“还原成技术事实”的脑内翻译。

列表的判断标准是 **是否更容易扫描**。requirements、constraints、options、steps、error cases、字段说明和检查项都适合列表；连续解释不需要为了“结构化”强行拆成 bullet。

# 安装

推荐使用 [`skills`](https://github.com/vercel-labs/skills) CLI 安装，不需要手动下载或复制 `SKILL.md`。

仓库把可安装的 Skill 放在 `skills/humanize-tech-writing/` 下，因此 CLI 会安装 Skill 包本身，而不会把 `.github/workflows`、仓库级 README 或其他维护文件一起复制进目标项目。

## 安装到当前项目

在目标项目根目录执行：

```bash
npx skills add keru-s/humanize-tech-writing
```

CLI 会发现仓库中的 `humanize-tech-writing` Skill，并让你选择要安装到哪些 Agent。

如果只想安装到 Codex，可以直接指定：

```bash
npx skills add keru-s/humanize-tech-writing -a codex
```

需要跳过交互确认时加 `-y`：

```bash
npx skills add keru-s/humanize-tech-writing -a codex -y
```

项目级安装是默认行为。对于 Codex，Skill 会安装到当前项目可发现的 Skill 目录中，适合跟项目一起使用。

## 全局安装

如果希望所有项目都能使用这个 Skill，加 `-g`：

```bash
npx skills add keru-s/humanize-tech-writing -a codex -g
```

也可以不指定 Agent，让 CLI 交互选择已检测到的 Agent：

```bash
npx skills add keru-s/humanize-tech-writing -g
```

## 查看而不安装

可以先确认 CLI 能正确发现 Skill：

```bash
npx skills add keru-s/humanize-tech-writing --list
```

## 手动安装

只有在不方便使用 `npx skills` 时，才需要手动把整个 `skills/humanize-tech-writing/` 目录放到 Agent 对应的项目级 Skill 目录。例如 Codex：

```text
your-project/
├── AGENTS.md
└── .agents/
    └── skills/
        └── humanize-tech-writing/
            ├── SKILL.md
            └── agents/
                └── openai.yaml
```

运行时核心是 [`skills/humanize-tech-writing/SKILL.md`](./skills/humanize-tech-writing/SKILL.md)。

## 建议的 AGENTS.md 触发规则

Skill 负责“怎么改”，项目指令负责“什么时候调用”。目标项目只需要一个很短的触发规则：

```md
## Technical writing

When creating or modifying Chinese technical documentation or code comments,
including API/documentation comments, use the `humanize-tech-writing` skill before finishing.

Preserve technical meaning, identifiers, literals, and established project terminology.
```

如果项目还希望覆盖 PR description、changelog 或 migration guide，可以把它们加入第一句的范围。

## 其他 Agent

`npx skills` 支持多个 Agent。安装时不传 `-a` 可以交互选择目标 Agent，也可以重复使用 `-a` 指定多个 Agent。

## Claude Code 插件

仓库保留 Claude Code plugin manifest，因此也可以通过 Claude Code plugin 安装：

```text
/plugin marketplace add keru-s/humanize-tech-writing
/plugin install humanize-tech-writing@humanize-tech-writing
```

# 使用方式

显式调用：

```text
用 humanize-tech-writing 检查这次修改里的 README 和代码注释。
```

只做 review：

```text
用 humanize-tech-writing review 当前 diff。只指出真正影响理解或明显带 AI 腔的技术文字；缺少事实时不要猜实现。
```

处理单个文件：

```text
把 docs/design.md 里明显的 AI 生造词、黑话和需要二次解码的隐喻改成工程师正常会写的表达。保留技术术语、事实和 MUST/SHOULD/MAY 的强弱语义。
```

# 适用范围

适合：

- README / docs
- ADR / RFC / 架构和设计说明
- API / 文档注释（例如 JavaDoc、docstring、JSDoc/TSDoc、KDoc 等）
- 行内和块注释
- TODO / workaround / 兼容性说明
- 配置 / 运维说明
- PR / changelog / migration guide
- AI Coding Agent 自动生成的技术文字

主要不用于：

- 市场文案、公众号、小说等通用写作
- 自动重命名类、方法、字段
- 在缺少上下文时批量“大扫除”项目术语

# 与上游项目的关系

本项目 fork 自 [jiji262/humanizer-chinese](https://github.com/jiji262/humanizer-chinese)，后者基于 [blader/humanizer](https://github.com/blader/humanizer) 的思路做了中文本土化。

原项目面向通用中文写作。本 fork 从 2.0.0 起转为技术写作专项 Skill；2.1.0 改成 **语义安全 + 文档类型感知 + 最小编辑** 的结构；2.2.0 增加 **字面事实优先 + 隐喻解码负担检查**，同时保护已经术语化的隐喻。

感谢原作者对中文 AI 写作模式的整理。本项目继续使用 MIT License。

# 版本历史

- **2.2.0** — 增加“优先字面事实，降低隐喻解码负担”：识别需要二次还原的隐喻、宣传式修辞和压缩标签，基于上下文展开真实对象/动作/关系；只保护项目明确术语和在中文技术语境中足够稳定的术语，不因英文存在对应概念而自动保留中文直译。
- **2.1.0** — 根据工程使用场景重构 Skill：增加“具体化必须有来源”、modality / uncertainty 保护和 minimal editing；按技术文档、API/文档注释、行内注释、变更文档区分规则；删除词缀判罪、固定 18 类模式和规则数量维护契约。
- **2.0.0** — 从通用中文 Humanizer 改为技术写作专项 Skill，重点处理 AI 生造词、工程黑话、抽象名词化、技术表达不具体以及无效代码注释。