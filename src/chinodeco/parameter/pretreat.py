# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.parameter"

import inspect
from functools import wraps
from typing import (
    Callable,
    Any
)

from ..debug.debugger import (
    DEBUG,
    debug,
)

from ..decodsl.control import (
    when
)

def _patch_args(bound: inspect.BoundArguments, sig: inspect.Signature, updates: list[tuple[Callable[[Any], Any], str | int]], *, tag: str = "") -> Callable:

    try:
        for modifier, key in updates:
            # by index
            if isinstance(key, int):
                try:
                    param_name = list(sig.parameters)[key]
                    bound.arguments[param_name] = modifier(bound.arguments[param_name])
                except IndexError:
                    raise IndexError(f"[{tag}] Positional index {key} out of range.")
                except Exception as e:
                    raise TypeError(f"[{tag}] {e}")

            # by key
            elif isinstance(key, str):
                if key in bound.arguments:
                    try:
                        bound.arguments[key] = modifier(bound.arguments[key])
                    except TypeError as e:
                        raise TypeError(f"[{tag}] {e}")
                else:
                    raise KeyError(f"[{tag}] Argument '{key}' not found.")
            else:
                raise TypeError(f"[{tag}] Invalid key type: {type(key)}. Must be int or str.")
    except ValueError as e:
        raise ValueError(f"[{tag}] {e}")

def setargs(*set_args:tuple[Any, str | int]) -> Callable:
    def decorator(func: Callable):
        sig = inspect.signature(func)

        @wraps(func)
        @when(DEBUG)(
            debug
        )
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            updates = []
            
            def make_modifier(v): return lambda x: v

            for value, key in set_args:
                updates.append((make_modifier(value), key))
            
            _patch_args(bound, sig, updates, tag = f"[{MODULE}.setargs]")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator

def addprefix(*add_args:tuple[str | list, str | int]) -> Callable:
    """
    Add a prefix to specified positional or keyword arguments of a function.

    Args:
        *add_args: Tuples of (prefix, index) to prepend to positional arguments, index also can be a key.

    Returns:
        A decorated function with specified arguments automatically prefixed.

    Raises:
        IndexError: If a positional argument index is out of range.
        KeyError: If a specified keyword argument is missing.
        TypeError: If concatenation fails due to type mismatch.
    """
    def decorator(func: Callable):
        sig = inspect.signature(func)

        @wraps(func)
        @when(DEBUG)(
            debug
        )
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            updates = []
            
            def make_modifier(p): return lambda x: p + x

            for pre, key in add_args:
                updates.append((make_modifier(pre), key))
            
            _patch_args(bound, sig, updates, tag = f"{MODULE}.addprefix")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator


def addsuffix(*add_args:tuple[str | list, int | str]) -> Callable:
    """
    Add a suffix to specified positional or keyword arguments of a function.

    Args:
        *add_args: Tuples of (suffix, index) to prepend to positional arguments, index also can be a key.

    Returns:
        A decorated function with specified arguments automatically suffixed.

    Raises:
        IndexError: If a positional argument index is out of range.
        KeyError: If a specified keyword argument is missing.
        TypeError: If concatenation fails due to type mismatch.
    """
    def decorator(func: Callable):
        sig = inspect.signature(func)

        @wraps(func)
        @when(DEBUG)(
            debug
        )
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            updates = []
            
            def make_modifier(s): return lambda x: x + s

            for suf, key in add_args:
                updates.append((make_modifier(suf), key))
            
            _patch_args(bound, sig, updates, tag = f"{MODULE}.addsuffix")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator

def mapargs(*map_args:tuple[Callable[[Any], Any], int | str]) -> Callable:
    def decorator(func: Callable):
        sig = inspect.signature(func)

        @wraps(func)
        @when(DEBUG)(
            debug
        )
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            updates = []
            
            def make_modifier(f): return lambda x: f(x)

            for map_func, key in map_args:

                if not callable(map_func):
                    raise TypeError(f"[{MODULE}.mapargs] map_func must be callable.")
                sig_map = inspect.signature(map_func)
                if len(sig_map.parameters) != 1:
                    raise TypeError(f"[{MODULE}.mapargs] map_func must accept exactly one argument.")
                updates.append((make_modifier(map_func), key))

            _patch_args(bound, sig, updates, tag = f"{MODULE}.mapargs")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator

def _matches(value, patterns):
    for pattern in patterns:
        if isinstance(pattern, type):
            if isinstance(value, pattern):
                return True
        elif value == pattern:
            return True
    return False

def filterargs(*, allow: list | None = None, block: list | None = None, allow_block: bool = False):
    if (not allow_block) and (allow is not None and block is not None):
        raise ValueError(f"[{MODULE}.filterargs] filterargs cannot accpet both 'allow' and 'block' at the same time.")
    allow = allow or []
    block = block or []
    def decorator(func: Callable):

        @wraps(func)
        @when(DEBUG)(
            debug
        )
        def wrapper(*args, **kwargs):
            active_allow = [arguments() if callable(arguments) else arguments for arguments in allow]
            active_block = [arguments() if callable(arguments) else arguments for arguments in block]

            bound = inspect.signature(func).bind_partial(*args, **kwargs)
            bound.apply_defaults()

            new_args = []
            for param in bound.args:
                if _matches(param, active_block) or not _matches(param, active_allow):
                    continue
                new_args.append(param)

            new_kwargs = {}
            for key, value in bound.kwargs.items():
                if _matches(value, active_block) or not _matches(value, active_allow):
                    continue
                new_kwargs[key] = value

            return func(*new_args, **new_kwargs)
        return wrapper
    return decorator