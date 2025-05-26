#!/usr/bin/env python3
"""
Module containing utility functions
"""

from typing import Any, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map with a given path of keys"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
