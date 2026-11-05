# ReadmeCraft · 给 README 打分的轻量检查器

[![CI](https://github.com/OWNER/readmecraft_30/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/readmecraft_30/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

> 一条命令，给仓库的 README 打分：8 条硬性检查、零第三方依赖、离线可用、结果可写进 CI。

ReadmeCraft 面向课程作业、社团项目和个人小工具这类「有人写代码、没人写文档」的仓库。
它不评价文笔，只回答一个问题：**一个新访客照着 README，能不能在五分钟内把项目跑起来？**

## 目录

- [为什么需要它](#为什么需要它)
- [安装](#安装)
- [使用](#使用)
- [评分规则](#评分规则)
- [在 CI 中使用](#在-ci-中使用)
- [贡献](#贡献)
- [许可证](#许可证)

## 为什么需要它

GitHub 上大量仓库的 README 只有一句项目名。读者要翻提交记录才知道怎么安装，
维护者又常常不知道「到底缺了什么」。通用的 Markdown linter 只能查语法，
查不出「缺少安装说明」这种结构性问题；ReadmeCraft 把开源项目的 README 惯例
固化成 8 条可执行规则，给出可解释的分数和逐条修改建议。

## 安装

需要 Python 3.9 及以上版本，无第三方依赖：

```bash
git clone https://github.com/OWNER/readmecraft_30.git
cd readmecraft_30
python -m readmecraft --version
```

也可以直接以脚本方式运行，不安装任何东西：

```bash
PYTHONPATH=src python -m readmecraft check README.md
```

## 使用

检查单个文件：

```bash
python -m readmecraft check README.md
```

批量检查一个目录下的所有 Markdown 文件，并把结果输出为 JSON 供 CI 消费：

```bash
python -m readmecraft check docs/ --json > report.json
```

为新建项目生成一份带完整骨架的 README：

```bash
python -m readmecraft init my-project
```

退出码约定：`0` 表示达到阈值（默认 60 分），`1` 表示未达标，`2` 表示参数或文件错误，
因此可以直接串进流水线。

## 评分规则

| 规则 | 权重 | 判定方式 |
| --- | --- | --- |
| 标题 | 15 | 首个标题为一级标题 |
| 项目简介 | 10 | 首个二级标题前有不少于 20 字的说明 |
| 安装 | 15 | 含「安装 / Install / Getting Started」小节 |
| 使用示例 | 15 | 含「使用 / Usage」小节且带代码块 |
| 许可证 | 15 | 含「许可证 / License」小节并指向 LICENSE |
| 贡献指南 | 10 | 含「贡献 / Contributing」小节 |
| 徽章 | 10 | 顶部有 CI、License 等徽章 |
| 目录 | 10 | 含目录，或至少有 3 个二级标题 |

总分 100，`A ≥ 90`、`B ≥ 75`、`C ≥ 60`、其余为 `D`。

## 在 CI 中使用

```yaml
- name: Check README
  run: |
    PYTHONPATH=src python -m readmecraft check README.md
```

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增规则的完整流程是：在 `rules.py` 中登记规则，
在 `scorer.py` 中实现判定，在 `tests/` 中补一条正例和一条反例。
所有讨论请走 Issue，合并前需要至少一位维护者 Review。

## 许可证

本项目采用 [MIT License](LICENSE) 发布，欢迎商用与二次分发，请保留版权声明。

## 致谢

规则设计参考了 [GitHub Open Source Guides](https://opensource.guide/) 与
[Standard Readme](https://github.com/RichardLitt/standard-readme) 的公开约定。
