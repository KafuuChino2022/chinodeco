# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

__version__ = "0.0.7"
__all__ = ["decochain", "setargs", "addprefix", "addsuffix", "mapargs", "filterargs"]

from .base import decochain
from .pretreat import (
    setargs,
    addprefix,
    addsuffix,
    mapargs,
    filterargs
)