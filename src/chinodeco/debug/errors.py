# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

MODULE = "chinodeco.debug.errors"

class UnknownCommandError(Exception):
    pass

class UnknownParameterError(Exception):
    pass

class ArgumentCountError(TypeError):
    pass