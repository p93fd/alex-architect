# apple-design

[English](README.md) | **简体中文**

一个可移植的 [Agent Skill](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)，把 Apple 官方 [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) 整理成可直接使用的参考资料，帮助你为 iOS、iPadOS、macOS、watchOS、visionOS（部分内容也涉及 tvOS）设计或评审用户界面。它本质上就是一份 `SKILL.md` 加配套参考文件，所以不只支持 [Claude Code](https://claude.com/claude-code)（作为原生插件安装），也能通过 [skills.sh](https://skills.sh) 安装到任何支持 Agent Skills 格式的其他编码 Agent 上——比如 Codex、Cursor、OpenCode 等。

> 这是一个独立的、由社区维护的项目，与 Apple Inc. 没有任何从属、认可或赞助关系。文中出现的 "Apple"、"iOS"、"macOS" 等均为 Apple Inc. 的商标，此处仅用于描述内容主题。

## 为什么需要这个

Apple 的设计规范几乎每年都会随 WWDC 更新——最典型的是 2025 年推出的 **Liquid Glass** 设计语言，彻底重做了 iOS/iPadOS/macOS 的材质、图标和控件外观体系。大模型的训练数据很容易停留在过时版本，或者张冠李戴不同平台的规范。这个技能给 Claude 提供了一份经过整理、转述、互相关联的 HIG 核心内容摘要，外加一份完整的官方 URL 站点地图，遇到摘要没覆盖的精确数值、组件名称或最新表述时可以现查——让回答有依据，而不是靠猜。

## 目录结构

```
apple-design/
├── SKILL.md                          # 入口文件：触发条件、导航、速查表
├── .claude-plugin/
│   ├── plugin.json                   # 插件清单（name: apple-design）
│   └── marketplace.json              # Marketplace 清单（name: tzzs）
└── references/
    ├── principles.md                 # 八条设计原则
    ├── platforms.md                  # iOS / iPadOS / macOS / watchOS / visionOS 平台特性
    ├── materials-color.md            # Materials、Liquid Glass、Color 系统
    ├── typography-symbols.md         # 字体、Dynamic Type、SF Symbols
    ├── layout.md                     # 视觉层级、尺寸类别、安全区域
    ├── accessibility.md              # 视觉/听觉/行动能力/语言/认知五大维度
    ├── components.md                 # Buttons、Tab bars、Sidebars、Lists、Toolbars
    ├── app-icons.md                  # 分层图标设计、Icon Composer
    ├── patterns-gestures.md          # 手势设计与常见交互模式
    ├── resources.md                  # 官方 UI Kit、字体、SF Symbols、Icon Composer
    └── hig-sitemap.md                # 完整 HIG URL 索引，供现查使用
```

内容采用渐进式披露结构：`SKILL.md` 保持简短，按主题把你导向对应的 `references/*.md` 文件；`hig-sitemap.md` 则在摘要不够用时，给出可以直接现查的官方 URL。

## 安装方式

### Claude Code（原生插件，推荐给 Claude Code 用户）

```bash
claude plugin marketplace add tzzs/apple-design-skill
claude plugin install apple-design@tzzs
```

确认已生效：

```bash
claude plugin list
```

### 其他任意 Agent（Codex、Cursor、OpenCode 等 70+ 种）：通过 skills.sh

[skills.sh](https://skills.sh) 是一个类似包管理器的 Agent Skills 目录站点，背后是开源的 [`npx skills`](https://github.com/vercel-labs/skills) CLI 工具。因为这个仓库的 `SKILL.md` 就放在仓库根目录，CLI 会自动识别，不需要额外指定路径：

```bash
npx skills add tzzs/apple-design-skill
```

CLI 会检测你本机已安装的 Agent 并让你交互式勾选；如果想跳过交互，直接指定目标 Agent：

```bash
# 只给 Codex 和 Cursor 安装，且不弹交互确认
npx skills add tzzs/apple-design-skill -a codex -a cursor -y

# 一次性给 skills.sh 支持的所有 Agent 都装上，全局生效
npx skills add tzzs/apple-design-skill -g --all
```

查看已安装内容：

```bash
npx skills list
```

如果你更想把 Claude Code 的技能也统一交给 `npx skills` 管理（而不是走上面的原生插件系统），这条命令同样适用——它会装到 `.claude/skills/` 或 `~/.claude/skills/`。

### 手动安装（软链接，不依赖网络/npx）

```bash
git clone https://github.com/tzzs/apple-design-skill.git
ln -s "$(pwd)/apple-design-skill" ~/.claude/skills/apple-design   # 换成你所用 Agent 对应的 skills 目录即可
```

技能通常在会话/Agent 启动时加载，装好之后开一个新会话即可生效。

## 使用方式

安装后，技能会在你讨论 Apple 平台界面设计问题时自动触发，不需要显式点名。比如：

- "彩色渐变背景上的 Liquid Glass Tab bar 该怎么处理？"
- "这个新手引导流程符合苹果规范吗？"
- "状态指示器该用哪种 SF Symbols 渲染模式？"
- "visionOS 上控件的最小点击区域是多大？"

在 Claude Code 里，也可以用 `/apple-design` 显式触发；其他 Agent 各自有自己的技能调用方式。

## 更新

如果是通过 Claude Code 插件安装的：

```bash
cd apple-design-skill
git pull
claude plugin marketplace update tzzs
claude plugin update apple-design@tzzs
```

如果是通过 `npx skills` 安装的（按已安装的技能名更新，不是按仓库地址）：

```bash
npx skills update apple-design
```

## 内容与版权说明

- `references/` 里的内容是对 Apple 官方文档的转述和整理（用自己的话概括，不是逐字复制），每个文件都标注了对应的官方原文 URL，需要精确措辞时可以直接查看原文。
- 具体数值（点数、对比度、命中区域大小等）属于事实性数据而非创作性表达，为保证准确性直接采用了 Apple 文档中的数值——但这些值会随时间调整，涉及精确建议时，请通过 [references/hig-sitemap.md](references/hig-sitemap.md) 里的链接核对官方最新页面。
- 本仓库自身的内容（Markdown 文件、插件清单、以及这份 README）采用 [MIT License](LICENSE) 开源，另有说明的除外；Apple 官方文档本身的版权仍归 Apple Inc. 所有。

## 参与贡献

欢迎提 Issue 和 PR——尤其是发现某个规范在 WWDC 更新后过时了，或者摘要有遗漏的情况。由于 HIG 有 100 多个页面，这个技能刻意只深入覆盖最高频用到的部分，其余内容依赖 [references/hig-sitemap.md](references/hig-sitemap.md) 现查；如果你想按现有结构补充某个缺失主题的摘要文件，非常欢迎提交 PR。
