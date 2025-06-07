# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.debug.debugger"

import inspect
from typing import (
    Callable,
    Any
)
from functools import wraps
from .errors import ArgumentCountError

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
        return lambda f: debug(f, verbose=verbose)
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if verbose:
                print(f"[{MODULE}.{getattr(func, "__qualname__", repr(func))}] {e}")
            else:
                print(f"{e}")
    return wrapper

def trycatch(exception: BaseException | tuple[BaseException], handler: Callable[[BaseException], Any]):
    """
    Decorator that wraps a function in a try-except block, invoking a handler if the specified exception occurs.

    Parameters:
        exception:
            The exception type(s) to catch. Can be a single exception class or a tuple of multiple exception classes.
        handler:
            A callable that takes exactly one argument (the exception instance) and handles the error.
            The return value of this handler will be used as the result of the decorated function upon exception.

    Raises:
        TypeError: If `func` or `handler` is not callable, or if `handler` does not accept exactly one parameter.

    Example:
        @trycatch(ValueError, lambda e: print(f"Handled error: {e}"))
        def parse_int(text):
            return int(text)
    """
    if not callable(handler):
        raise TypeError(f"[{MODULE}.trycatch] handler must be callable.")

    # check argument count
    sig = inspect.signature(handler)
    params = list(sig.parameters.values())
    valid_params = [p for p in params if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    if len(valid_params) != 1:
        raise ArgumentCountError(f"[{MODULE}.trycatch] handler must accept exactly one argument, but got {len(valid_params)}.")

    def decorator(func: Callable):
        if not callable(func):
            raise TypeError(f"[{MODULE}.trycatch] Invalid func type: {type(func)}. Must be Callable.")
        if not callable(func):
            raise TypeError(f"[{MODULE}.trycatch] Invalid handler type: {type(handler)}. Must be Callable.")
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                try:
                    return handler(e)
                except TypeError as error:
                    raise TypeError(f"[{MODULE}.trycatch] {error}.")
        return wrapper
    return decorator