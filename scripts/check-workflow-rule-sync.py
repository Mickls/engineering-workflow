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
                (
                    "唯一 owner",
                    "动态设计树",
                    "问题准入和地图",
                    "ready-for-decision",
                    "反向遗漏检查",
                    "informed override",
                ),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/requirements-workflow/SKILL.md",
                ("设计前澄清门禁", "clarification-interview.md", "clarification-template.md"),
            ),
            Checkpoint(
                "artifact-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-template.md",
                ("awaiting-clarification-approval", "问题地图", "active question", "澄清核销总结"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("breadth discovery", "decision ledger", "用户纠错先审计全部依赖"),
            ),
        ),
    ),
    RuleInvariant(
        "prepared-decision-interview",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-interview.md",
                (
                    "Discovery / Interview 分离",
                    "discovery-complete",
                    "semantic_key",
                    "exception evidence",
                    "Interaction Budget",
                ),
            ),
            Checkpoint(
                "checklist-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-checklist.md",
                ("breadth discovery", "semantic_key", "dependents", "interaction budget"),
            ),
            Checkpoint(
                "artifact-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/clarification-template.md",
                ("discovery 状态", "Decision Ledger", "exception evidence", "delegated/recommended-default"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("discovery-complete", "新问题先去重", "推荐代理"),
            ),
        ),
    ),
    RuleInvariant(
        "risk-triggered-review",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/issue-slicing/references/execution-review-boundaries.md",
                ("唯一 owner", "AFK 准入", "HITL 触发", "interaction budget", "Review Mode Reset"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/issue-slicing/SKILL.md",
                ("execution-review-boundaries.md", "AFK", "HITL"),
            ),
            Checkpoint(
                "coding-consumer",
                "plugins/engineering-workflow/skills/coding-standards/references/review-checklist.md",
                ("相邻实现", "review budget", "升级 HITL"),
            ),
            Checkpoint(
                "plan-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/plan-template.md",
                ("执行和 Review 边界", "interaction budget", "恢复 AFK 条件"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("AFK 是批准后默认模式", "升级 HITL", "恢复条件"),
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
                ("design/plan 只能写", "按总结设计并实现", "已批准范围内"),
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
        "preimplementation-acceptance",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/testing-policy/references/test-entry-and-value.md",
                ("编码前验收场景", "不能先实现", "关键副作用"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/testing-policy/SKILL.md",
                ("编码前先确定验收场景", "不根据实现反向定义期望"),
            ),
            Checkpoint(
                "design-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/design-template.md",
                ("编码前验收场景", "关键副作用 / 失败行为"),
            ),
            Checkpoint(
                "coverage-consumer",
                "plugins/engineering-workflow/skills/testing-policy/references/coverage-matrix.md",
                ("验收场景", "反向补写"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("行为切片编码前确定", "用户可见结果", "关键副作用"),
            ),
        ),
    ),
    RuleInvariant(
        "resource-aware-validation",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/testing-policy/references/test-entry-and-value.md",
                ("资源、隔离和重跑预算", "缓存目录", "历史残留", "自然里程碑"),
            ),
            Checkpoint(
                "plan-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/plan-template.md",
                ("大资源测试的集中里程碑",),
            ),
            Checkpoint(
                "coding-consumer",
                "plugins/engineering-workflow/skills/coding-standards/references/review-checklist.md",
                ("resource budget", "高成本验证"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("缓存和资源预算", "自然里程碑"),
            ),
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
        "behavior-risk-review-packet",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/verification-delivery/references/review-packets.md",
                ("唯一 owner", "用户 Review 区", "方案偏离", "最多三个"),
            ),
            Checkpoint(
                "route",
                "plugins/engineering-workflow/skills/verification-delivery/SKILL.md",
                ("review-packets.md", "行为", "剩余风险"),
            ),
            Checkpoint(
                "delivery-consumer",
                "plugins/engineering-workflow/skills/verification-delivery/references/delivery-checklists.md",
                ("用户 Review 包", "最多三个用户 review 项"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("方案偏离", "最多列三个", "技术细节随后提供"),
            ),
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
    RuleInvariant(
        "context-ledger-recovery",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/project-setup/references/refresh-rules.md",
                ("上下文压缩", "decision ledger", "禁止重新做全仓", "集中 targeted refresh"),
            ),
            Checkpoint(
                "handoff-consumer",
                "plugins/engineering-workflow/skills/engineering-handoff/references/handoff-template.md",
                ("决定与证据账本", "source commit", "证据失效条件"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("上下文压缩", "source_commit", "不全量重搜"),
            ),
        ),
    ),
    RuleInvariant(
        "proactive-subagent-orchestration",
        (
            Checkpoint(
                "owner",
                "global/AGENTS.md",
                (
                    "必须主动调用 Codex 原生子 agent",
                    "无需用户逐次要求",
                    "降低频繁上下文压缩",
                    "不得静默退化为长时间串行检索",
                ),
            ),
            Checkpoint(
                "readme-consumer",
                "README.md",
                ("主动子 agent 并行", "主上下文卸载", "频繁上下文压缩"),
            ),
        ),
    ),
    RuleInvariant(
        "acceptance-closure-follow-up",
        (
            Checkpoint(
                "owner",
                "plugins/engineering-workflow/skills/requirements-workflow/references/scope-and-overimplementation.md",
                ("验收冻结和 Follow-up", "completion boundary", "必须关闭并交付"),
            ),
            Checkpoint(
                "issue-consumer",
                "plugins/engineering-workflow/skills/requirements-workflow/references/issue-structure.md",
                ("创建独立 follow-up", "完成定义"),
            ),
            Checkpoint(
                "delivery-consumer",
                "plugins/engineering-workflow/skills/verification-delivery/references/delivery-checklists.md",
                ("完成边界和 Follow-up", "当前需求关闭"),
            ),
            Checkpoint(
                "global-fail-safe",
                "global/AGENTS.md",
                ("验收场景通过后立即交付", "建立 follow-up"),
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
