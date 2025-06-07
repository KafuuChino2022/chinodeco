# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import pytest
from chinodeco.decodsl.registry import CommandDispatcher
from chinodeco.debug.errors import (
    UnknownCommandError,
    ArgumentCountError,
    UnknownParameterError
)

def test_basic_registration_and_run():
    dispatcher = CommandDispatcher()

    @dispatcher.register("hello")
    def hello():
        return "world"

    assert dispatcher.run("hello") == "world"

def test_args_and_kwargs_parsing():
    dispatcher = CommandDispatcher()

    @dispatcher.register("greet")
    def greet(name, age=None):
        return f"{name} is {age} years old"

    result = dispatcher.run('greet Alice --age 18')
    assert result == "Alice is 18 years old"

def test_short_flag_expansion():
    dispatcher = CommandDispatcher()

    @dispatcher.register("flags")
    def flags(a=False, b=False, c=False):
        return f"a={a}, b={b}, c={c}"

    result = dispatcher.run("flags -abc")
    assert result == "a=True, b=True, c=True"

def test_command_with_dash_dash_args():
    dispatcher = CommandDispatcher()

    @dispatcher.register("cmd sub")
    def subcmd(x, y):
        return f"{x} + {y}"

    result = dispatcher.run('cmd sub -- 1 2')
    assert result == "1 + 2"

def test_unknown_command_error():
    dispatcher = CommandDispatcher()
    with pytest.raises(UnknownCommandError):
        dispatcher.run("nonexistent")

def test_argument_count_error():
    dispatcher = CommandDispatcher()

    @dispatcher.register("echo")
    def echo(a, b):
        return f"{a} {b}"

    with pytest.raises(ArgumentCountError):
        dispatcher.run("echo onlyone")

def test_unexpected_keyword_error():
    dispatcher = CommandDispatcher()

    @dispatcher.register("echo")
    def echo(x):
        return x

    with pytest.raises(ArgumentCountError):
        dispatcher.run("echo --y 123")

def test_overwrite_warning(recwarn):
    dispatcher = CommandDispatcher()

    @dispatcher.register("conflict")
    def a():
        return "a"

    @dispatcher.register("conflict")
    def b():
        return "b"

    result = dispatcher.run("conflict")
    assert result == "b"

    warning = recwarn.pop(RuntimeWarning) if recwarn else recwarn.pop()
    assert "is already registered" in str(warning.message)