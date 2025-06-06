# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

__version__ = "0.0.6"
__all__ = ["decochain", "setargs", "addprefix", "addsuffix", "mapargs", "filterargs"]

from .base import decochain
from .parameter import (
    setargs,
    addprefix,
    addsuffix,
    mapargs,
    filterargs
)