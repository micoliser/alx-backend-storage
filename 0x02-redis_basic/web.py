#!/usr/bin/env python3
""" implement a get page function """
import redis
import requests


r = redis.Redis()


def get_page(url: str) -> str:
    """ the get page function """

    r.incr("count:{}".format(url))
    r.expire("count:{}".format(url), 10)
    return requests.get(url).text