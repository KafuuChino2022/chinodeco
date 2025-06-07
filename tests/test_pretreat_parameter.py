# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest
from chinodeco.pretreat.parameter import setargs, mapargs, filterargs
from chinodeco.pretreat.parameter import addprefix, addsuffix


def test_setargs_positional():
    @setargs(("fixed", 0))
    def func(x, y): return x, y

    assert func("ignored", "y") == ("fixed", "y")


def test_setargs_keyword():
    @setargs((42, "y"))
    def func(x, y=0): return x + y

    assert func(1) == 43


def test_mapargs_positional():
    @mapargs((str.upper, 0))
    def shout(x): return x

    assert shout("hello") == "HELLO"


def test_mapargs_keyword():
    @mapargs((lambda v: v * 2, "n"))
    def double(n): return n

    assert double(n=3) == 6


def test_mapargs_invalid_func():
    with pytest.raises(TypeError):
        @mapargs((None, 0))
        def f(x): return x
        f("x")

    with pytest.raises(TypeError):
        @mapargs(((lambda x, y: x + y), 0))
        def f(x): return x
        f("x")


def test_filterargs_allow():
    @filterargs(allow=["keep"])
    def echo(*args): return args

    assert echo("keep", "drop") == ("keep",)


def test_filterargs_block():
    @filterargs(block=["x", 1])
    def echo(*args): return args

    assert echo("x", 1, "ok") == ("ok",)


def test_filterargs_both_invalid():
    with pytest.raises(ValueError):
        @filterargs(allow=["a"], block=["b"])
        def f(): pass


def test_addprefix_positional():
    @addprefix(("PRE_", 0))
    def process(x): return x

    assert process("data") == "PRE_data"


def test_addsuffix_keyword():
    @addsuffix(("_END", "word"))
    def process(word): return word

    assert process(word="hello") == "hello_END"