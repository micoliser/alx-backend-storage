#!/usr/bin/env python3
""" This module contains a function that returns students sorted by average """


def top_students(mongo_collection):
    """ returns all students sorted by average score """

    if mongo_collection is None:
        return []
    return mongo_collection.aggregate([
        {'$project': {
            'name': '$name',
            'averageScore': {'$avg': '$topics.score'}
        }},
        {'$sort': {'averageScore': -1}}
    ])
