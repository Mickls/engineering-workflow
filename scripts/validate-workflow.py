#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


MAX_SKILL_MD_LINES = 100
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}


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
    validate_skill_md_size(skill_md, text, errors)
    validate_frontmatter(skill_md, text, errors)
    validate_reference_links(skill_dir, skill_md, text, errors)


def validate_skill_md_size(path: Path, text: str, errors: list[str]) -> None:
    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_MD_LINES:
        errors.append(
            f"{path}: SKILL.md has {line_count} lines; keep entry files at "
            f"{MAX_SKILL_MD_LINES} lines or less and move details to references/"
        )


def validate_frontmatter(path: Path, text: str, errors: list[str]) -> None:
    if not text.startswith("---\n"):
        errors.append(f"{path}: missing YAML frontmatter")
        return

    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path}: frontmatter not closed")
        return

    frontmatter = text[4:end]
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):", stripped)
        if match and match.group(1) not in ALLOWED_FRONTMATTER_KEYS:
            errors.append(
                f"{path}: frontmatter key {match.group(1)!r} is not allowed; "
                "use only name and description"
            )

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
    linked_references = set()
    for match in re.finditer(r"\]\((references/[^)#]+)", text):
        reference_path = match.group(1)
        linked_references.add(reference_path)
        target = skill_dir / reference_path
        if not target.is_file():
            errors.append(f"{skill_md}: missing referenced file {reference_path}")

    references_dir = skill_dir / "references"
    if not references_dir.is_dir():
        return

    for reference in sorted(references_dir.glob("*.md")):
        reference_path = reference.relative_to(skill_dir).as_posix()
        if reference_path not in linked_references:
            errors.append(
                f"{skill_md}: reference file {reference_path} is not linked "
                "directly from SKILL.md"
            )


if __name__ == "__main__":
    raise SystemExit(main())
