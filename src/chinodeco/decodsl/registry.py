# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import shlex
import inspect
from typing import Callable

from ..debug import (
    DEBUG,
    debug,
    UnknownParameterError,
    UnknownCommandError,
    ArgumentCountError
)

from ..decodsl import (
    when
)

class CommandDispatcher:
    pass

class CommandDispatcher:
    def __init__(self, dispatcher: CommandDispatcher | None = None):
        self.commands = {} if dispatcher is None else dispatcher.commands
    
    def register(self, command: str, wrappers: tuple[Callable] | None = None):
        def __wrap(func):
            wrapped = func
            if wrappers is not None:
                for wrapper in wrappers:
                    wrapped = wrapper(wrapped)
            self.commands[command] = wrapped
            return func
        return __wrap
    
    def parse_command(self, raw: str) -> tuple[str, list[str], dict[str, str | bool]]:
        """
        Parse a CLI-style command string into (command, args, kwargs).

        Supports:
        - command arg1 arg2
        - -abc -> a=True, b=True, c=True
        - --key value
        - --key (alone, treated as key="")
        - quoted strings like "a b c"
        """
        tokens = shlex.split(raw)
        if not tokens:
            raise ValueError("Empty input")

        command = tokens[0]
        args = []
        kwargs = {}
        i = 1

        while i < len(tokens):
            token = tokens[i]
    
            if token.startswith("--"):  # 长参数
                key = token[2:]
                value = ""
                # 检查后续是否是值
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    value = tokens[i + 1]
                    i += 1
                kwargs[key] = value

            elif token.startswith("-") and len(token) > 1:  # 短参数组合 -abc
                for char in token[1:]:
                    kwargs[char] = True

            else:  # 普通参数
                args.append(token)

            i += 1

        return command, args, kwargs
    
    @when(DEBUG)(
        debug
    )
    def run(self, command: str):
        cmd, args, kwargs = self.parse_command(command)
        if cmd in self.commands:
            func = self.commands[cmd]
            sig = inspect.signature(func)
            try:
                sig.bind(*args, **kwargs)
            except TypeError as e:
                msg = str(e)
                if "missing" in msg or "required positional" in msg:
                    raise ArgumentCountError(f"[{self.run.__module__}.{self.run.__qualname__}] {msg}")
                elif "unexpected keyword" in msg:
                    raise UnknownParameterError(f"[{self.run.__module__}.{self.run.__qualname__}] {msg}")
        else:
            raise UnknownCommandError(f"[{self.run.__module__}.{self.run.__qualname__}] command '{cmd}' is not exist.")
        
        return func(*args, **kwargs)