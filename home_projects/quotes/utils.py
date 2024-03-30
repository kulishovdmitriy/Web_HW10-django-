from pymongo import MongoClient


def get_mongodb():
    client = MongoClient(
        'mongodb+srv://dmitriyykulishov:52628271@mongodb.dtj8cur.mongodb.net/?retryWrites=true&w=majority&appName=mongoDB'
    )
    db = client.mongodb

    return db
