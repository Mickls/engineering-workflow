from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "check-workflow-rule-sync.py"
SPEC = importlib.util.spec_from_file_location("check_workflow_rule_sync", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CheckWorkflowRuleSyncTest(unittest.TestCase):
    def test_includes_requirements_clarification_invariant(self) -> None:
        invariant = next(
            item
            for item in MODULE.INVARIANTS
            if item.name == "requirements-clarification"
        )
        self.assertEqual(
            1,
            sum(checkpoint.role == "owner" for checkpoint in invariant.checkpoints),
        )
        self.assertTrue(
            any(
                checkpoint.role == "global-fail-safe"
                for checkpoint in invariant.checkpoints
            )
        )

    def test_includes_low_friction_review_invariants(self) -> None:
        expected = {
            "risk-triggered-review",
            "preimplementation-acceptance",
            "behavior-risk-review-packet",
            "prepared-decision-interview",
            "context-ledger-recovery",
            "acceptance-closure-follow-up",
            "resource-aware-validation",
        }
        selected = {
            item.name: item
            for item in MODULE.INVARIANTS
            if item.name in expected
        }
        self.assertEqual(expected, set(selected))
        for invariant in selected.values():
            self.assertEqual(
                1,
                sum(
                    checkpoint.role == "owner"
                    for checkpoint in invariant.checkpoints
                ),
            )
            self.assertTrue(
                any(
                    checkpoint.role == "global-fail-safe"
                    for checkpoint in invariant.checkpoints
                )
            )

    def test_low_friction_invariant_reports_missing_consumer_marker(self) -> None:
        invariant = next(
            item
            for item in MODULE.INVARIANTS
            if item.name == "risk-triggered-review"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            missing_marker = "升级 HITL"
            for checkpoint in invariant.checkpoints:
                path = root / checkpoint.path
                path.parent.mkdir(parents=True, exist_ok=True)
                markers = checkpoint.markers
                if checkpoint.role == "coding-consumer":
                    markers = tuple(
                        marker
                        for marker in markers
                        if marker != missing_marker
                    )
                path.write_text("\n".join(markers), encoding="utf-8")

            errors = MODULE.validate_invariants(root, (invariant,))
            self.assertTrue(
                any(missing_marker in error for error in errors),
                errors,
            )

    def test_decision_efficiency_invariant_covers_duplicate_question_regression(self) -> None:
        invariant = next(
            item
            for item in MODULE.INVARIANTS
            if item.name == "prepared-decision-interview"
        )
        markers = {
            marker
            for checkpoint in invariant.checkpoints
            for marker in checkpoint.markers
        }
        self.assertTrue(
            {"discovery-complete", "semantic_key", "exception evidence"}
            <= markers
        )

    def test_acceptance_closure_requires_follow_up_separation(self) -> None:
        invariant = next(
            item
            for item in MODULE.INVARIANTS
            if item.name == "acceptance-closure-follow-up"
        )
        markers = {
            marker
            for checkpoint in invariant.checkpoints
            for marker in checkpoint.markers
        }
        self.assertIn("completion boundary", markers)
        self.assertIn("建立 follow-up", markers)

    def test_proactive_subagent_rule_does_not_require_per_task_user_prompt(self) -> None:
        invariant = next(
            item
            for item in MODULE.INVARIANTS
            if item.name == "proactive-subagent-orchestration"
        )
        owner = next(
            checkpoint
            for checkpoint in invariant.checkpoints
            if checkpoint.role == "owner"
        )
        self.assertEqual(
            {"owner", "readme-consumer"},
            {checkpoint.role for checkpoint in invariant.checkpoints},
        )
        self.assertIn("必须主动调用 Codex 原生子 agent", owner.markers)
        self.assertIn("无需用户逐次要求", owner.markers)
        self.assertIn("不得静默退化为长时间串行检索", owner.markers)

    def test_validates_owner_and_consumer_roles(self) -> None:
        invariant = MODULE.RuleInvariant(
            "demo",
            (
                MODULE.Checkpoint("owner", "owner.md", ("source rule",)),
                MODULE.Checkpoint("consumer", "consumer.md", ("route",)),
            ),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "owner.md").write_text("source rule", encoding="utf-8")
            (root / "consumer.md").write_text("route", encoding="utf-8")
            self.assertEqual(MODULE.validate_invariants(root, (invariant,)), [])

    def test_reports_missing_owner_role(self) -> None:
        invariant = MODULE.RuleInvariant(
            "demo",
            (MODULE.Checkpoint("consumer", "consumer.md", ("route",)),),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "consumer.md").write_text("route", encoding="utf-8")
            errors = MODULE.validate_invariants(root, (invariant,))
            self.assertTrue(any("exactly one owner" in error for error in errors))

    def test_reports_duplicate_owner_roles(self) -> None:
        invariant = MODULE.RuleInvariant(
            "demo",
            (
                MODULE.Checkpoint("owner", "one.md", ("source",)),
                MODULE.Checkpoint("owner", "two.md", ("source",)),
            ),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "one.md").write_text("source", encoding="utf-8")
            (root / "two.md").write_text("source", encoding="utf-8")
            errors = MODULE.validate_invariants(root, (invariant,))
            self.assertTrue(any("found 2" in error for error in errors))

    def test_reports_missing_checkpoint_marker(self) -> None:
        invariant = MODULE.RuleInvariant(
            "demo",
            (MODULE.Checkpoint("owner", "owner.md", ("source rule",)),),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "owner.md").write_text("wrong", encoding="utf-8")
            errors = MODULE.validate_invariants(root, (invariant,))
            self.assertTrue(any("source rule" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
