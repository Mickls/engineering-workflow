#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


def main() -> int:
    root = Path("plugins/engineering-workflow/skills")
    errors: list[str] = []

    skill_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found")

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(skill_dirs)} skills")
    return 0


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    agent_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.is_file():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return
    if not agent_yaml.is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")

    text = skill_md.read_text(encoding="utf-8")
    validate_frontmatter(skill_md, text, errors)
    validate_reference_links(skill_dir, skill_md, text, errors)


def validate_frontmatter(path: Path, text: str, errors: list[str]) -> None:
    if not text.startswith("---\n"):
        errors.append(f"{path}: missing YAML frontmatter")
        return

    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path}: frontmatter not closed")
        return

    frontmatter = text[4:end]
    if not re.search(r"^name:\s*.+", frontmatter, re.M):
        errors.append(f"{path}: frontmatter missing name")
    if not re.search(r"^description:\s*.+", frontmatter, re.M):
        errors.append(f"{path}: frontmatter missing description")


def validate_reference_links(
    skill_dir: Path,
    skill_md: Path,
    text: str,
    errors: list[str],
) -> None:
    for match in re.finditer(r"\]\((references/[^)#]+)", text):
        target = skill_dir / match.group(1)
        if not target.is_file():
            errors.append(f"{skill_md}: missing referenced file {match.group(1)}")


if __name__ == "__main__":
    raise SystemExit(main())
