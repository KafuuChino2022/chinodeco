# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.decodsl.control"

import inspect
from functools import wraps
from typing import (
    Callable,
    Iterable,
)

from ..debug.debugger import _debug_when

@_debug_when
class _when_else_chain:
    def __init__(self, condition, deco):
        self.__condition = condition
        self.__elsedc = None
        self.__deco = deco
    
    def elsedeco(self, elsedc: Callable | None = None):
        """
        Register an alternative decorator to apply when the condition is False.

        This method allows conditional decoration: if the main condition fails,
        the decorator provided here will be applied instead.

        Args:
            elsedc: A decorator function to apply if the main condition is False.

        Returns:
            Self: Enables method chaining.

        Notes:
            - If `when(predicate)(deco)` condition is False and no `elsedeco` is provided,
                the target function will be returned unmodified.
        """
        self.__elsedc = elsedc
        return self
    
    def __call__(self, func):
        if self.__condition:
            return self.__deco(func)
        elif self.__elsedc is not None:
            return self.__elsedc(func)
        else:
            return func

def when(predicate: Callable[[], bool] | bool):
    """
    Conditionally apply a decorator based on the evaluation of a predicate.

    Args:
        predicate: A zero-argument function returning a bool, or a bool value.
            If True, the given decorator will be applied.
            If False, the decorator is skipped unless an alternative is provided via `.elsedeco`.

    Returns:
        Callable: A decorator that applies another decorator conditionally.

    Notes:
        Use `.elsedeco(func: Callable | None = None)` to register an alternative decorator
        that is applied when the predicate evaluates to False.

    Example:
        ```python
        @when(lambda: some_condition)
        def deco(func):
            # decorator implementation
            return func

        # or with else decorator fallback
        @when(False).elsedeco(some_other_decorator)
        def deco(func):
            return func
        ```
    """
    def decorator(deco: Callable | None):
        if callable(predicate):
            condition = predicate()
        else:
            condition = predicate

        return _when_else_chain(condition, deco)
    return decorator

@_debug_when
class _whileloop_else_chain:
    def __init__(self, predicate, max_loops, deco):
        self.__predicate = predicate
        self.__max_loops = max_loops
        if callable(self.__predicate) and (not isinstance(self.__max_loops, int) or self.__max_loops < 1):
            raise ValueError(f"[{self.__class__.__module__}.{self.__class__.__qualname__}] max_loops must be a positive integer.")
        self.__break = None
        self.__deco = deco
        self.__elsefunc = None
        self.__args = ()
        self.__kwargs = {}

    def _eval_condition(self):
        return self.__predicate() if callable(self.__predicate) else bool(self.__predicate)

    def elsedo(self, elsefunc: Callable | None = None, /, *args, **kwargs):
        """
        Register a fallback function to be executed when the main predicate is initially False.

        This method is useful for specifying behavior when the loop condition fails at the first check.

        Args:
            elsefunc: A callable function to be executed instead of the main loop.
                If not callable, a TypeError will be raised (or printed if DEBUG mode is enabled).
            *args: Positional arguments to be passed to the fallback function.
            **kwargs: Keyword arguments to be passed to the fallback function.

        Returns:
            Self: Enables method chaining.

        Notes:
            - The fallback function will be called as `elsefunc(*args, **kwargs)`.
            - If your arguments rely on runtime state (e.g., dynamic variables),
                use a lambda or deferred function to avoid premature evaluation:
                `elsedo(lambda: print(f"value is {v}"))`
        """
        if not callable(elsefunc):
            raise TypeError(f"[{self.__class__.__module__}.{self.elsedo.__qualname__}] expected callable, but got {type(elsefunc)}.")
        self.__elsefunc = elsefunc
        self.__args = args
        self.__kwargs = kwargs
        return self

    def ifbreak(self, predicate: Callable | None = None):
        """
            Register a break condition for the loop execution.

        The loop will stop if this predicate returns True during any iteration.
        This is useful for introducing dynamic break control in the loop logic.

        Args:
            predicate: A function that returns True when the loop should exit early.

        Returns:
            Self: Enables method chaining.

        Notes:
            - The predicate is evaluated on each iteration after executing the loop body.
            - If omitted or None, no dynamic break condition is applied.
        """
        self.__break = predicate
        return self

    def __call__(self, func: Callable):
        if not callable(func):
            raise TypeError(f"[{self.__class__.__module__}.{self.elsedo.__qualname__}] expected callable, but got {type(func)}.")
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if callable(self.__predicate):
                    condition = self.__predicate()
                else:
                    condition = self.__predicate
                results = []
                count = 0
                if condition:
                    while condition:
                        if self.__break() if callable(self.__break) else self.__break:
                            break
                        results.append(await (self.__deco(func)(*args, **kwargs) if callable(self.__deco) else func(*args, **kwargs)))
                        count += 1
                        if callable(self.__predicate):
                            condition = self.__predicate()
                        else:
                            if count >= self.__max_loops:
                                break
                elif self.__elsefunc is not None:
                    self.__elsefunc(*self.__args, **self.__kwargs)
                return results
            return async_wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if callable(self.__predicate):
                    condition = self.__predicate()
                else:
                    condition = self.__predicate
                results = []
                count = 0
                if condition:
                    while condition:
                        if self.__break() if callable(self.__break) else self.__break:
                            break
                        results.append(self.__deco(func)(*args, **kwargs) if callable(self.__deco) else func(*args, **kwargs))
                        count += 1
                        if callable(self.__predicate):
                            condition = self.__predicate()
                        else:
                            if count >= self.__max_loops:
                                break
                elif self.__elsefunc is not None:
                    self.__elsefunc(*self.__args, **self.__kwargs)
                return results
            return wrapper

