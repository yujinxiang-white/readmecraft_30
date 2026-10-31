import unittest

from readmecraft.rules import has_code_block, has_section, headings, intro_text, plain_length


class HeadingsTest(unittest.TestCase):
    def test_collects_levels_in_order(self):
        text = "# 标题\n\n## 安装\n\n### 子步骤\n"
        self.assertEqual(headings(text), [(1, "标题"), (2, "安装"), (3, "子步骤")])

    def test_ignores_hash_lines_inside_code_fence(self):
        text = "# 标题\n\n```bash\n# 这是注释\n```\n"
        self.assertEqual([title for _, title in headings(text)], ["标题"])


class SectionTest(unittest.TestCase):
    def test_matches_chinese_and_english_alias(self):
        self.assertTrue(has_section("## 安装说明\n", "安装", "install"))
        self.assertTrue(has_section("## Getting Started\n", "安装", "getting started"))
        self.assertFalse(has_section("## 联系方式\n", "安装", "install"))


class CodeBlockTest(unittest.TestCase):
    def test_needs_a_closed_pair(self):
        self.assertFalse(has_code_block("```bash\nls\n"))
        self.assertTrue(has_code_block("```bash\nls\n```\n"))


class IntroTest(unittest.TestCase):
    def test_stops_at_second_level_heading(self):
        text = "# 项目\n\n一句话简介。\n\n## 安装\n\n不相关内容\n"
        self.assertEqual(intro_text(text), "一句话简介。")

    def test_plain_length_ignores_links_and_badges(self):
        text = "阅读 [文档](https://example.com) 了解详情"
        self.assertEqual(plain_length(text), len("阅读文档了解详情"))


if __name__ == "__main__":
    unittest.main()
