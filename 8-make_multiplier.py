#!/usr/bin/env python3
'''Defining the 8-make_multiplier module'''

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''
    make_multiplier that takes a float multiplier as argument
    and returns a function that multiplies a float by multiplier.
    '''
    return lambda n: n * multiplier
