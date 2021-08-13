def init_db_ann_load_data():
    from pymongo import MongoClient
    import json

    client = MongoClient("127.0.0.1",27017)
    db = client["hh"]

    with open("./vacancy_python.json", "r") as f:
        data = json.load(f)

    for l in data:
        res = db.vacancy.find(l).count()
        if res == 0:
            db.vacancy.insert_one(l)

init_db_ann_load_data()
