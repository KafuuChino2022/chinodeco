# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest

from chinodeco.decodsl.control import when, whileloop, foreach

def test_when_true_applies_decorator():
    def uppercase(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).upper()
        return wrapper

    @when(True)(uppercase)
    def greet():
        return "hello"
    
    assert greet() == "HELLO"

def test_when_false_skips_decorator():
    def uppercase(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).upper()
        return wrapper

    @when(False)(uppercase)
    def greet():
        return "hello"
    
    assert greet() == "hello"

def test_when_false_elsedeco_applied():
    def fail(func):
        def wrapper(*args, **kwargs):
            return "FAIL"
        return wrapper

    def success(func):
        def wrapper(*args, **kwargs):
            return "SUCCESS"
        return wrapper

    @when(False)(fail).elsedeco(success)
    def greet():
        return "hello"
    
    assert greet() == "SUCCESS"

def test_whileloop_static_true_runs_n_times():
    count = {"value": 0}
    @whileloop(True, max_loops=3)
    def inc():
        count["value"] += 1

    inc()
    assert count["value"] == 3

def test_whileloop_predicate_and_break():
    state = {"x": 0}

    def cond(): return state["x"] < 10
    def brk(): return state["x"] >= 5

    @whileloop(cond, max_loops=10).ifbreak(brk)
    def task():
        state["x"] += 1

    task()
    assert state["x"] == 5

def test_whileloop_fallback_called(monkeypatch):
    flag = {"called": False}

    def fallback():
        flag["called"] = True

    @whileloop(False, max_loops=1).elsedo(fallback)
    def nothing(): pass

    nothing()
    assert flag["called"] is True

def test_foreach_with_iterable():
    data = []

    @foreach(iter=[1, 2, 3])
    def f():
        data.append(1)

    f()
    assert data == [1, 1, 1]

def test_foreach_with_max_loops():
    data = []

    @foreach(max_loops=4)
    def f():
        data.append(1)

    f()
    assert len(data) == 4

def test_foreach_invalid_iter_type():
    with pytest.raises(TypeError):
        @foreach(iter=123)
        def fail(): pass

        fail()