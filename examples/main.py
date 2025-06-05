# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from chinodeco import *
from chinodeco.debug import debug
from chinodeco.decodsl import (
    when,
    CommandDispatcher
)

d = CommandDispatcher()

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

def main():
    
    hello("你好")
    print(hello.__name__)
    
    cmd = str(input(">"))
    d.run(cmd)
    print(prt.__name__)

if __name__ == "__main__":
    main()