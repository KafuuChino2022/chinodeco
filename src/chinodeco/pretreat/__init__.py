# !/usr/bin/env Python3
# -*- coding:utf-8 -*-

__all__ = ["setargs", "addprefix", "addsuffix", "mapargs", "filterargs", "tag", "tagpop", "settags", "haskey", "haskeys", "gettag", "gettags", "deltags", "alltags", "hastag", "hastags"]

from .parameter import (
    setargs,
    addprefix,
    addsuffix,
    mapargs,
    filterargs
)

from .attrset import (
    tag, 
    tagpop, 
    settags, 
    haskey, 
    haskeys, 
    gettag, 
    gettags, 
    deltags,
    alltags,
    hastags,
    hastag
)