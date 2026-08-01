# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Warp, etc.) working in this repository.

## What this repo is

A portable agent skill implemented entirely as Markdown, forked from [blader/humanizer](https://github.com/blader/humanizer) and localized for **Chinese** text (中文去 AI 味). The runtime artifact is `SKILL.md`: the agent reads its YAML frontmatter and editor prompt. There is no build step, and the repo should avoid wording that limits support to one or two harnesses.

## Key files

- `SKILL.md` — the skill itself, written in Chinese. Portable YAML frontmatter (`name`, `description`, `license`, `metadata.version`) followed by the canonical, numbered pattern list with before/after examples. **This is the source of truth.**
- `README.md` — for humans (Chinese): installation, usage, differences from the English upstream, a summary table of the patterns, and a version history.
- `.claude-plugin/plugin.json` — optional Claude Code plugin manifest.
- `.claude-plugin/marketplace.json` — optional single-repo marketplace entry so `/plugin marketplace add jiji262/humanizer-chinese` works.
- `scripts/validate-package.py` — dependency-free package and synchronization checks used locally and in CI.

## The maintenance contract

`SKILL.md` and `README.md` must stay in sync. When you change behavior or content:

- **Patterns:** the skill currently defines **36 numbered patterns** (`PATTERN_COUNT` in `scripts/validate-package.py`). If you add, remove, or renumber any, update the README pattern tables, `PATTERN_COUNT`, and every cross-reference in the same change. Keep numbering stable unless you are deliberately renumbering.
- **Version:** `SKILL.md` frontmatter stores the version under `metadata.version`, `README.md` has a "版本历史" section, and `.claude-plugin/plugin.json` has a `version` field. Bump them together so package metadata matches the skill. Keep the skill version under `metadata`; a top-level `version` key is not portable across Agent Skills hosts. (`marketplace.json` intentionally omits a version so `plugin.json` stays the package source of truth.)
- **Compatibility:** keep install and usage language harness-neutral. The skill should work in any agent harness that can load Markdown skill instructions.
- **Validation:** run `python3 scripts/validate-package.py`, `npx skills add . --list`, and `claude plugin validate .` before publishing.
- **Non-obvious fixes:** if you change the prompt to handle a tricky failure mode (a repeated mis-edit, an unexpected tone shift), add a short note to the README version history explaining what was fixed and why.

## Editing SKILL.md

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product. Edit it like a careful instruction document, not code.
- Chinese-specific rules differ from the English upstream on purpose — do not "sync back" upstream rules blindly. Key deliberate divergences: em dash is NOT banned outright (Chinese 破折号 is legitimate punctuation, only overuse/mis-typesetting is flagged, §27); curly quotes are the Chinese standard, not an AI tell (§31); subjectless sentences are idiomatic Chinese, not passive-voice violations (§16).
- The anti-fabrication rule (task rule 3) explicitly forbids inventing first-person anecdotes — baseline testing showed this is the most common failure when de-AI-ifying Chinese text. Keep that wording strong.
- **Word-list provenance:** the Chinese 盯防词 lists are curated (deliberately non-exhaustive) subsets aligned with the maintainer's shared anti-AI lexicon (`jiji262/skills` → `humanizer/lexicon.json`, categories `zh-commercial` / `zh-set-phrase` / `zh-reader-shout` / `zh-no-stance` / `zh-bait`). This repo is intentionally NOT a sync target — it has no runtime engine, so there is no vendored JSON here and none should be added. When editing word lists, avoid silently forking new term categories; strong new terms discovered here should be considered for backfill into that lexicon. `literary-hollow` is deliberately out of scope (task rule 3 exempts fiction).
