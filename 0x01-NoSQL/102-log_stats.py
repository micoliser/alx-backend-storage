#!/usr/bin/env python3
""" This module logs some stats about a nginx collection """


def log_stats():
    """ show some log stats about a nginx collection """
    from pymongo import MongoClient

    client = MongoClient()
    db = client.logs

    print("{} logs".format(db.nginx.count_documents({})))
    print("Methods:")

    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        count = db.nginx.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    count = db.nginx.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(count))
    print("IPs:")
    pipeline = [
        {'$group': {'_id': '$ip', 'countIps': {'$sum': 1}}},
        {'$sort': {'countIps': -1}},
        {'$limit': 10}
    ]
    for ip in db.nginx.aggregate(pipeline):
        print("\t{}: {}".format(ip.get('_id'), ip.get('countIps')))
    client.close()


if __name__ == '__main__':
    log_stats()
