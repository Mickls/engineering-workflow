#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class Invariant:
    phrase: str
    paths: tuple[str, ...]


INVARIANTS = (
    Invariant(
        "最小正确实现",
        (
            "global/AGENTS.md",
            "README.md",
            "plugins/engineering-workflow/skills/coding-standards/SKILL.md",
            "plugins/engineering-workflow/skills/coding-standards/agents/openai.yaml",
            "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
            "plugins/engineering-workflow/skills/verification-delivery/agents/openai.yaml",
        ),
    ),
    Invariant(
        "required",
        (
            "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
            "plugins/engineering-workflow/skills/requirements-workflow/references/design-template.md",
            "plugins/engineering-workflow/skills/requirements-workflow/agents/openai.yaml",
        ),
    ),
    Invariant(
        "defer-with-trigger",
        (
            "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
            "plugins/engineering-workflow/skills/requirements-workflow/references/design-template.md",
            "plugins/engineering-workflow/skills/requirements-workflow/agents/openai.yaml",
            "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
        ),
    ),
    Invariant(
        "out-of-scope",
        (
            "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
            "plugins/engineering-workflow/skills/requirements-workflow/references/design-template.md",
            "plugins/engineering-workflow/skills/requirements-workflow/agents/openai.yaml",
            "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
        ),
    ),
    Invariant(
        "over-engineering",
        (
            "plugins/engineering-workflow/skills/architecture-review/SKILL.md",
            "plugins/engineering-workflow/skills/architecture-review/agents/openai.yaml",
        ),
    ),
    Invariant(
        "trust boundary validation",
        (
            "global/AGENTS.md",
            "README.md",
            "plugins/engineering-workflow/skills/coding-standards/SKILL.md",
            "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
        ),
    ),
)


def main() -> int:
    errors: list[str] = []
    for invariant in INVARIANTS:
        for rel_path in invariant.paths:
            path = Path(rel_path)
            if not path.is_file():
                errors.append(f"{rel_path}: missing file for invariant {invariant.phrase!r}")
                continue
            text = path.read_text(encoding="utf-8")
            if invariant.phrase not in text:
                errors.append(f"{rel_path}: missing workflow rule invariant {invariant.phrase!r}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(INVARIANTS)} workflow rule invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
