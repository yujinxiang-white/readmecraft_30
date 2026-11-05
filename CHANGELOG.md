# 更新日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)，格式参考 Keep a Changelog。

## [Unreleased]

### Planned

- 支持 `.mdx` 与 `README.rst`；
- `--fix` 自动补全缺失小节。

## [0.1.0] - 2026-11-10

### Added

- 8 条 README 结构检查规则，权重合计 100；
- `check` 子命令：支持文件、目录、`--json`、`--no-color`；
- `init` 子命令：生成带目录、安装、使用、贡献、许可证五节的 README 骨架；
- GitHub Actions 工作流：Python 3.9 / 3.11 / 3.13 矩阵测试。

### Fixed

- 许可证规则此前只匹配英文 `License`，中文「许可证」标题会被误判（Issue #2）。
