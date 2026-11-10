"""把规则应用到文本上，得到可解释的评分结果。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .rules import (
    BADGE,
    RULES,
    Rule,
    has_code_block,
    has_section,
    headings,
    intro_text,
    plain_length,
)

GRADE_BOUNDS: tuple[tuple[int, str], ...] = ((90, "A"), (75, "B"), (60, "C"))
PASS_SCORE = 60


@dataclass
class Item:
    rule: Rule
    passed: bool
    detail: str = ""

    @property
    def earned(self) -> int:
        return self.rule.weight if self.passed else 0


def _check_title(text: str) -> tuple[bool, str]:
    found = headings(text)
    if not found:
        return False, "没有找到任何标题"
    level, _ = found[0]
    return (level == 1, "一级标题存在" if level == 1 else "首个标题不是一级标题")


def _check_intro(text: str) -> tuple[bool, str]:
    length = plain_length(intro_text(text))
    return (length >= 20, f"简介 {length} 字（需 ≥20）")


def _check_install(text: str) -> tuple[bool, str]:
    ok = has_section(text, "安装", "install", "getting started", "quick start")
    return (ok, "已找到安装小节" if ok else "缺少安装小节")


def _check_usage(text: str) -> tuple[bool, str]:
    ok = has_section(text, "使用", "usage", "example") and has_code_block(text)
    return (ok, "已有使用说明与代码块" if ok else "缺少使用小节或代码块")


LICENSE_MARKERS = ("LICENSE", "LICENCE", "COPYING")


def _check_license(text: str) -> tuple[bool, str]:
    upper = text.upper()
    has_file = any(marker in upper for marker in LICENSE_MARKERS)
    ok = has_section(text, "许可证", "license", "licence", "许可协议") and has_file
    return (ok, "已声明许可证" if ok else "缺少许可证小节或 LICENSE 链接")


def _check_contributing(text: str) -> tuple[bool, str]:
    ok = has_section(text, "贡献", "contributing")
    return (ok, "已找到贡献指南" if ok else "缺少贡献指南小节")


def _check_badges(text: str) -> tuple[bool, str]:
    count = len(BADGE.findall(text))
    return (count > 0, f"徽章 {count} 个")


def _check_toc(text: str) -> tuple[bool, str]:
    count = sum(1 for level, _ in headings(text) if level == 2)
    ok = has_section(text, "目录", "contents") or count >= 3
    return (ok, f"二级标题 {count} 个（需 ≥3）")


CHECKS = {
    "title": _check_title,
    "intro": _check_intro,
    "install": _check_install,
    "usage": _check_usage,
    "license": _check_license,
    "contributing": _check_contributing,
    "badges": _check_badges,
    "toc": _check_toc,
}


@dataclass
class Report:
    path: Path
    items: list[Item]

    @property
    def total(self) -> int:
        return sum(item.rule.weight for item in self.items)

    @property
    def score(self) -> int:
        return sum(item.earned for item in self.items)

    @property
    def grade(self) -> str:
        for bound, grade in GRADE_BOUNDS:
            if self.score >= bound:
                return grade
        return "D"

    @property
    def passed(self) -> bool:
        return self.score >= PASS_SCORE

    @property
    def failed(self) -> list[Item]:
        return [item for item in self.items if not item.passed]


def analyze(path: Path, text: str | None = None) -> Report:
    if text is None:
        text = path.read_text(encoding="utf-8")
    items = [Item(rule, *CHECKS[rule.key](text)) for rule in RULES]
    return Report(path=path, items=items)
