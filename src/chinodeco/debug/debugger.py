# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from typing import Callable
from functools import wraps

DEBUG = False
_DEBUG_VERBOSE = False

def debug(func: Callable | None = None, *, verbose = _DEBUG_VERBOSE):
    """
    A decorator that suppresses exceptions raised by the decorated function and optionally prints debug information.

    If `verbose` is True, it prints the module and qualified name of the function along with the error message.
    Otherwise, only the exception message is printed.

    Can be used with or without parentheses:
        @debug
        def my_func(): ...

        @debug(verbose=True)
        def my_func(): ...

    Args:
        func: The target function to wrap. Automatically handled when used as a decorator.
        verbose: Whether to include full function context in the error output.

    Returns:
        Callable: The wrapped function with error suppression and optional debug output.
    """
    if func is None:
        return lambda f: debug(f, verbose)
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if _DEBUG_VERBOSE:
                print(f"[{getattr(func, "__module__", "unknown")}.{getattr(func, "__qualname__", repr(func))}] {e}")
            else:
                print(f"{e}")
    return wrapper