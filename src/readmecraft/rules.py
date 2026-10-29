"""检查规则表。

规则是数据而不是分支代码：每条规则只有 key / 标题 / 权重 / 提示，
判定逻辑集中在 scorer.py，新增一条规则不需要改动 CLI。
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    key: str
    title: str
    weight: int
    hint: str


RULES: tuple[Rule, ...] = (
    Rule("title", "标题", 15, "以一级标题「# 项目名」开头"),
    Rule("intro", "项目简介", 10, "第一个二级标题前用 1-3 句话说明项目做什么"),
    Rule("install", "安装", 15, "包含「安装 / Install / Getting Started」小节"),
    Rule("usage", "使用示例", 15, "包含「使用 / Usage」小节且带代码块"),
    Rule("license", "许可证", 15, "包含「许可证 / License」小节并链接 LICENSE 文件"),
    Rule("contributing", "贡献指南", 10, "包含「贡献 / Contributing」小节"),
    Rule("badges", "徽章", 10, "顶部放置 CI / License 等徽章"),
    Rule("toc", "目录", 10, "含目录，或至少有 3 个二级标题"),
)

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)
FENCE = re.compile(r"^[ \t]*```", re.MULTILINE)
BADGE = re.compile(r"!\[[^\]]*\]\([^)]*(?:badge|shields\.io)[^)]*\)", re.IGNORECASE)
INLINE_CODE = re.compile(r"`[^`\n]+`")


def headings(text: str) -> list[tuple[int, str]]:
    """返回 [(层级, 标题文本)]，忽略代码块内部的伪标题。"""
    lines = text.splitlines()
    result: list[tuple[int, str]] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if match:
            result.append((len(match.group(1)), match.group(2).strip()))
    return result


def has_section(text: str, *names: str) -> bool:
    """标题中是否出现给定关键词之一（大小写不敏感，支持中英混排）。"""
    lowered = [name.lower() for name in names]
    for _, title in headings(text):
        plain = title.lower()
        if any(name in plain for name in lowered):
            return True
    return False


def has_code_block(text: str) -> bool:
    return len(FENCE.findall(text)) >= 2


def intro_text(text: str) -> str:
    """首个二级标题之前的正文，去掉标题行、徽章与代码块。"""
    lines: list[str] = []
    in_fence = False
    seen_heading = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("#"):
            if seen_heading and len(stripped) - len(stripped.lstrip("#")) >= 2:
                break
            seen_heading = True
            continue
        if stripped.startswith("[!["):
            continue
        lines.append(stripped)
    return " ".join(part for part in lines if part)


def plain_length(value: str) -> int:
    """去掉徽章、链接语法和空白后的字符数，避免用空链接刷长度。"""
    value = INLINE_CODE.sub("", value)
    value = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\s+", "", value)
    return len(value)
