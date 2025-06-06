# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

__all__ = ["when", "whileloop", "foreach", "CommandDispatcher"]

from .control import (
    when,
    whileloop,
    foreach
)

from .registry import (
    CommandDispatcher
)