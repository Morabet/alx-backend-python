#!/usr/bin/env python3
'''Defining the 7-to_kv module'''

from math import pow
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''
    to_kv that takes a string k and an int OR float v as arguments
    and returns a tuple. The first element of the tuple is the string
    '''
    return (k, pow(v, 2))