def whileloop(predicate: Callable[[], bool] | bool, *, loop_wrapper: Callable | None = None, max_loops = 1):
    """
    Decorator for executing a function repeatedly while a predicate is True.

    Args:
        predicate: A condition to evaluate before each execution.
            - If a callable is provided, it will be evaluated before every iteration.
            - If a constant boolean is provided, loop will execute at most once or based on max_loops.
        loop_wrapper: An optional decorator to apply to the function on **each call**.
        max_loops: Maximum number of iterations. Defaults to 1. Ignored when predicate is callable.

    Returns:
        A decorator that wraps the target function in a controlled loop.

    Notes:
        Use `.elsedo(func, *args, **kwargs)` to register a fallback function when predicate is initially False.
        Use `.ifbreak(predicate)` to provide a break condition during loop execution.
        If the predicate is not callable, it's assumed to be static and won't be re-evaluated during the loop.
        For dynamic or state-dependent conditions (e.g., involving mutable objects), wrap them in a lambda or function.
        Use `loop_wrapper=...` to wrap the function on **each loop iteration**.
        This differs from placing a decorator outside `@whileloop`, which wraps the whole decorated function only once.

    Example:
        ```python
        count = 3
        @whileloop(lambda: count > 0)
        def task():
            ...
        ```
    """
    return _whileloop_else_chain(predicate, max_loops, loop_wrapper)

@_debug_when
def foreach(iter: Iterable | None = None, *, max_loops: int = 10, loop_wrapper: Callable | None = None):
    def decorator(func: Callable):
        
        
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                results = []
                if (iter is not None) and isinstance(iter, Iterable):
                    for _ in iter:
                        results.append(await (loop_wrapper(func)(*args, **kwargs) if callable(loop_wrapper) else func(*args, **kwargs)))
                elif iter is None:
                    for _ in range(max_loops):
                        results.append(await (loop_wrapper(func)(*args, **kwargs) if callable(loop_wrapper) else func(*args, **kwargs)))
                else:
                    raise TypeError(f"[{MODULE}.foreach] Invalid iter type: {type(iter)}. Must be Iterable.")
                return results
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                results = []
                if (iter is not None) and isinstance(iter, Iterable):
                    for _ in iter:
                        results.append(loop_wrapper(func)(*args, **kwargs) if callable(loop_wrapper) else func(*args, **kwargs))
                elif iter is None:
                    for _ in range(max_loops):
                        results.append(loop_wrapper(func)(*args, **kwargs) if callable(loop_wrapper) else func(*args, **kwargs))
                else:
                    raise TypeError(f"[{MODULE}.foreach] Invalid iter type: {type(iter)}. Must be Iterable.")
                return results
            return sync_wrapper

    return decorator