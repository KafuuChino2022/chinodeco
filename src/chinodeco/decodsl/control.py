# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from functools import wraps
from typing import (
    Callable,
    Any
)
import inspect

class _when_else_chain:
    def __init__(self, condition, deco):
        self.__condition = condition
        self.__elsedc = None
        self.__deco = deco
    
    def elsedeco(self, elsedc: Callable | None = None):
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
    """Conditionally apply a decorator based on a condition. it will use "elsedeco" if the condition is False

    Args:
        condition: A zero-argument function that returns 
            True if the decorator should be applied, or False to skip it.
        elsedo: A decorator that it will be used when condition is False.

    Returns:
        Callable: A decorator that conditionally applies another decorator.
    """
    def decorator(deco: Callable | None):
        if isinstance(predicate, Callable):
            condition = predicate()
        else:
            condition = predicate

        return _when_else_chain(condition, deco)
    return decorator