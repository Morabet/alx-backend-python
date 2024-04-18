#!/usr/bin/env python3
'''Defining the 9-element_length module'''

from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''
    For each element i, it creates a tuple (i, len(i)), where i represents
    the original sequence element, and len(i) represents the length of
    that sequence element.
    '''
    return [(i, len(i)) for i in lst]
