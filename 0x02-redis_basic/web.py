#!/usr/bin/env python3
""" implement a get page function """
from functools import wraps
from typing import Callable
import redis
import requests


r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ count requests decorator """

    @wraps(method)
    def wrapper(url: str) -> str:
        """ wrapper function """

        r.incr('count:{}'.format(url))
        result = r.get('result:{}'.format(url))
        if result:
            return result.decode('utf-8')
        result = method(url)
        r.set('count:{}'.format(url), 0)
        r.setex('result:{}'.format(url), 10, result)
        return result
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ the get page function """

    return requests.get(url).text
