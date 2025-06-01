#!/usr/bin/env python3
"""Utility module with helper functions."""

import requests
from typing import Mapping, Any, Sequence
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a value in a nested dictionary using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """Make a GET request to a given URL and return the JSON response."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def memoize(method: callable) -> callable:
    """Decorator to cache the result of a method."""
    attr_name = f"_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
