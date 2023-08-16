#!/usr/bin/env python3
""" This module is used to list all documents in a collection """


def list_all(mongo_collection):
    """ returns all documents in a collection """

    if mongo_collection is None:
        return []
    return mongo_collection.find()
