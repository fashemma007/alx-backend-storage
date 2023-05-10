#!/usr/bin/env python3
"""Cache class module"""
from typing import Union
from uuid import uuid4
import redis


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

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
