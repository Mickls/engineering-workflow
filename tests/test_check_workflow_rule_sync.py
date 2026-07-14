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
