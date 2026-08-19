import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_skill_contract.py"


class SkillContractValidatorTest(unittest.TestCase):
    def run_validator(self, skill_root: Path) -> subprocess.CompletedProcess[str]:
        self.assertTrue(VALIDATOR.exists(), "contract validator must be implemented")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(skill_root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def copy_skill(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        copied_root = Path(temp_dir.name) / "qifu-list-page"
        shutil.copytree(SKILL_ROOT, copied_root)
        return temp_dir, copied_root

    def test_published_skill_satisfies_executable_contract(self) -> None:
        result = self.run_validator(SKILL_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_invocation_contract_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        (copied_root / "references" / "component-invocation-contract.md").unlink()

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("component-invocation-contract.md", result.stdout)

    def test_missing_failure_closed_rule_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        skill_file = copied_root / "SKILL.md"
        skill_text = skill_file.read_text(encoding="utf-8")
        start = skill_text.index("## 失败关闭")
        end = skill_text.index("\n## ", start + 4)
        skill_file.write_text(skill_text[:start] + skill_text[end + 1 :], encoding="utf-8")

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("失败关闭", result.stdout)

    def test_missing_platform_navigation_contract_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        (copied_root / "references" / "platform-yushu.md").unlink()

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("platform-yushu.md", result.stdout)

    def test_missing_custom_navigation_mode_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        platform_file = copied_root / "references" / "platform-yushu.md"
        platform_text = platform_file.read_text(encoding="utf-8")
        platform_file.write_text(
            platform_text.replace("navigationMode=yushuPreset|custom", ""),
            encoding="utf-8",
        )

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("navigationMode=yushuPreset|custom", result.stdout)

    def test_missing_list_action_placement_contract_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        rules_file = copied_root / "references" / "page-rules.md"
        rules_text = rules_file.read_text(encoding="utf-8")
        rules_file.write_text(
            rules_text.replace(
                "primaryAction.placement=listActions.left|listActions.right", ""
            ),
            encoding="utf-8",
        )

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("primaryAction.placement", result.stdout)

    def test_missing_table_column_limit_is_rejected(self) -> None:
        temp_dir, copied_root = self.copy_skill()
        self.addCleanup(temp_dir.cleanup)
        rules_file = copied_root / "references" / "page-rules.md"
        rules_text = rules_file.read_text(encoding="utf-8")
        rules_file.write_text(
            rules_text.replace("最多 8 个业务列", ""),
            encoding="utf-8",
        )

        result = self.run_validator(copied_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("最多 8 个业务列", result.stdout)


if __name__ == "__main__":
    unittest.main()
