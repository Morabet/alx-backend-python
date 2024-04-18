#!/usr/bin/env python3
'''Defining the module 101-safely_get_value'''

from typing import TypeVar, Union, Any, Mapping


T = TypeVar('T')


def safely_get_value(
        dct: Mapping,
        key: Any,
        default: Union[T, None] = None
) -> Union[Any, T]:
    '''adding type annotations to the function'''
    if key in dct:
        return dct[key]
    else:
        return default
