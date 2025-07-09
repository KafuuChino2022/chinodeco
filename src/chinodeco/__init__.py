# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

__version__ = "0.0.11"
__all__ = ["decochain", "setargs", "addprefix", "addsuffix", "mapargs", "filterargs", "tag", "tagpop", "settags", "haskey", "haskeys", "gettag", "gettags", "deltags", "alltags", "hastag", "hastags"]

from .base import decochain
from .pretreat import (
    setargs, addprefix,
    addsuffix, mapargs,
    filterargs,

    tag, tagpop, 
    settags, haskey, 
    haskeys, gettag, 
    gettags, deltags,
    alltags,hastags,
    hastag
)