# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest
from chinodeco.debug.debugger import debug, trycatch, ArgumentCountError

# ========== Tests for @debug ==========

def test_debug_basic_suppression(capfd):
    @debug
    def will_fail():
        raise ValueError("something broke")
    
    result = will_fail()
    assert result is None

    out, _ = capfd.readouterr()
    assert "something broke" in out
    assert "[" not in out  # non-verbose 不含函数信息

def test_debug_verbose(capfd):
    @debug(verbose=True)
    def fail():
        raise RuntimeError("detailed")
    
    fail()
    out, _ = capfd.readouterr()
    assert "detailed" in out
    assert "fail" in out
    assert "debug" in out  # MODULE名打印

def test_debug_success():
    @debug
    def safe(x):
        return x * 2
    
    assert safe(4) == 8


# ========== Tests for @trycatch ==========

def test_trycatch_valueerror_handled():
    @trycatch(ValueError, lambda e: f"Handled {e}")
    def risky(x):
        return int(x)
    
    assert risky("abc") == "Handled invalid literal for int() with base 10: 'abc'"

def test_trycatch_success_passthrough():
    @trycatch(ValueError, lambda e: "handled")
    def fine(x):
        return int(x)
    
    assert fine("42") == 42

def test_trycatch_multiple_exceptions():
    @trycatch((ValueError, ZeroDivisionError), lambda e: "rescued")
    def risky(x):
        return 10 / int(x)

    assert risky("0") == "rescued"
    assert risky("abc") == "rescued"

def test_trycatch_unhandled_exception():
    @trycatch(ValueError, lambda e: "rescued")
    def boom():
        raise KeyError("not covered")

    with pytest.raises(KeyError):
        boom()

def test_trycatch_handler_argument_count():
    with pytest.raises(ArgumentCountError) as e:
        @trycatch(ValueError, lambda: "wrong handler")
        def dummy_func():
            raise ValueError("test")

    assert "must accept exactly one argument" in str(e.value)