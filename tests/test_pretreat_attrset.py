# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest
from chinodeco.pretreat.tagging import (
    tag, tagpop, settags,
    haskey, haskeys,
    hastag, hastags,
    gettag, gettags,
    deltags, alltags
)

# 测试用函数
@tag("admin", ("role", "superuser"))
def sample():
    return 42

def test_settags_and_gettags():
    def f(): pass
    settags(f, "alpha", ("beta", 2))
    assert gettag(f, "alpha") is True
    assert gettag(f, "beta") == 2
    assert gettag(f, "gamma", "default") == "default"
    assert gettags(f, "alpha", "beta") == {"alpha": True, "beta": 2}
    assert gettags(f, "alpha", "missing") == {"alpha": True}

def test_tag_decorator():
    assert gettag(sample, "admin") is True
    assert gettag(sample, "role") == "superuser"
    assert haskey(sample, "role") is True
    assert haskeys(sample, "admin", "role") is True
    assert hastag(sample, "admin") is True
    assert hastags(sample, "admin", "role") is True

def test_tagpop_decorator():
    @tagpop("x")
    @tag("x", ("y", 1))
    def f(): pass

    assert haskey(f, "y")
    assert not haskey(f, "x")

def test_alltags():
    def f(): pass
    settags(f, "a", ("b", 2))
    tags = alltags(f)
    assert tags == {"a": True, "b": 2}

def test_deltags():
    def f(): pass
    settags(f, "x", ("y", 9))
    deltags(f, "x")
    assert not haskey(f, "x")
    deltags(f, "y", "nonexistent")  # Should silently ignore missing
    assert not haskey(f, "y")

def test_type_errors():
    with pytest.raises(TypeError):
        settags(123, "bad")  # not callable

    def f(): pass
    with pytest.raises(TypeError):
        settags(f, 1)  # invalid tag type

    with pytest.raises(TypeError):
        settags(f, ("not",))  # invalid tuple

    with pytest.raises(TypeError):
        deltags(f, "ok", 123)  # non-str key

def test_missing_tags_behavior():
    def f(): pass
    assert haskey(f, "missing") is False
    assert gettag(f, "missing", "fallback") == "fallback"
    assert gettags(f, "a", "b") == {}
    assert hastag(f, "any") is False
    assert hastags(f, "a", "b") is False
    assert alltags(f) == {}