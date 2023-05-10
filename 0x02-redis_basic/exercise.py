#!/usr/bin/env python3
"""Cache class module"""
from typing import Callable, Optional, Union
from uuid import uuid4
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """decorator func that returns a Callable"""
    key = method.__qualname__  # sets the method's name as redis key

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        # increases the value each time the func is called
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        The store function takes in a string, bytes, int or float and stores it
        in redis.

        data: variable data to be stored
        return: It returns the key that was used to store the data.

        """
        uuid_key = str(uuid4())  # generate a random key
        self._redis.set(uuid_key, data)  # store data in redis using uuid-key
        return uuid_key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """
        take a `key` string argument and an optional `Callable` argument named
        `fn` that will be used to convert the data back to the desired format
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get with the correct
        conversion function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except ValueError:
            value = 0
        return value
