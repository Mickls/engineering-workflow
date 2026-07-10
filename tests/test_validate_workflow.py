from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate-workflow.py"
SPEC = importlib.util.spec_from_file_location("validate_workflow", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.skill_root = self.root / "skills"
        self.global_agents = self.root / "AGENTS.md"
        self.global_agents.write_text("# Global\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def create_skill(self, name: str, body: str = "# Skill\n") -> Path:
        skill_dir = self.skill_root / name
        (skill_dir / "agents").mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            f'---\nname: {name}\ndescription: "Use for tests."\n---\n\n{body}',
            encoding="utf-8",
        )
        (skill_dir / "agents" / "openai.yaml").write_text(
            'interface:\n  display_name: "Test"\n  short_description: "Test skill metadata"\n  default_prompt: "Use $test-skill for tests."\n',
            encoding="utf-8",
        )
        return skill_dir

    def test_accepts_content_within_budgets(self) -> None:
        self.create_skill("test-skill")
        self.assertEqual(
            MODULE.validate_workflow(self.skill_root, self.global_agents), []
        )

    def test_rejects_oversized_global_agents(self) -> None:
        self.create_skill("test-skill")
        self.global_agents.write_text(
            "x" * (MODULE.MAX_GLOBAL_AGENTS_CHARS + 1), encoding="utf-8"
        )
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("global AGENTS" in error for error in errors))

    def test_rejects_oversized_skill_entry(self) -> None:
        self.create_skill("test-skill", "x" * (MODULE.MAX_SKILL_MD_CHARS + 1))
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("characters" in error for error in errors))

    def test_rejects_trigger_heading_in_body(self) -> None:
        self.create_skill("test-skill", "# Skill\n\n## 何时使用\n\n- always\n")
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("frontmatter description" in error for error in errors))

    def test_reports_long_paragraph_repeated_in_reference(self) -> None:
        paragraph = "Repeated guidance " * 12
        skill_dir = self.create_skill(
            "test-skill",
            f"# Skill\n\n{paragraph}\n\nSee [detail](references/detail.md).\n",
        )
        references = skill_dir / "references"
        references.mkdir()
        (references / "detail.md").write_text(paragraph, encoding="utf-8")
        warnings = MODULE.find_reference_duplicates(self.skill_root)
        self.assertEqual(1, len(warnings))

    def test_enforces_verification_delivery_specific_budget(self) -> None:
        body = "# Skill\n" + "line\n" * 57
        self.create_skill("verification-delivery", body)
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("high-frequency entry" in error for error in errors))

    def test_enforces_verification_delivery_character_budget(self) -> None:
        self.create_skill("verification-delivery", "x" * 1_900)
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("high-frequency entry" in error for error in errors))

    def test_rejects_aggregate_skill_budget(self) -> None:
        for index in range(8):
            self.create_skill(f"test-skill-{index}", "x" * 2_450)
        errors = MODULE.validate_workflow(self.skill_root, self.global_agents)
        self.assertTrue(any("characters total" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
