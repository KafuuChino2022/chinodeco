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

## [0.0.2] - 2025-06-05
### Changed

- `chinodeco.decodsl.when`: 重构语法支持 .elsedeco(...) 链式调用，提升条件逻辑表达力
                            简化带参/不带参装饰器的判断逻辑，增强兼容性

### Enhanced
- `chinodeco.parameter.addprefix / addsuffix`: 参数选择支持混用 形参名 与 位置索引，适配更复杂调用方式
                                               参数绑定逻辑更严谨，确保 *args / **kwargs 情况均能正确识别并修改目标参数
                                               错误信息更清晰，明确提示位置越界、参数缺失或类型不匹配等问题

> 本版本提升了装饰器的可组合性与调用灵活性，为后续 DSL 功能扩展打下基础。