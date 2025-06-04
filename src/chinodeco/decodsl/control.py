# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from functools import wraps
from typing import Callable
import inspect


def when(predicate: Callable[[], bool] | bool, *, elsedeco: Callable | None = None):
    """Conditionally apply a decorator based on a condition. it will use "elsedeco" if the condition is False

    Args:
        condition: A zero-argument function that returns 
            True if the decorator should be applied, or False to skip it.
        elsedo: A decorator that it will be used when condition is False.

    Returns:
        Callable: A decorator that conditionally applies another decorator.
    """
    def wrapper(deco: Callable | None):
        if isinstance(predicate, Callable):
            condition = predicate()
        else:
            condition = predicate
        
        def handle_no_args_deco(target):
            if not callable(deco):
                raise TypeError(f"[chinodeco.decodsl.when] {deco} is not a callable decorator")
            sig = inspect.signature(deco)
            if len(sig.parameters) == 1:
                return deco(target) if condition else target if elsedeco is None else elsedeco(target)
            return deco(target) if condition else target if elsedeco is None else elsedeco(target)

        def handle_args_deco(*args, **kwargs):
            try:
                real_decorator = deco(*args, **kwargs)
            except Exception as e:
                raise TypeError(f"[chinodeco.decodsl.when] Invalid decorator usage: {deco}(*{args}, **{kwargs}) failed: {e}")

            @wraps(real_decorator)
            def wrapped_decorator(func):
                return real_decorator(func) if condition else func if elsedeco is None else elsedeco(func)
            return wrapped_decorator

        def conditional(*args, **kwargs):
            if len(args) == 1 and callable(args[0]) and not kwargs:
                return handle_no_args_deco(args[0])
            return handle_args_deco(*args, **kwargs)

        return conditional
    return wrapper