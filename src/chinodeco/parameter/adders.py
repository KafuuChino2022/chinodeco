# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import inspect
from functools import wraps
from typing import (
    Callable,
    Any
)

def addprefix(*add_args:tuple[str | list, str]) -> Callable:
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
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            args = list(args)

            for prefix, key in add_args:
                # by index
                if isinstance(key, int):
                    try:
                        param_name = list(sig.parameters)[key]
                        bound.arguments[param_name] = prefix + bound.arguments[param_name]
                    except IndexError:
                        frame = inspect.currentframe()
                        raise IndexError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Positional index {key} out of range.")
                    except TypeError:
                        frame = inspect.currentframe()
                        raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Cannot add prefix to non-concatenable type at index {key}.")

                # by key
                elif isinstance(key, str):
                    if key in bound.arguments:
                        try:
                            bound.arguments[key] = prefix + bound.arguments[key]
                        except TypeError:
                            frame = inspect.currentframe()
                            raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Cannot add prefix to argument '{key}'.")
                    else:
                        frame = inspect.currentframe()
                        raise KeyError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Argument '{key}' not found.")
                else:
                    frame = inspect.currentframe()
                    raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Invalid key type: {type(key)}. Must be int or str.")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator


def addsuffix(*add_args:tuple[str | list, int]) -> Callable:
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
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            args = list(args)

            for suffix, key in add_args:
                # by index
                if isinstance(key, int):
                    try:
                        param_name = list(sig.parameters)[key]
                        bound.arguments[param_name] = bound.arguments[param_name] + suffix
                    except IndexError:
                        frame = inspect.currentframe()
                        raise IndexError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Positional index {key} out of range.")
                    except TypeError:
                        frame = inspect.currentframe()
                        raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Cannot add suffix to non-concatenable type at index {key}.")

                # by key
                elif isinstance(key, str):
                    if key in bound.arguments:
                        try:
                            bound.arguments[key] = bound.arguments[key] + suffix
                        except TypeError:
                            frame = inspect.currentframe()
                            raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Cannot add suffix to argument '{key}'.")
                    else:
                        frame = inspect.currentframe()
                        raise KeyError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Argument '{key}' not found.")
                else:
                    frame = inspect.currentframe()
                    raise TypeError(f"[{frame.f_globals["__name__"]}.{frame.f_code.co_name}] Invalid key type: {type(key)}. Must be int or str.")

            return func(*bound.args, **bound.kwargs)

        return wrapper
    return decorator