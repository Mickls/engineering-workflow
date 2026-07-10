#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


MAX_GLOBAL_AGENTS_LINES = 100
MAX_GLOBAL_AGENTS_CHARS = 6_000
MAX_SKILL_MD_LINES = 80
MAX_SKILL_MD_CHARS = 3_000
MAX_TOTAL_SKILL_MD_CHARS = 20_000
SPECIAL_SKILL_BUDGETS = {"verification-delivery": (60, 1_800)}
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
TRIGGER_HEADINGS = ("## 何时使用", "## 什么时候使用")
MIN_DUPLICATE_PARAGRAPH_CHARS = 120


def main() -> int:
    skill_root = Path("plugins/engineering-workflow/skills")
    global_agents = Path("global/AGENTS.md")
    errors = validate_workflow(skill_root, global_agents)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skill_root.iterdir() if path.is_dir())
    total_skill_chars = sum(
        len((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        for skill_dir in skill_dirs
    )
    global_chars = len(global_agents.read_text(encoding="utf-8"))
    print(f"validated {len(skill_dirs)} skills")
    print(
        f"context budget: global={global_chars}/{MAX_GLOBAL_AGENTS_CHARS} chars, "
        f"skill entries={total_skill_chars}/{MAX_TOTAL_SKILL_MD_CHARS} chars"
    )
    duplicate_warnings = find_reference_duplicates(skill_root)
    for warning in duplicate_warnings:
        print(f"warning: {warning}")
    print(f"reference overlap candidates: {len(duplicate_warnings)}")
    return 0


def validate_workflow(skill_root: Path, global_agents: Path) -> list[str]:
    errors: list[str] = []
    validate_global_agents(global_agents, errors)

    if not skill_root.is_dir():
        errors.append(f"{skill_root}: missing skill root")
        return errors

    skill_dirs = sorted(path for path in skill_root.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found")
        return errors

    total_skill_chars = 0
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        text = validate_skill(skill_dir, errors)
        if text is not None:
            total_skill_chars += len(text)

    if total_skill_chars > MAX_TOTAL_SKILL_MD_CHARS:
        errors.append(
            f"{skill_root}: SKILL.md files have {total_skill_chars} characters total; "
            f"keep the aggregate at {MAX_TOTAL_SKILL_MD_CHARS} or less"
        )

    return errors


def validate_global_agents(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"{path}: missing global AGENTS file")
        return

    text = path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    if line_count > MAX_GLOBAL_AGENTS_LINES:
        errors.append(
            f"{path}: has {line_count} lines; keep global AGENTS at "
            f"{MAX_GLOBAL_AGENTS_LINES} lines or less"
        )
    if len(text) > MAX_GLOBAL_AGENTS_CHARS:
        errors.append(
            f"{path}: has {len(text)} characters; keep global AGENTS at "
            f"{MAX_GLOBAL_AGENTS_CHARS} characters or less"
        )


def validate_skill(skill_dir: Path, errors: list[str]) -> str | None:
    skill_md = skill_dir / "SKILL.md"
    agent_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.is_file():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return None
    if not agent_yaml.is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")

    text = skill_md.read_text(encoding="utf-8")
    validate_skill_md_size(skill_md, text, errors)
    validate_special_skill_budget(skill_dir.name, skill_md, text, errors)
    validate_trigger_sections(skill_md, text, errors)
    validate_frontmatter(skill_md, text, errors)
    validate_reference_links(skill_dir, skill_md, text, errors)
    return text


def validate_skill_md_size(path: Path, text: str, errors: list[str]) -> None:
    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_MD_LINES:
        errors.append(
            f"{path}: SKILL.md has {line_count} lines; keep entry files at "
            f"{MAX_SKILL_MD_LINES} lines or less and move details to references/"
        )
    if len(text) > MAX_SKILL_MD_CHARS:
        errors.append(
            f"{path}: SKILL.md has {len(text)} characters; keep entry files at "
            f"{MAX_SKILL_MD_CHARS} characters or less"
        )


def validate_special_skill_budget(
    skill_name: str,
    path: Path,
    text: str,
    errors: list[str],
) -> None:
    budget = SPECIAL_SKILL_BUDGETS.get(skill_name)
    if budget is None:
        return

    max_lines, max_chars = budget
    line_count = len(text.splitlines())
    if line_count > max_lines:
        errors.append(
            f"{path}: {skill_name} has {line_count} lines; keep this high-frequency "
            f"entry at {max_lines} lines or less"
        )
    if len(text) > max_chars:
        errors.append(
            f"{path}: {skill_name} has {len(text)} characters; keep this "
            f"high-frequency entry at {max_chars} characters or less"
        )


def validate_trigger_sections(path: Path, text: str, errors: list[str]) -> None:
    for heading in TRIGGER_HEADINGS:
        if re.search(rf"^{re.escape(heading)}\s*$", text, re.M):
            errors.append(
                f"{path}: move trigger guidance from {heading!r} into frontmatter description"
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


def find_reference_duplicates(skill_root: Path) -> list[str]:
    warnings: list[str] = []
    for skill_dir in sorted(path for path in skill_root.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        references_dir = skill_dir / "references"
        if not skill_md.is_file() or not references_dir.is_dir():
            continue

        skill_paragraphs = set(normalized_paragraphs(skill_md.read_text(encoding="utf-8")))
        for reference in sorted(references_dir.glob("*.md")):
            for paragraph in normalized_paragraphs(reference.read_text(encoding="utf-8")):
                if paragraph in skill_paragraphs:
                    preview = paragraph[:80]
                    warnings.append(
                        f"{skill_md} and {reference} repeat a long paragraph: {preview!r}"
                    )
    return warnings


def normalized_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for raw in re.split(r"\n\s*\n", text):
        normalized = " ".join(raw.split())
        if len(normalized) >= MIN_DUPLICATE_PARAGRAPH_CHARS:
            paragraphs.append(normalized)
    return paragraphs


if __name__ == "__main__":
    raise SystemExit(main())
