#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class Checkpoint:
    role: str
    path: str
    markers: tuple[str, ...]


@dataclass(frozen=True)
class RuleInvariant:
    name: str
    checkpoints: tuple[Checkpoint, ...]


INVARIANTS = (
    RuleInvariant(
        "requirements-clarification",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-interview.md",
                ("唯一 owner", "动态设计树", "反向遗漏检查", "informed override"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
                ("设计前澄清门禁", "clarification-interview.md", "clarification-template.md"),
            ),
            Checkpoint(
                "artifact-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-template.md",
                ("awaiting-clarification-approval", "澄清核销总结"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("澄清核销总结", "不推断批准"),
            ),
        ),
    ),
    RuleInvariant(
        "requirements-design-confirmation",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/requirements-workflow/references/confirmation-and-change-gates.md",
                ("Design / Plan 批准", "设计批准前不得", "后续用户消息"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
                ("confirmation-and-change-gates.md",),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("design/plan 只能写", "后续明确确认"),
            ),
        ),
    ),
    RuleInvariant(
        "scope-classification",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/requirements-workflow/references/scope-and-overimplementation.md",
                ("required", "defer-with-trigger", "out-of-scope"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
                ("scope-and-overimplementation.md",),
            ),
            Checkpoint(
                "template-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/design-template.md",
                ("required / defer-with-trigger / out-of-scope",),
            ),
        ),
    ),
    RuleInvariant(
        "minimal-correct-implementation",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/coding-standards/references/minimal-correct-implementation.md",
                ("最小正确实现", "trust boundary validation"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/coding-standards/SKILL.md",
                ("minimal-correct-implementation.md",),
            ),
            Checkpoint("global-fail-safe", "global/AGENTS.md", ("最小正确实现",)),
            Checkpoint(
                "delivery-consumer",
                "plugins/engineering-workflow/skills/verification-delivery/references/delivery-checklists.md",
                ("最小正确实现",),
            ),
        ),
    ),
    RuleInvariant(
        "implementation-path",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/coding-standards/references/context-and-coverage.md",
                ("DI/provider", "generated code", "blocked"),
            ),
            Checkpoint(
                "coding-route",
                "plugins/engineering-workflow/skills/coding-standards/SKILL.md",
                ("context-and-coverage.md",),
            ),
            Checkpoint(
                "delivery-consumer",
                "plugins/engineering-workflow/skills/verification-delivery/references/delivery-checklists.md",
                ("DI/provider", "generated code", "manual-only"),
            ),
            Checkpoint("global-fail-safe", "global/AGENTS.md", ("DI/provider", "manual-only")),
        ),
    ),
    RuleInvariant(
        "real-entry-testing",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/testing-policy/references/test-entry-and-value.md",
                ("真实入口", "稳定 public contract"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/testing-policy/SKILL.md",
                ("test-entry-and-value.md",),
            ),
            Checkpoint("global-fail-safe", "global/AGENTS.md", ("稳定 public contract",)),
        ),
    ),
    RuleInvariant(
        "incident-evidence",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/incident-debugging/SKILL.md",
                ("真实入口", "同一条复现流程", "不能说“已修复”"),
            ),
            Checkpoint("global-fail-safe", "global/AGENTS.md", ("生产事故", "证明根因")),
        ),
    ),
    RuleInvariant(
        "completion-claims",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
                ("重新运行相关命令", "退出状态"),
            ),
            Checkpoint(
                "special-cases",
                "plugins/engineering-workflow/skills/verification-delivery/references/completion-claims.md",
                ("同路径验证", "剩余风险"),
            ),
            Checkpoint("global-fail-safe", "global/AGENTS.md", ("刚运行", "未验证项")),
        ),
    ),
    RuleInvariant(
        "over-engineering-review",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/architecture-review/SKILL.md",
                ("over-engineering", "不默认修改生产代码"),
            ),
            Checkpoint(
                "report-consumer",
                "plugins/engineering-workflow/skills/architecture-review/references/report-template.md",
                ("推荐强度", "风险"),
            ),
        ),
    ),
    RuleInvariant(
        "context-readiness-reuse",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/project-setup/references/refresh-rules.md",
                ("同一任务内复用", "不等于 stale", "watch_patterns"),
            ),
            Checkpoint(
                "project-setup-route",
                "plugins/engineering-workflow/skills/project-setup/SKILL.md",
                ("readiness 证据", "refresh-rules.md"),
            ),
            Checkpoint(
                "requirements-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/context-readiness.md",
                ("复用该证据",),
            ),
            Checkpoint(
                "coding-consumer",
                "plugins/engineering-workflow/skills/coding-standards/references/context-and-coverage.md",
                ("readiness evidence", "不重复 refresh"),
            ),
            Checkpoint(
                "testing-consumer",
                "plugins/engineering-workflow/skills/testing-policy/SKILL.md",
                ("readiness evidence", "复用"),
            ),
            Checkpoint(
                "delivery-consumer",
                "plugins/engineering-workflow/skills/verification-delivery/references/delivery-checklists.md",
                ("readiness evidence", "不重复 refresh"),
            ),
        ),
    ),
)


def validate_invariants(
    root: Path = Path("."),
    invariants: tuple[RuleInvariant, ...] = INVARIANTS,
) -> list[str]:
    errors: list[str] = []
    for invariant in invariants:
        owner_count = sum(
            1 for checkpoint in invariant.checkpoints if checkpoint.role == "owner"
        )
        if owner_count != 1:
            errors.append(
                f"invariant {invariant.name!r}: expected exactly one owner, found {owner_count}"
            )
        for checkpoint in invariant.checkpoints:
            path = root / checkpoint.path
            if not path.is_file():
                errors.append(
                    f"{checkpoint.path}: missing {checkpoint.role} for invariant {invariant.name!r}"
                )
                continue
            text = path.read_text(encoding="utf-8")
            for marker in checkpoint.markers:
                if marker not in text:
                    errors.append(
                        f"{checkpoint.path}: {checkpoint.role} for invariant "
                        f"{invariant.name!r} is missing marker {marker!r}"
                    )

    return errors


def main() -> int:
    errors = validate_invariants()

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(INVARIANTS)} workflow rule ownership invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
