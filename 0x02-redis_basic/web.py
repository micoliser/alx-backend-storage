#!/usr/bin/env python3
""" implement a get page function """
from functools import wraps
from redis.client import Redis
from typing import Callable
import requests


r = Redis()


def count_requests(method: Callable) -> Callable:
    """ count requests decorator """

    @wraps(method)
    def wrapper(url):
        """ wrapper function """

        r.incr("count:{}".format(url))
        result = r.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        r.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ the get page function """

    return requests.get(url).text
