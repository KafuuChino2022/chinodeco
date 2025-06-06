# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.decodsl.registry"

import shlex
import inspect
from typing import Callable

from ..debug.debugger import (
    DEBUG,
    debug,
)

from ..debug.errors import (
    UnknownParameterError,
    UnknownCommandError,
    ArgumentCountError
)

from ..decodsl.control import (
    when
)

class CommandDispatcher:
    pass

class CommandDispatcher:
    def __init__(self, dispatcher: CommandDispatcher | None = None):
        """
        Initialize a CommandDispatcher.

        Args:
            dispatcher (CommandDispatcher, optional): If provided, inherits the command registry
                from the given dispatcher instance. This enables command reuse or delegation across
                multiple dispatchers.

        Example:
            # Share commands from one dispatcher to another
            base = CommandDispatcher()
            derived = CommandDispatcher(base)
        """
        self.commands = {} if dispatcher is None else dispatcher.commands
    
    def register(self, command: str, *wrappers: Callable):
        """
        Register a function as a command handler.

        Args:
            command: The command keyword that will trigger the registered function.
            wrappers: A tuple of decorator functions to wrap the command handler.
                These wrappers will be applied in order, allowing preprocessing like logging, validation, etc.

        Returns:
            Callable: A decorator that registers the function as a command handler.

        Example:
            @dispatcher.register("greet")
            def greet(name):
                print(f"Hello, {name}!")

            @dispatcher.register("secure", wrappers=(auth_check,))
            def secure_action():
                ...
        """
        def __wrap(func):
            wrapped = func
            if wrappers is not None:
                for wrapper in wrappers:
                    wrapped = wrapper(wrapped)
            self.commands[command] = wrapped
            return func
        return __wrap
    
    @when(DEBUG)(
        debug
    )
    def parse_command(self, raw: str, emptiable: bool) -> tuple[str, list[str], dict[str, str | bool]]:
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
        if not tokens and emptiable:
            return ("", [], {})
        elif not tokens:
            raise ValueError(f"[{self.__class__.__module__}.{self.parse_command.__qualname__}] command is empty.")

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
    def run(self, command: str, cmd_emptiable: bool = True):
        """
        Execute a registered command with parsed arguments and keyword arguments.

        This method parses the raw command string, extracts the command name,
        positional arguments, and keyword arguments, then invokes the corresponding
        registered function if found.

        Args:
            command: A raw command-line style string to be executed.
                Example: `"greet hello --name Alice -v"`

        Returns:
            Any: The return value of the executed command function.

        Raises:
            UnknownCommandError: If the command name is not registered.
            ArgumentCountError: If required positional arguments are missing.
            UnknownParameterError: If unexpected keyword arguments are passed.

        Notes:
            - Command functions must be registered via `register(command_name)(func)` before execution.
            - Arguments are parsed using shell-like syntax (via `shlex.split()`).
            - Supports short flags (e.g., `-abc`), long options (`--key value`), and quoted strings.
        """
        cmd, args, kwargs = self.parse_command(command, cmd_emptiable)
        if not cmd and cmd_emptiable:
            return None
        elif cmd in self.commands:
            func = self.commands[cmd]
            sig = inspect.signature(func)
            try:
                sig.bind(*args, **kwargs)
            except TypeError as e:
                msg = str(e)
                if "missing" in msg or "required positional" in msg:
                    raise ArgumentCountError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")
                elif "unexpected keyword" in msg:
                    raise UnknownParameterError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")
        else:
            raise UnknownCommandError(f"[{self.__class__.__module__}.{self.run.__qualname__}] command '{cmd}' is not exist.")
        
        return func(*args, **kwargs)