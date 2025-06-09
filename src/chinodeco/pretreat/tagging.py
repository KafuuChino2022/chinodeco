# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.pretreat.attrset"

from typing import (
    Callable,
    Any
)

from ..debug.debugger import _debug_when

def _ensure_callable(func: Any, funcname: str):
    if not callable(func):
        raise TypeError(f"[{MODULE}.{funcname}] expected a callable, but got {type(func).__name__}")


def settags(func: Callable, *tags: str | tuple[str, Any]):
    """
    Add one or more tags with optional values to the callable's __chino_tags dictionary.

    Each tag can be a string (value defaults to True) or a tuple (key, value).

    Args:
        func: Callable object to add tags to.
        *tags: Tags to add, each either a str or a (str, Any) tuple.

    Raises:
        TypeError: If a tag is neither str nor tuple[str, Any], or tuple format is invalid.
    """
    _ensure_callable(func, "settags")
    if not hasattr(func, "__chino_tags"):
        func.__chino_tags = {}
    for tag in tags:
        if isinstance(tag, str):
            func.__chino_tags[tag] = True
        elif isinstance(tag, tuple):
            if len(tag) == 2 and isinstance(tag[0], str):
                func.__chino_tags[tag[0]] = tag[1]
            else:
                raise TypeError(f"[{MODULE}.tag] Invalid tuple tag: expected (str, Any), got {tag!r}")
        else:
            raise TypeError(f"[{MODULE}.tag] each tag must be a str or tuple[str, Any], but got {type(tag).__name__}: {tag!r}")

@_debug_when
def tag(*tags: str | tuple[str, Any]):
    """
    Decorator that adds specified tags to the decorated callable.

    Args:
        *tags: Tags to add, each either a str or a (str, Any) tuple.

    Returns:
        Callable: The decorated function with tags added.
    """
    def decorator(func: Callable):
        _ensure_callable(func, "tag")
        settags(func, *tags)
        return func
    return decorator


def haskey(func: Callable, key: str) -> bool:
    """
    Check whether the callable has a given tag key.

    Args:
        func: Callable to check.
        key: Tag key to look for.

    Returns:
        bool: True if the tag exists, False otherwise.
    """
    _ensure_callable(func, "haskey")
    return key in getattr(func, "__chino_tags", {})


def haskeys(func: Callable, *keys: str) -> bool:
    """
    Check whether the callable has all specified tag keys.

    Args:
        func: Callable to check.
        *keys: Tag keys to verify.

    Returns:
        bool: True if all specified tags exist and are truthy, False otherwise.
    """
    _ensure_callable(func, "haskeys")
    tags = getattr(func, "__chino_tags", {})
    return all(key in tags for key in keys)

def hastag(func: Callable, key:str) -> bool:
    """
    Check whether the callable has a given tag key with truthy values.

    Args:
        func: Callable to check.
        key: Tag key to look for.

    Returns:
        bool: True if the tag exists, False otherwise.
    """
    _ensure_callable(func, "hastag")
    return getattr(func, "__chino_tags", {}).get(key, False)

def hastags(func: Callable, *keys: str) -> bool:
    """
    Check whether the callable has all specified tag keys with truthy values.

    Args:
        func: Callable to check.
        *keys: Tag keys to verify.

    Returns:
        bool: True if all specified tags exist and are truthy, False otherwise.
    """
    _ensure_callable(func, "hastags")
    tags = getattr(func, "__chino_tags", {})
    return all(tags.get(key, False) for key in keys)

def gettag(func: Callable, key: str, default: Any = None) -> Any:
    """
    Retrieve the value of a specific tag on the callable.

    Args:
        func: Callable from which to retrieve the tag.
        key: Tag key to retrieve.
        default: Value to return if tag is missing (default: None).

    Returns:
        Any: The tag value or the default if not found.
    """
    _ensure_callable(func, "gettag")
    return getattr(func, "__chino_tags", {}).get(key, default)


def gettags(func: Callable, *keys: str) -> dict[str, Any]:
    """
    Retrieve multiple tags and their values from the callable.

    Args:
        func: Callable to query.
        *keys: Tag keys to retrieve.

    Returns:
        dict: A dictionary of tag keys to their values for all found keys.
    """
    _ensure_callable(func, "gettags")
    tags = getattr(func, "__chino_tags", {})
    return {key: tags[key] for key in keys if key in tags}

def deltags(func: Callable, *keys: str) -> None:
    """
    Remove one or more tags from the function's __chino_tags dictionary.

    Args:
        func: The callable object whose tags will be modified.
        *tags: Tag keys to remove.

    Example:
        deltags(func, "role", "admin")
    """
    _ensure_callable(func, "deltags")
    if not all(isinstance(key, str) for key in keys):
        raise TypeError(f"[{MODULE}.deltags] all keys must be str.")
    tags = getattr(func, "__chino_tags", None)
    if isinstance(tags, dict):
        for key in keys:
            tags.pop(key, None)

def alltags(func: Callable) -> dict[str, Any]:
    """
    Retrieve the complete __chino_tags dictionary from the callable.

    Args:
        func: Callable to query.

    Returns:
        dict[str, Any]: A dictionary of all tag keys and their corresponding values.
                        Returns an empty dict if no tags are present.
    """
    _ensure_callable(func, "alltags")
    return getattr(func, "__chino_tags", {})

@_debug_when
def tagpop(*keys: str):
    """
    Decorator that removes one or more tags from the decorated callable.

    Args:
        *keys: Tag keys to remove from the function's __chino_tags dictionary.

    Returns:
        Callable: The decorated function with specified tags removed.
    """
    def decorator(func: Callable):
        _ensure_callable(func, "tagpop")
        deltags(func, *keys)
        return func
    return decorator