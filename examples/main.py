# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from chinodeco import *
from chinodeco.decodsl import when

@when(0)(
    addsuffix(("[_]", "msg"))
).elsedeco(
    decochain(addsuffix(("[.]", 0)), addprefix(("[above]", "msg")))
)
@when(1)(
    addprefix(("[system]", "msg"))
)
def hello(msg):
    print(msg)

def main():
    hello("你好")
    print(hello.__name__)

if __name__ == "__main__":
    main()