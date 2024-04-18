#!/usr/bin/env python3
'''Defining the 100-safe_first_element module'''

from typing import Any, Iterable, Optional, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''Augmenting the following code with the correct duck-typed annotations'''
    if lst:
        return lst[0]
    else:
        return None
