#!/usr/bin/env python3
""" This module contains a Cache class. """
from functools import wraps
from typing import Union, Callable
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """ Count calls decorator. """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function. """

        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ call history decorator """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function """

        self._redis.rpush(method.__qualname__ + ':inputs', str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ':outputs', str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """ replay function to display history of calls to function """

    r = redis.Redis()
    print("{} was called {} times:".format(method.__qualname__,
                                           r.get(method.__qualname__)
                                           .decode('utf-8')))

    inputs = r.lrange(method.__qualname__ + ':inputs', 0, -1)
    outputs = r.lrange(method.__qualname__ + ':outputs', 0, -1)

    for input, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(method.__qualname__,
                                     input.decode('utf-8'),
                                     output.decode('utf-8')))


class Cache:
    """ Cache class. """

    def __init__(self) -> None:
        """ Initialize class instance. """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in redis. """

        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float]:
        """ gets a value from the cache. """

        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """ gets a value from the cache converted to string """

        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ gets a value from the cache converted to int """

        return self.get(key, int)
