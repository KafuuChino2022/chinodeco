# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from typing import (
    Callable,
    Any
)
from functools import wraps

def addprefix(*add_args:tuple[str | list, int], add_kwargs: dict[Any, str | list] = None) -> Callable:
    """
    Add a prefix to specified positional or keyword arguments of a function.

    Args:
        *add_args: Tuples of (prefix, index) to prepend to positional arguments.
        add_kwargs: A dict mapping keyword argument names to prefixes.

    Returns:
        A decorated function with specified arguments automatically prefixed.

    Raises:
        IndexError: If a positional argument index is out of range.
        KeyError: If a specified keyword argument is missing.
        TypeError: If concatenation fails due to type mismatch.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args)
            for pre, index in add_args:
                try:
                    args[index] = pre + args[index]
                except IndexError:
                    raise IndexError(f"[chinodeco.parameter.addprefix] args index {index} out of range.")
                except TypeError:
                    raise TypeError(f"[chinodeco.parameter.addprefix] Cannot concatenate {type(pre)} and {type(args[index])} at position {index}.")

            if add_kwargs is not None:
                for key, pre in add_kwargs.items():
                    try:
                        kwargs[key] = pre + kwargs[key]
                    except KeyError:
                        raise KeyError(f"[chinodeco.parameter.addprefix] kwargs key '{key}' not found.")
                    except TypeError:
                        raise TypeError(f"[chinodeco.parameter.addprefix] Cannot concatenate {type(pre)} and {type(kwargs[key])} for key '{key}'.")

            return func(*args, **kwargs)
        return wrapper
    return decorator


def addsuffix(*add_args:tuple[str | list, int], add_kwargs: dict[Any, str | list] = None) -> Callable:
    """
    Add a suffix to specified positional or keyword arguments of a function.

    Args:
        *add_args: Tuples of (suffix, index) to prepend to positional arguments.
        add_kwargs: A dict mapping keyword argument names to suffixes.

    Returns:
        A decorated function with specified arguments automatically suffixed.

    Raises:
        IndexError: If a positional argument index is out of range.
        KeyError: If a specified keyword argument is missing.
        TypeError: If concatenation fails due to type mismatch.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args)
            for suf, index in add_args:
                try:
                    args[index] = args[index] + suf
                except IndexError:
                    raise IndexError(f"[chinodeco.parameter.addsuffix] args index {index} out of range.")
                except TypeError:
                    raise TypeError(f"[chinodeco.parameter.addsuffix] Cannot concatenate {type(args[index])} and {type(suf)} at position {index}.")

            if add_kwargs is not None:
                for key, suf in add_kwargs.items():
                    try:
                        kwargs[key] = kwargs[key] + suf
                    except KeyError:
                        raise KeyError(f"[chinodeco.parameter.addsuffix] kwargs key '{key}' not found.")
                    except TypeError:
                        raise TypeError(f"[chinodeco.parameter.addsuffix] Cannot concatenate {type(kwargs[key])} and {type(suf)} for key '{key}'.")

            return func(*args, **kwargs)
        return wrapper
    return decorator