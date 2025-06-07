# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest
from chinodeco.base import decochain

def test_decochain_applies_in_order():
    order = []

    def d1(f):
        def wrapper(*args, **kwargs):
            order.append("d1")
            return f(*args, **kwargs)
        return wrapper

    def d2(f):
        def wrapper(*args, **kwargs):
            order.append("d2")
            return f(*args, **kwargs)
        return wrapper

    @decochain(d1, d2)
    def func():
        return "done"

    order.clear()
    result = func()
    assert result == "done"
    assert order == ["d1", "d2"], "decorators should apply outer-to-inner (reversed in code)"

def test_decochain_with_none_values():
    # None should be ignored silently
    @decochain(None, lambda f: f)
    def func():
        return 100

    assert func() == 100

def test_decochain_empty_input():
    # No decorators: should return original function
    @decochain()
    def identity(x):
        return x

    assert identity("ok") == "ok"

def test_decochain_preserves_wrapped_signature():
    from inspect import signature

    def multiply_by_two(f):
        def wrapper(x):
            return f(x * 2)
        return wrapper

    @decochain(multiply_by_two)
    def square(x):
        return x * x

    sig = signature(square)
    assert list(sig.parameters) == ['x']
    assert square(3) == 36  # (3 * 2)^2