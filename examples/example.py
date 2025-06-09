# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

import asyncio

from chinodeco import decochain
from chinodeco.debug import debug, trycatch
from chinodeco.decodsl import when, whileloop, foreach
from chinodeco.pretreat import setargs, addprefix, addsuffix, mapargs, filterargs
from chinodeco.decodsl import CommandDispatcher
from chinodeco.pretreat import tag

@decochain(debug, foreach(range(10), loop_wrapper = decochain(setargs(("1", 0)), addprefix(("pre_", "param2")), addsuffix(("_suf", 2)), mapargs((str.upper, "param4")), filterargs(block=["hello"]))))
async def async_func(param1, param2, param3, param4, **kwargs):
    print(param1, param2, param3, param4, kwargs)

@trycatch(Exception, lambda e: print(f"{e}"))
@when(True)(
    whileloop(True, max_loops=2)
)
async def a_f():
    print(1)

async def main():
    asyncio.gather(async_func("0", "1", "2", "3", k = "hello"), a_f())

d = CommandDispatcher()

@d.register("print", debug(verbose=True), tag("admin"))
def prt(msg):
    print(msg)

def sync_main():
    try:
        d.run(input(">"), "user")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    asyncio.run(main())
    sync_main()