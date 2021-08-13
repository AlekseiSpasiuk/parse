

def find_bd(price, cur = "USD"):
    from pymongo import MongoClient
    import requests
    import json

    client = MongoClient("127.0.0.1",27017)
    db = client["hh"]

    res = db.vacancy.find( {"$or": [
            {"$and": [{"currency":cur}, {"min_price": {"$gte": price}}, {"max_price": {"$lte": price}}]},
            {"$and": [{"currency":cur}, {"min_price": {"$gte": price}}, {"max_price": {"$gte": price}}]},
            {"$and": [{"currency":cur}, {"min_price": {"$gte": price}}]},
            {"$and": [{"currency":cur}, {"max_price": {"$gte": price}}]}
        ]})
    return (list(res))

z = find_bd(4000)
for l in z:
    print(l)
