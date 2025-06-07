# !/usr/bin/env Python3
# -*- coding:utf-8 -*-
import warnings

warnings.warn(
    "chinodeco.parameter is deprecated and will be removed in a future version. "
    "Please use chinodeco.pretreat or chinodeco.pretreat.parameter instead. ",
    DeprecationWarning,
    stacklevel = 2
)

__all__ = ["setargs", "addprefix", "addsuffix", "mapargs", "filterargs"]

from ..pretreat.parameter import (
    setargs,
    addprefix,
    addsuffix,
    mapargs,
    filterargs
)