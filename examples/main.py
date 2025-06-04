# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

from chinodeco import *
from chinodeco.decodsl import when

@when(0, elsedeco = decochain(addsuffix(("[.]", 0))))(
    addsuffix(("[_]", 0))
)
@when(1)(
    addprefix(("[system]", 0))
)
def hello(msg):
    print(msg)

def main():
    hello("你好")

if __name__ == "__main__":
    main()