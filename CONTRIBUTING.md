# 贡献指南

感谢你愿意为 ReadmeCraft 出一份力。这个项目的目标很小：**只做 README 的结构检查，不碰文笔评价**。
在提 Pull Request 之前，请先花两分钟读完下面三节。

## 开发环境

```bash
git clone https://github.com/OWNER/readmecraft_30.git
cd readmecraft_30
python -m venv .venv
.venv/Scripts/activate        # Windows
pip install -e .
python -m unittest discover -s tests -t . -v
```

项目不引入任何第三方运行依赖，提交前请确认 `python -m readmecraft check README.md` 能跑通。

## 分支约定

| 分支 | 用途 |
| --- | --- |
| `main` | 随时可发布的稳定分支，受保护，只能通过 Pull Request 合入 |
| `feature/<主题>` | 新功能，例如 `feature/score-weights` |
| `hotfix/<主题>` | 紧急修复，例如 `hotfix/license-rule` |
| `docs/<主题>` | 只改文档的提交 |

提交信息遵循 Conventional Commits：`feat: 支持 .mdx`、`fix: 修正许可证规则误判`、
`docs: 补充分支约定`。每个 Pull Request 至少关联一个 Issue。

## 新增一条检查规则

1. 在 `src/readmecraft/rules.py` 的 `RULES` 里登记 key、标题、权重与提示；
2. 在 `src/readmecraft/scorer.py` 的 `CHECKS` 中实现判定函数；
3. 在 `tests/` 里补一条正例、一条反例；
4. 更新 README 的规则表与 `CHANGELOG.md`。

权重总和必须保持 100，`test_weights_sum_to_one_hundred` 会挡住不合规的改动。

## 行为准则

参与讨论即表示同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。技术分歧请对事不对人。
