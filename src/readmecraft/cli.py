"""命令行入口：check 检查，init 生成骨架。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .report import render
from .scorer import PASS_SCORE, analyze

TEMPLATE = """# {name}

[![CI](https://github.com/OWNER/{name}/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/{name})
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 一句话说明这个项目解决什么问题。

## 目录

- [安装](#安装)
- [使用](#使用)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装

```bash
git clone https://github.com/OWNER/{name}.git
cd {name}
```

## 使用

```bash
python -m {name} --help
```

## 贡献

欢迎提 Issue 与 Pull Request，详见 CONTRIBUTING.md。

## 许可证

本项目采用 [MIT License](LICENSE) 发布。
"""


def _collect(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(path for path in target.rglob("*.md") if path.is_file())
    return [target]


def _cmd_check(args: argparse.Namespace) -> int:
    targets: list[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            print(f"readmecraft: 找不到 {path}", file=sys.stderr)
            return 2
        targets.extend(_collect(path))

    if not targets:
        print("readmecraft: 没有找到 Markdown 文件", file=sys.stderr)
        return 2

    payload = []
    worst = 0
    for path in targets:
        report = analyze(path)
        worst = max(worst, 0 if report.passed else 1)
        payload.append(report)
        if not args.json:
            print(render(report, color=not args.no_color))
            print()

    if args.json:
        data = [
            {
                "path": str(report.path),
                "score": report.score,
                "grade": report.grade,
                "passed": report.passed,
                "items": [
                    {
                        "key": item.rule.key,
                        "title": item.rule.title,
                        "weight": item.rule.weight,
                        "passed": item.passed,
                        "detail": item.detail,
                    }
                    for item in report.items
                ],
            }
            for report in payload
        ]
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return worst


def _cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.name)
    readme = target / "README.md"
    if readme.exists():
        print(f"readmecraft: {readme} 已存在，未覆盖", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    readme.write_text(TEMPLATE.format(name=target.name), encoding="utf-8")
    print(f"已生成 {readme}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="readmecraft", description="给 README 打分：8 条结构检查，零依赖。"
    )
    parser.add_argument("--version", action="version", version=f"readmecraft {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="检查 Markdown 文件或目录")
    check.add_argument("paths", nargs="+", help="文件或目录路径")
    check.add_argument("--json", action="store_true", help="以 JSON 输出，便于 CI 消费")
    check.add_argument("--no-color", action="store_true", help="关闭 ANSI 颜色")
    check.set_defaults(func=_cmd_check)

    init = sub.add_parser("init", help="为一个新项目生成 README 骨架")
    init.add_argument("name", help="项目目录名")
    init.set_defaults(func=_cmd_init)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
