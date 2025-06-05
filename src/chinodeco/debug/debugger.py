# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from typing import Callable
from functools import wraps

DEBUG = False
_DEBUG_VERBOSE = False

def debug(func: Callable):
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