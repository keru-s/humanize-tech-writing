# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

`humanize-tech-writing` is a portable Agent Skill for **Chinese technical writing**. It rewrites project documentation and code comments to remove AI-coined terminology, vague engineering jargon, unnecessary abstraction, translationese, and comments that merely restate code.

This repository is intentionally narrower than its upstream `humanizer-chinese`: it is for README files, design docs, ADR/RFC content, API/configuration docs, JavaDoc/docstrings, and code comments. It is not a general-purpose prose humanizer.

The runtime artifact is `SKILL.md`. There is no build step.

## Product principles

The order of priority is:

1. technical correctness
2. consistency with project terminology
3. concrete and directly understandable language
4. natural Chinese engineering writing
5. brevity

Never improve “human-ness” at the cost of technical precision.

Do not treat all specialized words as AI jargon. Established technical terms and project-specific terms must be preserved when supported by repository context.

## Key files

- `SKILL.md` — source of truth for the skill behavior and 18 rule categories.
- `README.md` — user-facing description, examples, project-level installation, usage, and version history.
- `agents/openai.yaml` — OpenAI Agent Skills display metadata.
- `.claude-plugin/plugin.json` — Claude Code plugin manifest.
- `.claude-plugin/marketplace.json` — Claude Code marketplace entry.
- `scripts/validate-package.py` — dependency-free consistency checks.
- `.github/workflows/validate.yml` — CI validation.

## Maintenance contract

`SKILL.md`, `README.md`, Agent metadata, and plugin metadata must stay in sync.

### Rule count

The skill currently defines **18 numbered rules** (`PATTERN_COUNT` in `scripts/validate-package.py`). If rules are added, removed, or renumbered, update together:

- `SKILL.md`
- README rule table
- `PATTERN_COUNT`
- any cross-references

Keep numbering stable unless the change deliberately restructures the skill.

### Version

The current version must match in:

- `SKILL.md` → `metadata.version`
- `README.md` → latest entry in `版本历史`
- `.claude-plugin/plugin.json` → `version`

Keep version metadata portable; do not add harness-specific frontmatter keys to `SKILL.md` unless the Agent Skills format requires them.

### Naming

The canonical skill/package name is `humanize-tech-writing`.

Do not reintroduce `humanizer-chinese` as the active package name. It may appear only when documenting upstream history or attribution.

### Technical-writing behavior

When changing the skill prompt, preserve these invariants:

- Never invent facts, causes, metrics, constraints, or design intent.
- Preserve identifiers, API fields, protocol names, CLI commands, configuration keys, errors, paths, URLs, and fixed strings unless the user explicitly asks to change them.
- Prefer existing project terminology over generic “plain language”.
- Do not blindly remove established terms such as `幂等`, `回源`, `透传`, `背压`, `熔断`, or `最终一致性` when they are technically accurate.
- Treat words like `失败` as normal Chinese; flag unnecessary constructions such as `失败态` or `失败承接` when they hide the actual behavior.
- Code comments should explain non-obvious reasons, constraints, or behavior, not translate the code line by line.
- Do not add change-history comments where Git history belongs.

### Examples

Examples should be technically plausible but must remain generic. Avoid examples whose “improved” version introduces details that were not present in the original unless the surrounding text explicitly says those details must come from real project context.

### Project-level use

The README documents the recommended Codex layout:

```text
.agents/skills/humanize-tech-writing/SKILL.md
```

It also recommends a small `AGENTS.md` trigger rule so the skill is applied when Chinese technical docs or code comments are created or modified. Keep this distinction clear:

- project instructions decide **when** to apply the skill
- `SKILL.md` decides **how** to edit the text

## Validation

Before publishing, run:

```bash
python3 scripts/validate-package.py
npx skills add . --list
claude plugin validate .
```

If a tool is unavailable locally, CI should still exercise the package checks.

## Upstream attribution

This project is derived from `jiji262/humanizer-chinese`, which in turn builds on `blader/humanizer`. Keep the upstream attribution in `README.md` and preserve the MIT license notice as required by the existing license.
