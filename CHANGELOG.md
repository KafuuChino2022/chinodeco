# Changelog

所有 notable changes 都将记录于此。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) 和 [Semantic Versioning](https://semver.org/lang/zh-CN/)

---

## [0.0.1] - 2025-06-04
### Added
- `chinodeco.decochain`: 支持一行组合多个装饰器, 自动跳过 None
- `chinodeco.decodsl.when`: 支持条件性装饰器, 支持 else 分支逻辑
- `chinodeco.parameter.addprefix`: 为参数添加前缀（str / list）
- `chinodeco.parameter.addsuffix`: 为参数添加后缀（str / list）

> 本版本为内部开发版本（非正式发行）, 用于测试装饰器设计模式与 DSL 封装的可行性。

## [0.0.2] - 2025-06-05
### Changed

- `chinodeco.decodsl.when`: 重构语法支持 .elsedeco(...) 链式调用, 提升条件逻辑表达力
                            简化带参/不带参装饰器的判断逻辑, 增强兼容性

### Enhanced
- `chinodeco.parameter.addprefix / addsuffix`: 参数选择支持混用 形参名 与 位置索引, 适配更复杂调用方式
                                               参数绑定逻辑更严谨, 确保 *args / **kwargs 情况均能正确识别并修改目标参数
                                               错误信息更清晰, 明确提示位置越界、参数缺失或类型不匹配等问题

> 本版本提升了装饰器的可组合性与调用灵活性, 为后续 DSL 功能扩展打下基础。

## [0.0.3] - 2025-06-05
### Added
- `chinodeco.debug.debug`：新增错误抑制型装饰器, 防止可调用对象抛出异常中断程序, 默认打印错误信息。
- `chinodeco.debug.DEBUG`：新增调试模式全局开关, 与 `when` 配合控制行为； `_DEBUG_VERBOSE` 控制调试信息详细程度。
- `chinodeco.debug.errors`：新增三种异常类型 `UnknownCommandError`、`UnknownParameterError`、`ArgumentCountError`, 并导出至 `chinodeco.debug`。
- `chinodeco.decodsl.CommandDispatcher`：命令分发器类, 支持注册命令并基于命令字符串执行函数, 支持位置参数、短选项和键值对参数格式。

> DEBUG与_DEBUG_VERBOSE默认情况下都为False

## [0.0.4] - 2025-06-06
### Added
- `chinodeco.decodsl.whileloop`：函数循环执行装饰器, 支持：
  - 条件为 Callable 时持续判断；
  - 条件为常量时基于 `max_loops` 限制执行次数；
  - `.elsedo(...)`：注册条件不满足时的备用函数；
  - `.ifbreak(...)`：提供动态中断逻辑；
  - `loop_wrapper` 控制每次循环使用包装后的函数。
  
### Changed
- `chinodeco.debug.debug`：新增 `verbose` 参数, 允许用户决定是否输出完整模块路径与函数名称信息。

### Enhanced
- `chinodeco.debug.DEBUG`：扩展全局调试模式生效范围, 现已覆盖所有模块中的 raise 操作；
  若启用调试模式, 所有异常将转换为错误提示输出而不中断程序执行。

### Design Note
- 当 `whileloop` 接收非 Callable 的条件时, 视为不可变条件, 仅执行最多 `max_loops` 次。后续版本可能补充对“可变对象”的检测支持。

> 本版本引入了函数循环控制语义与更细粒度的调试输出控制机制, 增强 DSL 的行为表达力与调试友好性。

## [0.0.5] - 2025-06-06
### Added
- 新增 `chinodeco.decodsl.foreach` 循环装饰器（定义于 `chinodeco.decodsl.control`）：
  - 支持遍历 `iter` 参数（若非 Iterable, 则退化为最大循环次数 `max_loops`）；
  - 使用 `loop_wrapper` 为原函数在每次循环中提供新的装饰（不保留）；
  - 函数整体将返回每次调用的返回值组成的列表；
- 新增 `chinodeco.debug.trycatch` 装饰器（定义于 `chinodeco.debug.debugger`）：
  - 支持传入 `exception` 或 `(BaseException, ...)` 类型的元组；
  - `handler` 必须接收一个参数用于错误处理；
  
### Changed
- `chinodeco.debug.errors.ArgumentCountError` 现继承自 `TypeError`；
- 全局异常结构改进：统一使用模块级异常抛出逻辑, 提升一致性与可维护性；

### Fixed
- 修复 `chinodeco.debug.debug` 在显式传入 `verbose` 时仍被 `_DEBUG_VERBOSE` 覆盖的 Bug；

> 本版本加入了异常处理装饰器并添加了新的循环控制, 着重重写了包内的异常抛出

## [0.0.6] - 2025-06-06
### Added
- 新增 `chinodeco.parameter.pretreat` 模块, 提供三个参数预处理装饰器：
  - `setargs`: 指定参数值
  - `mapargs`: 映射函数到参数值
  - `filterargs`: 筛选保留或屏蔽的参数
- 每个模块均新增 `MODULE` 常量标明其来源模块名, 方便调试和报错标识
- 为所有子包添加 `__all__` 以显式导出子模块内容

### Changed
- `chinodeco.parameter.adders` 模块已废弃, 相关逻辑合并入 `pretreat`
- `addprefix` 与 `addsuffix` 已重构, 提取内部逻辑供其他装饰器共用

### Enhanced
- 所有抛出异常的错误信息现在统一使用 `MODULE` 缩写作为前缀, 减少运行时性能损耗并提高错误来源识别性

### Known Issues
- 本版本新增的装饰器与模块尚未经过实际测试, 暂缺 docstring 文档, 计划在下个版本中补齐

> 当前版本处于功能开发阶段, 尚未进入发布流程, 相关 API 稳定性与接口格式仍可能调整

## [0.0.7] - 2025-06-07
### Added
- 完善对包的测试, 补写上一个版本的 docstring, 提升整体代码质量
- 为 `chinodeco.decodsl.control.CommandDispatcher` 添加多级命令注册机制和 `--` 跳过继续匹配命令树功能, 增强命令解析灵活性

### Fixed
- 修复 `chinodeco.parameter.filterargs` 在单 block 模式下屏蔽所有参数的 bug

### Changed
- 废弃 `chinodeco.parameter`, 将 `pretreat` 模块合并至 `chinodeco.pretreat.parameter`, 优化包结构
- 将 `chinodeco.debug.debugger.trycatch` 与 `chinodeco.pretreat.parameter.mapargs` 的 `handler` / `map_func` 参数数量检查提前至装饰器阶段, 防止运行时异常

### Deprecated
- 计划在未来版本中完全废弃 `chinodeco.parameter`, 目前仍从 `chinodeco.pretreat` 包暂时导入以保证兼容性, 请尽早迁移至新模块

> 当前版本处于功能开发阶段, 尚未进入发布流程, 相关 API 稳定性与接口格式仍可能调整

## [0.0.8] - 2025-06-07
### Added
- 新增模块 `chinodeco.pretreat.attrset`，提供一套统一的标签标记系统，包括：
  - `@tag`, `@tagpop`：装饰器形式为函数添加/移除标签；
  - `settags`, `deltags`：显式设置/删除标签；
  - `gettag`, `gettags`, `alltags`：获取单个、多个或全部标签信息；
  - `haskey`, `haskeys`：检查标签键是否存在；
  - `hastag`, `hastags`：检查标签键是否存在且值为真。
- `chinodeco.debug.debugger.debug` 装饰器新增对类的支持，可为类中所有方法批量添加调试包装。

### Changed
- 精简了调试模式下 `@debug` 与 `@when(DEBUG)` 的组合逻辑，避免装饰器嵌套层级对性能产生影响。
- 调试机制仅作用于装饰阶段，不再干预函数调用阶段抛出的异常行为，提升可控性和透明性。

### Enhanced
- 内部调试机制的结构更合理，避免了循环依赖风险，便于后续模块之间交叉依赖（如 `attrset` 与 `CommandDispatcher` 的组合使用）。

---

> 当前版本处于功能开发阶段，预计下个版本将在 `chinodeco.decodsl.control.CommandDispatcher` 基础上引入权限机制，结合标签实现更灵活的行为控制。