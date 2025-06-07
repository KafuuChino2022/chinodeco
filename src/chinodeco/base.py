# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.base"

from typing import Callable

from .debug.debugger import _debug_when

@_debug_when
def decochain(*wrappers: Callable | None):
    """
    Chain multiple decorators together.

    Applies each decorator in `wrappers` to the target in order.

    Args:
        *wrappers: Decorators to apply.

    Returns:
        A decorator that applies all given decorators.
    """
    def composed(func):
        wrapped = func
        for wrapper in reversed(wrappers):
            if wrapper is not None:
                wrapped = wrapper(wrapped)
        return wrapped
    return composed