"""终端输出：把评分结果渲染成宽度对齐的表格（支持中文，可选颜色）。"""

from __future__ import annotations

import sys
from unicodedata import east_asian_width

from . import __version__
from .scorer import Report

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

RULE_WIDTH = 14
DETAIL_WIDTH = 34
LINE_WIDTH = 60


def text_width(value: str) -> int:
    return sum(2 if east_asian_width(char) in "WF" else 1 for char in value)


def pad(value: str, width: int, align: str = "left") -> str:
    space = max(0, width - text_width(value))
    if align == "right":
        return " " * space + value
    return value + " " * space


def symbols() -> tuple[str, str, str, str]:
    """按当前控制台编码挑选符号，Windows 的 GBK 终端下退回 ASCII。"""
    encoding = getattr(getattr(sys, "stdout", None), "encoding", None) or "utf-8"
    try:
        "✓✗─…".encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return "v", "x", "-", "..."
    return "✓", "✗", "─", "…"


def clip(value: str, width: int, ellipsis: str = "…") -> str:
    if text_width(value) <= width:
        return value
    out = ""
    for char in value:
        if text_width(out + char) > width - 1:
            return out + ellipsis
        out += char
    return out


def render(report: Report, color: bool = True) -> str:
    tick, cross, bar, ellipsis = symbols()
    ok = GREEN if color else ""
    bad = RED if color else ""
    accent = YELLOW if color else ""
    dim = DIM if color else ""
    bold = BOLD if color else ""
    reset = RESET if color else ""

    grade_color = ok if report.score >= 90 else (accent if report.passed else bad)

    lines = [
        f"{bold}ReadmeCraft {__version__}{reset}  ·  {dim}检查 {report.path}{reset}",
        f"{dim}{bar * LINE_WIDTH}{reset}",
        f"{dim}    {pad('规则', RULE_WIDTH)}{pad('判定说明', DETAIL_WIDTH)}得分{reset}",
    ]
    for item in report.items:
        mark = f"{ok}{tick}{reset}" if item.passed else f"{bad}{cross}{reset}"
        score = f"{item.earned}/{item.rule.weight}"
        title = pad(item.rule.title, RULE_WIDTH)
        detail = pad(clip(item.detail, DETAIL_WIDTH, ellipsis), DETAIL_WIDTH)
        color_start = "" if item.passed else bad
        lines.append(f"  {mark} {color_start}{title}{reset}{detail}{pad(score, 5, 'right')}")

    lines.append(f"{dim}{bar * LINE_WIDTH}{reset}")
    verdict = "达到发布线" if report.passed else "未达到 60 分发布线"
    lines.append(
        f"得分 {bold}{report.score}/{report.total}{reset}"
        f"  等级 {grade_color}{report.grade}{reset}  {dim}{verdict}{reset}"
    )
    if report.failed:
        hint = "；".join(item.rule.title for item in report.failed[:3])
        lines.append(f"{accent}建议优先补齐：{hint}{reset}")
    return "\n".join(lines)
