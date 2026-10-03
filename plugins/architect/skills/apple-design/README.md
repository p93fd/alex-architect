# apple-design

**English** | [简体中文](README.zh-CN.md)

A portable [Agent Skill](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) that turns Apple's official [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) into ready-to-use reference material for designing and reviewing user interfaces on iOS, iPadOS, macOS, watchOS, and visionOS (with tvOS notes where relevant). It's just a `SKILL.md` plus supporting reference files, so it works with [Claude Code](https://claude.com/claude-code) (as a native plugin) and with any other coding agent that supports the Agent Skills format — Codex, Cursor, OpenCode, and others — via [skills.sh](https://skills.sh).

> This is an independent, community-maintained project. It is not affiliated with, endorsed by, or sponsored by Apple Inc. "Apple," "iOS," "macOS," and the other platform/technology names used here are trademarks of Apple Inc., used only to describe the subject matter of this content.

## Why this exists

Apple's design guidance shifts almost every year around WWDC — most notably the 2025 introduction of the **Liquid Glass** design language, which rebuilt materials, icons, and control appearance across iOS/iPadOS/macOS. An LLM's training data can easily be stale or mix up specs across platforms. This skill gives Claude a curated, paraphrased, cross-linked summary of the HIG's most load-bearing content, plus a full sitemap of official URLs to fetch live when a precise number, component name, or the latest wording is needed — so answers stay grounded instead of guessed.

## What's inside

```
apple-design/
├── SKILL.md                          # Entry point: triggers, navigation, quick references
├── .claude-plugin/
│   ├── plugin.json                   # Plugin manifest (name: apple-design)
│   └── marketplace.json              # Marketplace manifest (name: tzzs)
└── references/
    ├── principles.md                 # The eight design principles
    ├── platforms.md                  # iOS / iPadOS / macOS / watchOS / visionOS characteristics
    ├── materials-color.md            # Materials, Liquid Glass, Color system
    ├── typography-symbols.md         # Fonts, Dynamic Type, SF Symbols
    ├── layout.md                     # Visual hierarchy, size classes, safe areas
    ├── accessibility.md              # Vision / hearing / mobility / speech / cognitive
    ├── components.md                 # Buttons, Tab bars, Sidebars, Lists, Toolbars
    ├── app-icons.md                  # Layered icon design, Icon Composer
    ├── patterns-gestures.md          # Gesture design and common interaction patterns
    ├── resources.md                  # Official UI Kits, fonts, SF Symbols, Icon Composer
    └── hig-sitemap.md                # Full HIG URL index for live lookups
```

The content follows a progressive-disclosure structure: `SKILL.md` stays short and routes to the right `references/*.md` file for the topic at hand, and `hig-sitemap.md` gives Claude the exact URL to fetch live whenever a summary isn't enough.

## Install

### Claude Code (native plugin, recommended for Claude Code)

```bash
claude plugin marketplace add tzzs/apple-design-skill
claude plugin install apple-design@tzzs
```

Verify it's active:

```bash
claude plugin list
```

### Any other agent (Codex, Cursor, OpenCode, and 70+ more) via skills.sh

[skills.sh](https://skills.sh) is a package-manager-style catalog for Agent Skills, backed by the open-source [`npx skills`](https://github.com/vercel-labs/skills) CLI. Since this repo's `SKILL.md` sits at the repository root, the CLI picks it up automatically — no extra path needed:

```bash
npx skills add tzzs/apple-design-skill
```

The CLI detects installed agents and prompts you to pick one or more; to skip the prompt, target agents explicitly:

```bash
# Install for Codex and Cursor only, non-interactively
npx skills add tzzs/apple-design-skill -a codex -a cursor -y

# Install once, globally, for every agent skills.sh knows how to configure
npx skills add tzzs/apple-design-skill -g --all
```

Check what's installed:

```bash
npx skills list
```

This also works for Claude Code itself (it installs into `.claude/skills/` or `~/.claude/skills/`) if you'd rather manage it alongside your other agents' skills instead of through the native plugin system above.

### Manual install (symlink, no network/npx required)

```bash
git clone https://github.com/tzzs/apple-design-skill.git
ln -s "$(pwd)/apple-design-skill" ~/.claude/skills/apple-design   # or the equivalent skills/ directory for your agent
```

Skills usually load at session/agent start, so start a new session afterward.

## Usage

Once installed, the skill triggers automatically on Apple-platform UI design questions — you don't need to name it explicitly. For example:

- "How should I handle a Liquid Glass tab bar over a colorful gradient background?"
- "Does this onboarding flow follow Apple's guidelines?"
- "Which SF Symbol rendering mode should I use for a status indicator?"
- "What's the minimum tap target size on visionOS?"

In Claude Code, you can also invoke it directly with `/apple-design`; other agents follow their own skill-invocation conventions.

## Updating

If you installed it as a Claude Code plugin:

```bash
cd apple-design-skill
git pull
claude plugin marketplace update tzzs
claude plugin update apple-design@tzzs
```

If you installed it via `npx skills` (this updates by installed skill name, not repo source):

```bash
npx skills update apple-design
```

## Content and licensing notes

- The prose in `references/` paraphrases and summarizes Apple's official documentation in the authors' own words — it is not a verbatim copy, and each file cites its official source URL for anyone who needs exact wording.
- Numeric specs (point sizes, contrast ratios, hit target sizes, etc.) are facts, not creative expression, and are reproduced directly from Apple's documentation for accuracy — but they change over time, so always spot-check precision-critical values against the live HIG page linked from [references/hig-sitemap.md](references/hig-sitemap.md).
- This repository's own content (the Markdown files, manifests, and this README) is offered under the [MIT License](LICENSE) unless noted otherwise. Apple's underlying documentation remains Apple's copyright.

## Contributing

Issues and pull requests are welcome — especially reports of stale specs after a WWDC update, or gaps in coverage. Since the HIG has 100+ pages, this skill intentionally covers the most frequently needed ones in depth and relies on [references/hig-sitemap.md](references/hig-sitemap.md) for everything else; PRs that add a missing summary file following the existing structure are appreciated.
