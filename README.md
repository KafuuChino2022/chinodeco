# chinodeco

chinodeco 是一个用于函数级控制与预处理的 Python 装饰器工具包。
它提供了结构化、模块化的 DSL 风格 API，适用于需要复杂控制逻辑（如条件执行、循环控制、参数转换等）的中型 Python 项目。

## 特性一览

- 装饰器链组合支持：通过 `@decochain(...)` 合并多个装饰器
- 控制流装饰器：条件判断、循环控制、遍历执行
- 预处理工具：函数参数的设置、映射、过滤等
- 调试工具：内建调试模式与异常捕获装饰器
- 命令分发系统：基于树结构注册、解析和执行命令
- 完整支持同步与异步函数（v0.0.9 起）

## 安装

```
pip install git+https://github.com/KafuuChino2022/chinodeco.git
```

或将项目作为子模块引入：

```
git submodule add https://github.com/KafuuChino2022/chinodeco.git external/chinodeco
```

## 模块结构（导出接口）

| 模块 | 说明 |
|------|------|
| `chinodeco.base` | 核心合并器 `decochain` |
| `chinodeco.debug` | 调试工具：`debug`, `trycatch` |
| `chinodeco.decodsl.control` | 控制流：`when`, `whileloop`, `foreach` |
| `chinodeco.decodsl.registry` | 命令注册器：`CommandDispatcher` |
| `chinodeco.pretreat.parameter` | 参数处理器：`setargs`, `addprefix`, `mapargs`, 等 |
| `chinodeco.pretreat.tagging` | 属性标记与查询装饰器：`tag`, `settags`, `hastag`, 等 |

## 示例用法

```python
from chinodeco import decochain
from chinodeco.debug import debug
from chinodeco.pretreat import setargs, mapargs

@decochain(
    debug,
    setargs(("default", 0)),
    mapargs((str.upper, "param1"))
)
def greet(param1, param2):
    print(f"Hello {param1}, code {param2}!")

greet("example", 0)  # Output: Hello DEFAULT, code 0
```

```python
from chinodeco.decodsl import when, whileloop

@when(True)(
    whileloop(True, max_loops=2)
)
async def task():
    print("Looping...")

import asyncio
asyncio.run(task())
```

## 协议

本项目使用 Apache License 2.0。

## NOTICE

参见项目根目录的 NOTICE 文件，了解项目声明与第三方依赖（若有）。

## 开发计划

- 支持异步函数装饰器适配（v0.0.9）
- 命令权限系统（v0.0.10+）
- 自定义错误系统（如 `AuthorizationError`）
- 更强的测试用例和覆盖率分析
- 发布至 PyPI

## 参与贡献

项目仍在初期阶段，尚未发布，欢迎反馈设计建议或提交 PR。
