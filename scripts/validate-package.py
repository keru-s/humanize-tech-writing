#!/usr/bin/env python3
"""Validate Humanize Tech Writing repository consistency without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()
README = (ROOT / "README.md").read_text()
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
MARKETPLACE = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
OPENAI = (ROOT / "agents" / "openai.yaml").read_text()

CANONICAL_NAME = "humanize-tech-writing"


def require(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


frontmatter = require(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must start with YAML frontmatter",
).group(1)

skill_name = require(
    re.search(r"(?m)^name:\s*([^\s]+)\s*$", frontmatter),
    "SKILL.md name is missing",
).group(1)
if skill_name != CANONICAL_NAME:
    raise SystemExit(f"Expected skill name {CANONICAL_NAME!r}, found {skill_name!r}")

skill_version = require(
    re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter),
    "SKILL.md metadata.version is missing",
).group(1)
readme_version = require(
    re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", README),
    "README version history is missing",
).group(1)

versions = {skill_version, readme_version, str(PLUGIN.get("version", ""))}
if len(versions) != 1:
    raise SystemExit(f"Version mismatch: {sorted(versions)}")

if PLUGIN.get("name") != CANONICAL_NAME:
    raise SystemExit("plugin.json name does not match the canonical skill name")

if MARKETPLACE.get("name") != CANONICAL_NAME:
    raise SystemExit("marketplace.json name does not match the canonical skill name")

plugins = MARKETPLACE.get("plugins", [])
if len(plugins) != 1 or plugins[0].get("name") != CANONICAL_NAME:
    raise SystemExit("marketplace plugin entry does not match the canonical skill name")

if f"${CANONICAL_NAME}" not in OPENAI:
    raise SystemExit("agents/openai.yaml default prompt must reference the canonical skill name")

if len(SKILL.splitlines()) > 300:
    raise SystemExit("SKILL.md exceeds the 300-line prompt budget")

print(f"Humanize Tech Writing package v{skill_version} is internally consistent")
