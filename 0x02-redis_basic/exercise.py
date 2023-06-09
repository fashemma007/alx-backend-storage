#!/usr/bin/env python3
"""Cache class module"""
from typing import Callable, Optional, Union
from uuid import uuid4
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """decorator func that returns a Callable"""
    key = method.__qualname__  # sets the function's name as redis key

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        # increases the value each time the func is called
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        inputs = str(args)  # stringify passed in arguments
        # stringify return value
        outputs = str(method(self, *args, **kwargs))

        # create a key with list as values using rpush
        # method.__qualname__ returns the name of the called func / method
        # and appends :inputs to it e.g `Cache.store:inputs`

        # append functions return to redis list `Cache.store:inputs`
        self._redis.rpush(method.__qualname__ + ":inputs", inputs)
        # append functions return to redis list `Cache.store:outputs`
        self._redis.rpush(method.__qualname__ + ":outputs", outputs)
        return outputs

    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    # print(function_name)
    value = r.get(function_name)  # get the number of times twas called
    # print(value)
    try:
        value = int(value.decode("utf-8"))
    except UnicodeDecodeError:
        value = 0
    except ValueError:
        value = 0
    print("{} was called {} times:".format(function_name, value))

    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)
    # abc = zip(inputs, outputs)
    # for a, b in abc:
    #     print(a, b)

    # since all values are byte-encoded, we av to decode to utf-8
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except UnicodeDecodeError:
            input = ""

        try:
            output = output.decode("utf-8")
        except UnicodeDecodeError:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
