# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
    仅包含0.0.5及以前的样例
"""

from chinodeco import (
    decochain,
    addprefix,
    addsuffix,
    filterargs
)

from chinodeco.debug import (
    debug,
    trycatch
)

from chinodeco.decodsl import (
    when,
    whileloop,
    foreach, 
    CommandDispatcher
)

d = CommandDispatcher()

def test_trycatch_handler_argument_count():
    @trycatch(ValueError, lambda: "wrong handler")  # no parameter
    def fail():
        raise ValueError("fail")
    
    fail()

@when(0)(
    addsuffix(("[_]", "msg"))
).elsedeco(
    decochain(addsuffix(("[.]", 0)), addprefix(("[above]", "msg")))
)
@when(lambda: 1 - 1)(
    addprefix(("[system]", 0))
).elsedeco(when(d is not None)(
    addprefix(("1", 0), ("2", "msg"))
))
def hello(msg):
    print(msg)

@debug
@d.register("print")
def prt(message: str):
    return print(message)

c = 3

@whileloop(lambda: c > 0, loop_wrapper = d.register("print count_c")).elsedo(
    print, f"in else"
)
def counter1():
    global c
    print(c)
    c -= 1

@whileloop(lambda: c > 0).elsedo(
    lambda: print(f"c is {c}")
)
def counter2():
    global c
    print(c)
    c -= 1

b = 0
@foreach(range(10))
def counter3():
    global b
    print(b)
    b += 1

@filterargs(block=[1, "a"])
def a(*args):
    return args

@trycatch(Exception, lambda e: print(e))
def main():
    test_trycatch_handler_argument_count()
    print(a(1, 2, "a", "b"))
    
    hello("你好")
    print(hello.__name__)
    
    cmd = str(input("please enter 'print', the args include 'message': str\n>"))
    d.run(cmd)
    print(prt.__name__)
    
    global c
    counter1()
    counter2()
    c = 4
    d.run(input("please enter 'print count_c'\n>"))
    
    counter3()

if __name__ == "__main__":
    main()