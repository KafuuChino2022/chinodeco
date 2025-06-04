# Changelog

所有 notable changes 都将记录于此。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) 和 [Semantic Versioning](https://semver.org/lang/zh-CN/)

---

## [0.0.1] - 2025-06-04
### Added
- `chinodeco.decochain`: 支持一行组合多个装饰器，自动跳过 None
- `chinodeco.decodsl.when`: 支持条件性装饰器，支持 else 分支逻辑
- `chinodeco.parameter.addprefix`: 为参数添加前缀（str / list）
- `chinodeco.parameter.addsuffix`: 为参数添加后缀（str / list）

> 本版本为内部开发版本（非正式发行），用于测试装饰器设计模式与 DSL 封装的可行性。