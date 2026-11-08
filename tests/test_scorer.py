import unittest
from pathlib import Path

from readmecraft.scorer import PASS_SCORE, analyze

ROOT = Path(__file__).resolve().parent.parent


def load(name: str) -> str:
    return (ROOT / "examples" / name).read_text(encoding="utf-8")


class ScoreTest(unittest.TestCase):
    def test_full_readme_scores_high(self):
        report = analyze(Path("examples/README.good.md"), load("README.good.md"))
        self.assertGreaterEqual(report.score, 90)
        self.assertEqual(report.grade, "A")
        self.assertTrue(report.passed)

    def test_bad_readme_is_blocked(self):
        report = analyze(Path("examples/README.bad.md"), load("README.bad.md"))
        self.assertLess(report.score, PASS_SCORE)
        self.assertFalse(report.passed)
        keys = {item.rule.key for item in report.failed}
        self.assertIn("install", keys)
        self.assertIn("license", keys)

    def test_weights_sum_to_one_hundred(self):
        report = analyze(Path("README.md"), load("README.good.md"))
        self.assertEqual(report.total, 100)

    def test_score_equals_sum_of_passed_weights(self):
        report = analyze(Path("examples/README.bad.md"), load("README.bad.md"))
        expected = sum(item.rule.weight for item in report.items if item.passed)
        self.assertEqual(report.score, expected)

    def test_copying_file_counts_as_license(self):
        text = "# demo\n\n一句足够长的项目简介，用来通过长度检查。\n\n## License\n\n见 COPYING 文件。\n"
        report = analyze(Path("COPYING.md"), text)
        license_item = next(item for item in report.items if item.rule.key == "license")
        self.assertTrue(license_item.passed)

if __name__ == "__main__":
    unittest.main()
