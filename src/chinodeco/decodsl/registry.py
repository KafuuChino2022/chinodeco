# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.decodsl.registry"

import warnings
import shlex
import inspect
from typing import (
    Callable,
    Any
)

from ..debug.debugger import _debug_when

from ..debug.errors import (
    UnknownParameterError,
    UnknownCommandError,
    ArgumentCountError,
    AuthorizationError
)

class CommandNode:
    pass
class CommandDispatcher:
    pass

class CommandNode:
    def __init__(self, handler: Callable | None = None, children: dict[str, CommandNode] | None = None):
        self.handler: Callable = handler
        self.children: dict[str, CommandNode] = children or {}

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
        self.root = dispatcher.root if dispatcher is not None else CommandNode()
    
    @_debug_when
    def register(self, path: str, *wrappers: Callable):
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
        tokens = path.split()
        node = self.root
        for current_cmd in tokens:
            node = node.children.setdefault(current_cmd, CommandNode())
        def __wrap(func):
            wrapped = func
            if wrappers is not None:
                for wrapper in reversed(wrappers):
                    wrapped = wrapper(wrapped)
            if node.handler is not None:
                warnings.warn(f"[{self.__class__.__module__}.{self.register.__qualname__}] command '{".".join(path.split())}' is already registered; existing command will be overwritten.", RuntimeWarning)
            node.handler = wrapped
            return func
        return __wrap

    @staticmethod
    def _clean_token(token: str):
        if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")) and len(token > 1):
            return token[1: -1]
        return token

    def parse_command(self, raw: str, emptiable: bool = True) -> tuple[CommandNode, list[str], list[str], dict[str, str | bool]]:
        """
        Parse a CLI-style command string into (command, args, kwargs).

        Supports:
        - command1 command2 arg1 arg2
        - -abc -> a=True, b=True, c=True
        - --key value
        - --key (alone, treated as key="")
        - quoted strings like "a b c"
        - command1 command2 -- arg1 arg2 ("--" can be used to stop identify commands, but args)
        """
        tokens = shlex.split(raw, posix = False)
        if not tokens and emptiable:
            return (self.root, [], [], {})

        if not tokens:
            raise ValueError(f"[{self.__class__.__module__}.{self.parse_command.__qualname__}] command is empty.")

        node = self.root
        if len(tokens) == 1 and not tokens[0] in node.children:
            return (self.root, [tokens[0]], [], {})
        command_path = []
        args = []
        kwargs = []
        i = 0
        
        if tokens[0] not in node.children:
            return (self.root, [tokens[0]], [], {})

        while i < len(tokens):
            token = tokens[i]

            # command treat
            if token == "--":
                i += 1
                break

            if token.startswith("-") or (token not in node.children) or (token.startswith("'") and token.endswith("'")) or (token.startswith('"') and token.endswith('"')):
                break

            node = node.children[token]
            command_path.append(token)
            i += 1

        while i < len(tokens):
            token = tokens[i]
            # param treat
            if token.startswith("--"):
                key = token[2:]
                values = ""
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    values = []
                    while i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                        values.append(self._clean_token(tokens[i + 1]))
                        i += 1
                    values = values if len(values) > 1 else values[0]
                kwargs.append((key, values))
            elif token.startswith("-") and len(token) > 1:
                for char in token[1:]:
                    kwargs.append((char, True))
            else:
                args.append(self._clean_token(token))

            i += 1

        kwargs_dict = {k: v for k, v in kwargs}

        return node, command_path, args, kwargs_dict

    def run(self, command: str, *options: tuple[str, Any] | str, cmd_emptiable: bool = True):
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
        node, path, args, kwargs = self.parse_command(command, cmd_emptiable)
        if not path and cmd_emptiable:
            return None
        if not node.handler:
            raise UnknownCommandError(f"[{self.__class__.__module__}.{self.run.__qualname__}] command '{".".join(path)}' is not exist.")

        func = node.handler
        sig = inspect.signature(func)

        try:
            sig.bind(*args, **kwargs)
        except TypeError as e:
            msg = str(e)
            if "missing" in msg or "required positional" in msg:
                raise ArgumentCountError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")
            elif "unexpected keyword" in msg:
                raise UnknownParameterError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")

        if options:
            tags = getattr(func, "__chino_tags", {})
            for option in options:
                if isinstance(option, tuple) and len(option) == 2 and isinstance(option[0], str):
                    if tags.get(option[0], False) == option[1]:
                        return func(*args, **kwargs)
                elif isinstance(option, str):
                    if tags.get(option, False):
                        return func(*args, **kwargs)
                else:
                    raise TypeError(f"[{self.__class__.__module__}.{self.run.__qualname__}] each option must be a str or tuple[str, Any], but got {type(option).__name__}: {option!r}")
            raise AuthorizationError(f"[{self.__class__.__module__}.{self.run.__qualname__}]-'{func.__qualname__}' you are not allowed to use command '{" ".join(path)}' please check your authority.")
        return func(*args, **kwargs)
    
    
    async def asyncrun(self, command: str, *options: tuple[str, Any] | str, cmd_emptiable: bool = True):
        """
        Execute a registered command with parsed arguments and keyword arguments.

        This method parses the raw command string, extracts the command name,
        positional arguments, and keyword arguments, then invokes the corresponding
        registered coroutine function if found.

        Args:
            command: A raw command-line style string to be executed.
                Example: `"greet hello --name Alice -v"`

        Returns:
            Any: The return value of the executed command coroutine function.

        Raises:
            UnknownCommandError: If the command name is not registered.
            ArgumentCountError: If required positional arguments are missing.
            UnknownParameterError: If unexpected keyword arguments are passed.

        Notes:
            - Command functions must be registered via `register(command_name)(func)` before execution.
            - Arguments are parsed using shell-like syntax (via `shlex.split()`).
            - Supports short flags (e.g., `-abc`), long options (`--key value`), and quoted strings.
        """
        node, path, args, kwargs = self.parse_command(command, cmd_emptiable)
        if not path and cmd_emptiable:
            return None
        if not node.handler:
            raise UnknownCommandError(f"[{self.__class__.__module__}.{self.run.__qualname__}] command '{".".join(path)}' is not exist.")

        func = node.handler
        sig = inspect.signature(func)

        try:
            sig.bind(*args, **kwargs)
        except TypeError as e:
            msg = str(e)
            if "missing" in msg or "required positional" in msg:
                raise ArgumentCountError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")
            elif "unexpected keyword" in msg:
                raise UnknownParameterError(f"[{self.__class__.__module__}.{self.run.__qualname__}] {msg}")
        
        if options:
            tags = getattr(func, "__chino_tags", {})
            for option in options:
                if isinstance(option, tuple) and len(option) == 2 and isinstance(option[0], str):
                    if tags.get(option[0], False) == option[1]:
                        return func(*args, **kwargs)
                elif isinstance(option, str):
                    if tags.get(option, False):
                        return func(*args, **kwargs)
                else:
                    raise TypeError(f"[{self.__class__.__module__}.{self.run.__qualname__}] each option must be a str or tuple[str, Any], but got {type(option).__name__}: {option!r}")
            raise AuthorizationError(f"[{self.__class__.__module__}.{self.run.__qualname__}]-'{func.__qualname__}' you are not allowed to use command '{" ".join(path)}' please check your authority.")

        return (await func(*args, **kwargs)) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)