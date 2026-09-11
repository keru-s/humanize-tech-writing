# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

`humanize-tech-writing` is a portable Agent Skill for **Chinese technical writing**. It edits project documentation and code comments to remove AI-coined terminology, vague abstraction, translationese, canned AI phrasing, metaphor-heavy packaging, and low-value comments while preserving technical meaning.

The repository is intentionally narrower than upstream `humanizer-chinese`. It is designed for engineering artifacts such as README files, design docs, ADR/RFC content, API and documentation comments, API/configuration docs, inline/block comments, and change-oriented technical docs.

The runtime Skill package lives under `skills/humanize-tech-writing/`. There is no build step.

## Product priorities

Preserve this order of priority when editing the Skill:

1. technical meaning and factual correctness
2. project terminology and contracts
3. modality, uncertainty, and boundary conditions
4. clarity and concreteness
5. natural, concise technical writing

Style improvements must not weaken the first three items.

## Key files

- `skills/humanize-tech-writing/SKILL.md` — source of truth for Skill behavior.
- `skills/humanize-tech-writing/agents/openai.yaml` — OpenAI Agent Skills display metadata bundled with the Skill.
- `README.md` — user-facing scope, examples, installation, usage, and version history.
- `.claude-plugin/plugin.json` — Claude Code plugin manifest.
- `.claude-plugin/marketplace.json` — Claude Code marketplace entry.
- `scripts/validate-package.py` — dependency-free repository consistency checks.
- `.github/workflows/validate.yml` — CI validation.

## Maintenance contract

`skills/humanize-tech-writing/SKILL.md`, `README.md`, Agent metadata, and plugin metadata must stay consistent.

### Version

The current version must match in:

- `skills/humanize-tech-writing/SKILL.md` → `metadata.version`
- `README.md` → newest entry in `版本历史`
- `.claude-plugin/plugin.json` → `version`

Do not create a maintenance contract around a fixed number of writing rules. The Skill should be organized for model comprehension, not for preserving a taxonomy inherited from upstream.

### Naming

The canonical Skill/package name is `humanize-tech-writing`.

`humanizer-chinese` may appear only in upstream history or attribution. Do not reintroduce it as the active package name.

## Behavioral invariants

When changing the prompt, preserve these rules.

### Evidence before specificity

Concrete implementation details must come from the text being edited or project evidence such as code, tests, API/schema definitions, docs, ADR/RFC content, issues, PR context, or explicit user input.

Never make an abstract sentence look better by inventing a plausible retry count, error code, trigger, metric, design rationale, compatibility claim, or other behavior.

Examples in `SKILL.md` and `README.md` must follow the same rule. An “after” example must not silently add facts that were absent from the “before” example.

### Preserve semantics

Do not change identifiers, API fields, protocol names, CLI commands, configuration keys, errors, paths, URLs, fixed strings, or other program semantics unless the user explicitly asks.

Preserve modality and uncertainty, including distinctions such as:

- MUST / SHOULD / MAY
- 必须 / 应该 / 可以 / 可能 / 不得
- always / sometimes / never

Do not strengthen or weaken a requirement merely to make prose smoother.

### Preserve established terminology

A suffix, word shape, or metaphorical origin is never enough evidence that a term should be removed. Terms such as `幂等性`, `可观测性`, `序列化`, `复杂度`, `调用链路`, `回源`, `背压`, `熔断`, `心跳`, and `冷启动` may be correct engineering language.

Prefer terminology in this order:

1. explicit user terminology
2. repository glossary/instructions/design docs
3. stable terms in code and interfaces
4. established industry terminology in the current language
5. plain Chinese

The existence of an English term is not, by itself, evidence that a literal Chinese translation should be preserved. A translated expression such as `配置漂移` should still be evaluated unless the project explicitly adopts it or the Chinese usage is genuinely stable and precise.

### Prefer literal technical facts over decorative metaphors

Technical writing should make the real objects, actions, states, and relationships easy to recover without an extra decoding step.

Do not use a hard “metaphor count” threshold. Instead ask whether a reader must translate rhetoric back into literal technical meaning before they can understand the sentence.

Preserve established project and industry terms even if they originated as metaphors. For non-standard expressions, prefer literal wording when the metaphor adds only drama, compression, or a sense of sophistication. Pay particular attention to rhetorical imagery, promotional wording, compressed labels, and stacked metaphors that obscure the actual actor, action, causality, or boundary.

When expanding a compressed label, use only behavior supported by the surrounding text or project evidence. Never invent the literal implementation just to remove a metaphor.

### Document-type awareness

Do not apply one comment rule to every technical artifact.

- README / ADR / RFC / design docs: behavior, constraints, decisions, trade-offs, supported rationale.
- API or documentation comments: public contract, parameters, returns, exceptions, nullability, units, side effects, thread-safety, blocking, ordering, lifecycle, and boundaries as needed. This includes JavaDoc, docstrings, JSDoc/TSDoc, KDoc, Rust doc comments, Go declaration comments, C# XML docs, and equivalent forms in other languages.
- Inline / block comments: non-obvious constraints, invariants, compatibility, concurrency/ordering, supported rationale, workaround conditions.
- PR / changelog / migration docs: change history is expected and useful.

“Comments should explain why” is mainly a heuristic for inline comments. Never invent a reason to satisfy that heuristic.

### Minimal editing

The Skill is intended to run repeatedly in coding agents. Avoid diff noise:

- edit only text with a real clarity/style problem
- keep nearby correct prose unchanged
- preserve repository templates and unrelated structure
- do not rename the same technical object for variety

## Prompt design

Keep `skills/humanize-tech-writing/SKILL.md` compact enough that the model can identify the important rules quickly. Prefer a small number of clear sections such as:

1. scope
2. priority
3. hard constraints
4. document-type rules
5. editing preferences
6. project workflow
7. final check

Do not recreate long pattern taxonomies or low-value word lists unless they demonstrably improve behavior.

Keep few-shot examples sparse and representative. Prefer one or two examples for a behavior class, then state the general rule. Do not enumerate every observed bad phrase as an example; that encourages lexical substitution instead of semantic judgment.

Style guidance should remain preference-level where appropriate. For example, active voice, main-point-first structure, list usage, and metaphor reduction can improve technical writing, but existing ADR/RFC templates, established terminology, or domain conventions may take precedence.

## Project-level use

For a consuming repository, keep the `AGENTS.md` trigger short. It decides **when** to invoke this Skill; `SKILL.md` contains **how** to edit.

Recommended snippet:

```md
## Technical writing

When creating or modifying Chinese technical documentation or code comments,
including API/documentation comments, use the `humanize-tech-writing` skill before finishing.

Preserve technical meaning, identifiers, literals, and established project terminology.
```

Recommended Codex layout after installation:

```text
.agents/skills/humanize-tech-writing/SKILL.md
```

## Validation

The local validator checks repository-owned consistency only. Do not hard-code a custom blacklist of Agent Skills frontmatter keys; format/schema validity belongs to the relevant Agent Skills or harness validator.

Before publishing, run:

```bash
python3 scripts/validate-package.py
npx skills add . --list
claude plugin validate .
```

`npx skills add . --list` should discover `skills/humanize-tech-writing/SKILL.md` as the installable Skill rather than treating the repository root as the Skill package.

## Upstream attribution

This project is derived from `jiji262/humanizer-chinese`, which in turn builds on `blader/humanizer`. Keep upstream attribution in `README.md` and preserve the existing MIT license notice.